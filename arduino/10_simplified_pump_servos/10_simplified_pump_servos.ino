/*
 * ============================================================================
 * LABORATORIO 2 - CONTROL HIDRÁULICO (VERSIÓN SIMPLIFICADA + YF0401)
 * Universidad Militar Nueva Granada
 * Ingeniería Mecatrónica - Control Lineal y Laboratorio
 * ============================================================================
 * 
 * VERSIÓN DEPURADA: BOMBA + SERVOS + YF0401 FLOW SENSOR
 * 
 * Descripción:
 *   Control simple de bomba y válvulas servo para la interfaz Python.
 *   Incluye medición de caudal con YF0401 en GPIO 6.
 * 
 * Hardware:
 *   - ESP32-S3 DevKit
 *   - H-Bridge L298N + Motor 12V (BOMBA)
 *   - 2x Servos para válvulas (GPIO 18, 19)
 *   - YF0401 caudalímetro (GPIO 6)
 * 
 * Conexiones:
 *   GPIO 17 → H-Bridge ENA (PWM motor)
 *   GPIO 15 → H-Bridge IN1
 *   GPIO 16 → H-Bridge IN2
 *   GPIO 18 → Servo valve Tank 1
 *   GPIO 19 → Servo valve Tank 2
 *   GPIO 7  → LED Status
 *   GPIO 6  → YF0401 Flow Sensor (pulsos)
 * 
 * Comandos UART (115200 baud):
 *   PUMP,<pwm>        - Control bomba (0-255)
 *   SERVO1,<angle>    - Servo 1 ángulo (0-180)
 *   SERVO2,<angle>    - Servo 2 ángulo (0-180)
 *   TIMECFG,<tank>,<fill_ms>,<open_angle>,<close_angle>
 *                     - Configurar tiempos de tanque
 *   TIMESEQ,<pwm>     - Iniciar secuencia temporal con PWM
 *   TIMESTOP          - Detener secuencia temporal
 *   TIMESTAT          - Ver configuración de tiempos
 *   FLOW              - Mostrar caudal actual
 *   FLOWCAL,<pulsos>  - Calibrar sensor (pulsos/litro)
 *   STOP              - Parar bomba
 *   STATUS            - Estado actual
 *   HELP              - Menú de ayuda
 * 
 * Autor: David Santiago García Suarez
 * Fecha: Mayo 2026
 * Versión: 2.1 (Con YF0401)
 * ============================================================================
 */

#include <ESP32Servo.h>

// ============================================================================
// DEFINICIÓN DE PINES
// ============================================================================

#define MOTOR_PWM_PIN    17    // PWM bomba
#define MOTOR_IN1_PIN    15    // Dirección 1
#define MOTOR_IN2_PIN    16    // Dirección 2
#define SERVO_TANK1_PIN  18    // Servo válvula tanque 1
#define SERVO_TANK2_PIN  19    // Servo válvula tanque 2
#define LED_STATUS_PIN   7     // LED indicador
#define FLOW_SENSOR_PIN  6     // YF0401 caudalímetro (pulsos)

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

#define PWM_FREQUENCY       10000
#define PWM_RESOLUTION      8     // 0-255
#define SERVO_MIN_ANGLE     0
#define SERVO_MAX_ANGLE     180
#define SEQUENCE_TIMEOUT_MS 120000  // 2 minutos máximo
#define FLOW_CALIBRATION    450     // Pulsos por litro (YF0401 típico)
#define FLOW_UPDATE_MS      1000    // Actualizar caudal cada 1 segundo

// ============================================================================
// VARIABLES GLOBALES
// ============================================================================

// Bomba
int currentPWM = 0;
bool motorRunning = false;
bool motorDirection = false;  // false = adelante, true = atrás

// Servos
Servo servo1, servo2;
int servo1_angle = 90;  // Posición inicial
int servo2_angle = 90;

// Caudalímetro
volatile unsigned long flow_pulse_count = 0;
unsigned long last_flow_update_time = 0;
float current_flow_lmin = 0.0;
float flow_calibration_factor = FLOW_CALIBRATION;

// Control por tiempos
struct TankTimingConfig {
  unsigned long fill_time_ms;
  int open_angle;
  int close_angle;
};

TankTimingConfig tank1_config = {10000, 45, 135};
TankTimingConfig tank2_config = {8000, 45, 135};

bool time_seq_active = false;
int time_seq_pump_pwm = 0;
unsigned long time_seq_start_ms = 0;
unsigned long time_seq_step_start_ms = 0;
int time_seq_step = 0;
unsigned long last_telemetry_ms = 0;
#define TELEMETRY_INTERVAL_MS 100

