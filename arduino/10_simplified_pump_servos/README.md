# Simplified Pump + Servos Control

**Versión actual con control por tiempos automático**

## Descripción
Código Arduino simplificado que elimina complejidades innecesarias:
- ❌ Ultrasónicos (HC-SR04)
- ❌ Sensor de flujo (YF-S401)
- ❌ PID complejo
- ❌ Logging CSV

✅ **Incluye:**
- Control PWM de bomba (0-255)
- Control de 2 servos para válvulas (0-180°)
- **Comandos UART simples**
- **Control secuencial automático por tiempos**
- LED indicador

## Instalación

1. Abre Arduino IDE
2. Ve a `File → Open` y selecciona `10_simplified_pump_servos.ino`
3. **Tools:**
   - Board: `ESP32-S3 Dev Module`
   - Port: Tu puerto COM
4. Click en **Upload**

## Comandos - Control Manual

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `PUMP,<pwm>` | Controlar bomba (0-255) | `PUMP,200` |
| `SERVO1,<ángulo>` | Servo 1 (0-180°) | `SERVO1,45` |
| `SERVO2,<ángulo>` | Servo 2 (0-180°) | `SERVO2,135` |
| `STOP` | Parar bomba | `STOP` |
| `STATUS` | Ver estado actual | `STATUS` |
| `HELP` | Menú de ayuda | `HELP` |

## Comandos - Control por Tiempos (NUEVO)

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `TIMECFG,tank,ms,open_°,close_°` | Configurar tanque | `TIMECFG,1,5000,45,135` |
| `TIMESEQ,<pwm>` | Iniciar secuencia automática | `TIMESEQ,200` |
| `TIMESTOP` | Detener secuencia | `TIMESTOP` |
| `TIMESTAT` | Ver configuración de tiempos | `TIMESTAT` |

## Ejemplos - Control Manual

```
PUMP,200       # Bomba 78%
SERVO1,45      # Servo 1 a 45°
SERVO2,135     # Servo 2 a 135°
STOP           # Parar bomba
```

## Ejemplos - Control por Tiempos

```
# Configurar tanques
TIMECFG,1,5000,45,135     # Tank 1: 5s fill, 45° abre, 135° cierra
TIMECFG,2,8000,45,135     # Tank 2: 8s fill, 45° abre, 135° cierra

# Iniciar secuencia
TIMESEQ,200                # Inicia con PWM 200 (78%)

# Resultado: Tank 1 llena 5s → Tank 2 llena 8s → Bomba se detiene automáticamente
```

## Parámetros por Defecto

- **Tank 1 Fill Time:** 10000 ms (10s)
- **Tank 2 Fill Time:** 8000 ms (8s)
- **Open Angle:** 45°
- **Close Angle:** 135°

## Especificaciones

- **Plataforma:** ESP32-S3 DevKit
- **Baudrate:** 115200
- **PWM Frequency:** 10 kHz
- **Motor PWM:** GPIO 17
- **Servo 1:** GPIO 18
- **Servo 2:** GPIO 19
- **LED Status:** GPIO 7

## Ver también

- `CONTROL_POR_TIEMPOS.md` - Documentación completa del sistema temporal
- `CAMBIOS_IMPLEMENTADOS.md` - Detalles técnicos de la implementación

✓ Bomba: 200/255 (78%)

SERVO1,90
✓ Servo 1: 90°

SERVO2,45
✓ Servo 2: 45°

STATUS
╔═══ ESTADO ACTUAL ═══╗
   Bomba: ENCENDIDA
   PWM: 200/255 (78%)
   Servo 1: 90°
   Servo 2: 45°
╚═══════════════════════╝
```

## Conexiones Hardware

```
ESP32-S3 → H-Bridge L298N
─────────────────────────
GPIO 17 (PWM)  → ENA
GPIO 15        → IN1
GPIO 16        → IN2

ESP32-S3 → Servos
──────────────────
GPIO 18 → Servo 1 (Señal PWM)
GPIO 19 → Servo 2 (Señal PWM)

Bomba: Motor 12V DC
Servos: 5V (alimentar desde fuente externa)
```

## Integración con Python

La interfaz Python puede enviar comandos como:
```python
serial_port.write(b"PUMP,150\r\n")     # Bomba al 59%
serial_port.write(b"SERVO1,45\r\n")    # Servo 1 a 45°
serial_port.write(b"SERVO2,135\r\n")   # Servo 2 a 135°
serial_port.write(b"STATUS\r\n")       # Pedir estado
```

## Ventajas

✓ **Código limpio** - Fácil de entender y modificar
✓ **Sin dependencias complejas** - Solo esenciales
✓ **Rápido** - Sin procesamiento innecesario
✓ **Debuggable** - Mensajes claros en Serial
✓ **Compatible con GUI Python** - Comandos simples

## Troubleshooting

### Motor no gira con PUMP,200+
- Verifica conexiones del H-Bridge
- Comprueba voltaje 12V en los terminales
- Intenta PUMP,255 (máximo)

### Los servos no responden
- Verifica que estén conectados a 5V
- Comprueba GPIO 18 y 19
- Los servos pueden estar fuera de rango (0-180°)

### No hay comunicación Serial
- Verifica velocidad 115200 baud
- Reconecta USB
- Intenta con otro puerto COM

## Notas
⚠️ Asegúrate de que los servos se alimenten con 5V y que la tierra esté conectada a todo el sistema (ESP32, H-Bridge, Servos, Motor).