// Buffer UART
String commandBuffer = "";

// ============================================================================
// INTERRUPCIONES
// ============================================================================

// ISR para contar pulsos del caudalímetro
void IRAM_ATTR flowPulseISR() {
  flow_pulse_count++;
}

// ============================================================================
// SETUP
// ============================================================================

void setup() {
  Serial.begin(115200);
  delay(500);
  
  // Configurar GPIO
  pinMode(MOTOR_PWM_PIN, OUTPUT);
  pinMode(MOTOR_IN1_PIN, OUTPUT);
  pinMode(MOTOR_IN2_PIN, OUTPUT);
  pinMode(LED_STATUS_PIN, OUTPUT);
  pinMode(FLOW_SENSOR_PIN, INPUT);
  
  // Caudalímetro con interrupción
  attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_PIN), flowPulseISR, RISING);
  last_flow_update_time = millis();
  
  // Configurar PWM
  ledcAttach(MOTOR_PWM_PIN, PWM_FREQUENCY, PWM_RESOLUTION);
  
  // Inicializar servos
  servo1.attach(SERVO_TANK1_PIN);
  servo2.attach(SERVO_TANK2_PIN);
  servo1.write(servo1_angle);
  servo2.write(servo2_angle);
  
  // Estado inicial
  digitalWrite(MOTOR_IN1_PIN, LOW);
  digitalWrite(MOTOR_IN2_PIN, LOW);
  ledcWrite(MOTOR_PWM_PIN, 0);
  digitalWrite(LED_STATUS_PIN, LOW);
  
  printWelcome();
}

// ============================================================================
// LOOP PRINCIPAL
// ============================================================================

void loop() {
  // Actualizar medición de caudal
  updateFlowMeasurement();
  
  // Procesar secuencia temporal si está activa
  if (time_seq_active) {
    updateTimeSequence();
  }
  
  // Procesar comandos UART
  if (Serial.available()) {
    char ch = Serial.read();
    
    if (ch == '\n' || ch == '\r') {
      if (commandBuffer.length() > 0) {
        processCommand(commandBuffer);
        commandBuffer = "";
      }
    } else if (ch >= 32 && ch <= 126) {
      commandBuffer += ch;
      Serial.write(ch);
    }
  }
}

// ============================================================================
// PROCESAMIENTO DE COMANDOS
// ============================================================================

void processCommand(String cmd) {
  Serial.println();
  cmd.toUpperCase();
  cmd.trim();
  
  if (cmd.startsWith("PUMP,")) {
    int pwm = cmd.substring(5).toInt();
    setPumpPWM(pwm);
    
  } else if (cmd.startsWith("SERVO1,")) {
    int angle = cmd.substring(7).toInt();
    setServo1(angle);
    
  } else if (cmd.startsWith("SERVO2,")) {
    int angle = cmd.substring(7).toInt();
    setServo2(angle);
    
  } else if (cmd.startsWith("TIMECFG,")) {
    configureTimingTank(cmd);
    
  } else if (cmd.startsWith("TIMESEQ,")) {
    int pwm = cmd.substring(8).toInt();
    startTimeSequence(pwm);
    
  } else if (cmd == "TIMESTOP") {
    stopTimeSequence();
    
  } else if (cmd == "TIMESTAT") {
    printTimeStatus();
    
  } else if (cmd == "STOP") {
    stopPump();
    
  } else if (cmd == "STATUS") {
    printStatus();
    
  } else if (cmd == "FLOW") {
    Serial.print("💧 Caudal: ");
    Serial.print(current_flow_lmin, 2);
    Serial.println(" L/min");
    
  } else if (cmd.startsWith("FLOWCAL,")) {
    float cal = cmd.substring(8).toFloat();
    if (cal > 0) {
      flow_calibration_factor = cal;
      Serial.print("✓ Calibración: ");
      Serial.print(cal);
      Serial.println(" pulsos/litro");
    } else {
      Serial.println("❌ Valor inválido");
    }
    
  } else if (cmd == "HELP") {
    printHelp();
    
  } else {
    Serial.println("❌ Comando no reconocido");
  }
}

// ============================================================================
// MEDICIÓN DE CAUDAL
// ============================================================================

void updateFlowMeasurement() {
  unsigned long now = millis();
  
  if (now - last_flow_update_time >= FLOW_UPDATE_MS) {
    // Calcular caudal: (pulsos / factor) / tiempo_en_minutos
    float pulses_per_liter = flow_calibration_factor;
    float liters_per_interval = (float)flow_pulse_count / pulses_per_liter;
    float time_interval_minutes = FLOW_UPDATE_MS / 60000.0;
    
    current_flow_lmin = liters_per_interval / time_interval_minutes;
    
    // Reset para siguiente intervalo
    flow_pulse_count = 0;
    last_flow_update_time = now;
  }
}

// ============================================================================
// CONTROL DE BOMBA
// ============================================================================

void setPumpPWM(int pwm) {
  pwm = constrain(pwm, 0, 255);
  currentPWM = pwm;
  motorRunning = (pwm > 0);
  
  if (motorRunning) {
    setMotorDirection(motorDirection);
  }
  
  ledcWrite(MOTOR_PWM_PIN, pwm);
  digitalWrite(LED_STATUS_PIN, motorRunning ? HIGH : LOW);
  
  Serial.print("✓ Bomba: ");
  Serial.print(pwm);
  Serial.print("/255 (");
  Serial.print((pwm * 100) / 255);
  Serial.println("%)");
}

void stopPump() {
  currentPWM = 0;
  motorRunning = false;
  ledcWrite(MOTOR_PWM_PIN, 0);
  digitalWrite(LED_STATUS_PIN, LOW);
  Serial.println("✓ Bomba detenida");
}

void setMotorDirection(bool direction) {
  motorDirection = direction;
  if (direction) {
    digitalWrite(MOTOR_IN1_PIN, HIGH);
    digitalWrite(MOTOR_IN2_PIN, LOW);
  } else {
    digitalWrite(MOTOR_IN1_PIN, LOW);
    digitalWrite(MOTOR_IN2_PIN, HIGH);
  }
}

// ============================================================================
// CONTROL DE SERVOS
// ============================================================================

void setServo1(int angle) {
  angle = constrain(angle, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE);
  servo1_angle = angle;
  servo1.write(angle);
  Serial.print("✓ Servo 1: ");
  Serial.print(angle);
  Serial.println("°");
}

void setServo2(int angle) {
  angle = constrain(angle, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE);
  servo2_angle = angle;
  servo2.write(angle);
  Serial.print("✓ Servo 2: ");
  Serial.print(angle);
  Serial.println("°");
}

// ============================================================================
// CONTROL POR TIEMPOS
// ============================================================================

void configureTimingTank(String cmd) {
  int idx1 = cmd.indexOf(',');
  int idx2 = cmd.indexOf(',', idx1 + 1);
  int idx3 = cmd.indexOf(',', idx2 + 1);
  int idx4 = cmd.indexOf(',', idx3 + 1);
  
  if (idx1 == -1 || idx2 == -1 || idx3 == -1) {
    Serial.println("❌ Formato: TIMECFG,tank,ms,open_angle,close_angle");
    return;
  }
  
  int tank = cmd.substring(idx1 + 1, idx2).toInt();
  unsigned long fill_ms = cmd.substring(idx2 + 1, idx3).toInt();
  int open_angle = cmd.substring(idx3 + 1, idx4 == -1 ? cmd.length() : idx4).toInt();
  int close_angle = (idx4 != -1) ? cmd.substring(idx4 + 1).toInt() : 135;
  
  if (tank == 1) {
    tank1_config.fill_time_ms = fill_ms;
    tank1_config.open_angle = open_angle;
    tank1_config.close_angle = close_angle;
    Serial.print("✓ Tank 1: ");
    Serial.print(fill_ms); Serial.print("ms, ");
    Serial.print(open_angle); Serial.print("°, ");
    Serial.print(close_angle); Serial.println("°");
  } else if (tank == 2) {
    tank2_config.fill_time_ms = fill_ms;
    tank2_config.open_angle = open_angle;
    tank2_config.close_angle = close_angle;
    Serial.print("✓ Tank 2: ");
    Serial.print(fill_ms); Serial.print("ms, ");
    Serial.print(open_angle); Serial.print("°, ");
    Serial.print(close_angle); Serial.println("°");
  }
}

void startTimeSequence(int pwm) {
  if (time_seq_active) {
    Serial.println("⚠ Secuencia activa. Usa TIMESTOP primero");
    return;
  }
  
  pwm = constrain(pwm, 0, 255);
  time_seq_active = true;
  time_seq_pump_pwm = pwm;
  time_seq_start_ms = millis();
  time_seq_step_start_ms = millis();
  time_seq_step = 1;
  last_telemetry_ms = millis();  // Reinicializar timestamp para telemetría en tiempo real
  
  setPumpPWM(pwm);
  setServo1(tank1_config.open_angle);
  
  Serial.print("▶ Secuencia: Tank 1 abierto por ");
  Serial.print(tank1_config.fill_time_ms);
  Serial.println("ms");
  
  sendSequenceTelemetry();
}

void sendSequenceTelemetry() {
  if (!time_seq_active) return;
  
  unsigned long now = millis();
  unsigned long step_elapsed = now - time_seq_step_start_ms;
  int progress = 0;
  
  if (time_seq_step == 1) {
    progress = min(100, (int)((step_elapsed * 100) / tank1_config.fill_time_ms));
  } else if (time_seq_step == 2) {
    progress = min(100, (int)((step_elapsed * 100) / tank2_config.fill_time_ms));
  }
  
  Serial.print("[DISCRETE] FILL,");
  Serial.print(time_seq_step);
  Serial.print(",");
  Serial.print(progress);
  Serial.print(",");
  Serial.println(currentPWM);
}

void stopTimeSequence() {
  time_seq_active = false;
  time_seq_step = 0;
  last_telemetry_ms = 0;  // Resetear timestamp
  stopPump();
  setServo1(tank1_config.close_angle);
  setServo2(tank2_config.close_angle);
  Serial.println("[DISCRETE] STOPPED");
}

void updateTimeSequence() {
  unsigned long now = millis();
  unsigned long total_elapsed = now - time_seq_start_ms;
  unsigned long step_elapsed = now - time_seq_step_start_ms;
  
  if (total_elapsed > SEQUENCE_TIMEOUT_MS) {
    stopTimeSequence();
    return;
  }
  
  if (now - last_telemetry_ms >= TELEMETRY_INTERVAL_MS) {
    sendSequenceTelemetry();
    last_telemetry_ms = now;
  }
  
  switch (time_seq_step) {
    case 1:
      if (step_elapsed >= tank1_config.fill_time_ms) {
        setServo1(tank1_config.close_angle);
        setServo2(tank2_config.open_angle);
        time_seq_step_start_ms = millis();
        time_seq_step = 2;
        Serial.println("[DISCRETE] TRANSITION");
      }
      break;
      
    case 2:
      if (step_elapsed >= tank2_config.fill_time_ms) {
        setServo2(tank2_config.close_angle);
        stopPump();
        time_seq_active = false;
        time_seq_step = 3;
        Serial.println("[DISCRETE] COMPLETE");
      }
      break;
  }
}

void printTimeStatus() {
  Serial.println("\n╔════ TIEMPOS ════╗");
  Serial.print("║ Tank 1: ");
  Serial.print(tank1_config.fill_time_ms);
  Serial.println("ms ║");
  Serial.print("║ Tank 2: ");
  Serial.print(tank2_config.fill_time_ms);
  Serial.println("ms ║");
  Serial.println("╚════════════════╝");
}

// ============================================================================
// INFORMACIÓN
// ============================================================================

void printWelcome() {
  Serial.println("\n╔══════════════════════════════════╗");
  Serial.println("║  HYDRAULIC CONTROL + YF0401      ║");
  Serial.println("║  UMNG - Mecatrónica Lab 2         ║");
  Serial.println("╚══════════════════════════════════╝");
  Serial.println("HELP para comandos\n");
}

void printStatus() {
  Serial.println("\n╔═══ ESTADO ═══╗");
  Serial.print("Bomba: ");
  Serial.println(motorRunning ? "ON" : "OFF");
  Serial.print("PWM: ");
  Serial.print(currentPWM);
  Serial.print("/255 (");
  Serial.print((currentPWM * 100) / 255);
  Serial.println("%)");
  Serial.print("Servo 1: ");
  Serial.print(servo1_angle);
  Serial.println("°");
  Serial.print("Servo 2: ");
  Serial.print(servo2_angle);
  Serial.println("°");
  Serial.print("[FLOW] ");
  Serial.print(current_flow_lmin, 2);
  Serial.println(" L/min");
  Serial.println("╚════════════╝\n");
}

void printHelp() {
  Serial.println("\n╔════ COMANDOS ════╗");
  Serial.println("PUMP,<pwm>       (0-255)");
  Serial.println("SERVO1,<angle>   (0-180)");
  Serial.println("SERVO2,<angle>   (0-180)");
  Serial.println("TIMECFG,t,ms,o,c");
  Serial.println("TIMESEQ,<pwm>");
  Serial.println("TIMESTOP");
  Serial.println("FLOW");
  Serial.println("FLOWCAL,<ppm>");
  Serial.println("STATUS / HELP");
  Serial.println("╚═══════════════╝\n");
}
