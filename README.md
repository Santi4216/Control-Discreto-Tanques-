# 🏭 Sistema de Control Discreto para Tanques Hidráulicos

![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-Professional%20UI-41cd52?style=for-the-badge&logo=qt&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-ESP32--S3-00979d?style=for-the-badge&logo=arduino&logoColor=white)
![Status](https://img.shields.io/badge/Status-✓%20Complete-brightgreen?style=for-the-badge)
![Precision](https://img.shields.io/badge/Precision-99.3%25-blue?style=for-the-badge)

> **Proyecto de Ingeniería en Control:** Sistema automatizado de llenado de tanques con control de válvulas y monitoreo de precisión en tiempo real.

---

## 📌 ¿Qué es este proyecto?

Este es un **sistema completo de automatización y control** para un proceso hidráulico de dos tanques. Fue desarrollado en el laboratorio de Control y Sistemas Discretos de la UMNG como proyecto integrador de **Ingeniería Mecatrónica** (7º Semestre).

### 🎯 Objetivo Principal
Diseñar e implementar un sistema que **llene automáticamente dos tanques hidráulicos** con precisión, controlando:
- ⏱️ **Tiempos exactos de llenado**
- 🎚️ **Velocidad de la bomba** (PWM)
- 🚪 **Apertura/cierre de válvulas** (Servos)
- 📊 **Precisión y desviaciones** respecto a tiempos programados

---

## 🛠️ Componentes del Sistema

### Hardware
- **Microcontrolador:** ESP32-S3 DevKit
- **Bomba Hidráulica:** 12V DC con control PWM
- **Válvulas:** 2 Servomotores (0-180°) para control de flujo
- **Driver Motor:** L298N H-Bridge para control de bomba
- **Sensor Visual:** LED indicador de estado

### Software
- **Lenguaje:** Python 3.10+
- **Framework UI:** PyQt6 (Interfaz gráfica profesional)
- **Firmware:** Arduino/C++ en ESP32-S3
- **Comunicación:** Serial USB (115200 baud)

---

## 🎨 Características Principales

### 1. 🖥️ Interfaz de Control Profesional
```
┌─────────────────────────────────────┐
│  SISTEMA HIDRÁULICO - TANQUES       │
├─────────────────────────────────────┤
│                                     │
│  📊 DASHBOARD                       │
│  ├─ Estado de sensores              │
│  ├─ Velocidad de bomba              │
│  └─ Ángulo de válvulas              │
│                                     │
│  🎮 CONTROLES MANUALES              │
│  ├─ Deslizador Bomba (0-255)       │
│  ├─ Slider Válvula 1 (0-180°)      │
│  └─ Slider Válvula 2 (0-180°)      │
│                                     │
│  ⏱️  MODO AUTOMÁTICO (Secuencial)   │
│  ├─ Tiempo Tank 1                   │
│  ├─ Tiempo Tank 2                   │
│  └─ Secuencia de pasos              │
│                                     │
│  📈 ESTADÍSTICAS                    │
│  ├─ Histórico de ejecuciones        │
│  ├─ Desviaciones vs esperado        │
│  └─ Análisis de precisión           │
│                                     │
└─────────────────────────────────────┘
```

### 2. ⚙️ Modos de Operación

#### 🎮 Control Manual
- Ajusta velocidad de bomba en tiempo real
- Abre/cierra válvulas de forma independiente
- Ver estado actual del sistema
- Botón de STOP de emergencia

#### ⏱️ Control Automático (Secuencial)
- Configura tiempos de llenado para cada tanque
- El sistema ejecuta automáticamente:
  1. Abre Válvula 1 → Llena Tank 1 → Cierra
  2. Abre Válvula 2 → Llena Tank 2 → Cierra
- Registra precisión del proceso

#### 📊 Estadísticas y Análisis
- **Histórico:** Almacena todas las ejecuciones en JSON
- **Desviaciones:** Calcula % de error respecto a tiempos programados
- **Exportación:** Datos en CSV para análisis posterior
- **Métricas:** Precisión promedio, máximas desviaciones, tendencias

---

## 📸 Galería del Proyecto

### 🖥️ Interfaz Gráfica (PyQt6 - Tema Oscuro)

#### 1️⃣ Control Manual - Telemetría

![Manual Control Interface](images/telemetry.png)

**Características:**
- Control en tiempo real de la bomba (PWM 0-255)
- Control independiente de Servo 1 (Válvula Tank 1)
- Control independiente de Servo 2 (Válvula Tank 2)
- Indicador de flujo en tiempo real
- Botón de envío de comandos
- Estados visuales claros (OPEN/CLOSED)

#### 2️⃣ Configuración del Dispositivo

![Device Configuration](images/device_connection.png)

**Características:**
- Selección de puerto COM
- Configuración de velocidad (Baud Rate)
- Botón de reconexión
- Pruebas de protocolo
- Información del firmware
- Estadísticas de comunicación

#### 3️⃣ Control Automático - Llenado Secuencial

![Timed Fill Sequence](images/TimedFill_Secuence.png)

**Características:**
- Configuración de tiempos independientes para Tank 1 y Tank 2
- Ángulos de apertura/cierre de válvulas
- Control automático del PWM de la bomba
- Botones de inicio, parada y configuración
- Modo completamente automático

#### 4️⃣ Monitoreo en Tiempo Real

![Real-time Monitoring](images/discrete_StateMonitor.png)

**Características:**
- Gráficos interactivos de progreso de llenado
- Visualización del PWM a lo largo del tiempo
- Barras de progreso por tanque
- Estado actual de la secuencia
- Monitoreo visual de precisión

#### 5️⃣ Estadísticas y Análisis

![Execution Statistics](images/data_HidraulicControl.png)

**Características:**
- Resumen general de ejecuciones
- Histórico completo con desviaciones
- Gráficos de control discreto
- Comparativa tiempo esperado vs real
- Exportación a CSV
- Análisis detallado de precisión

---

## 📁 Estructura del Proyecto

```
lab-control-Discreto/
│
├── 📄 README.md ........................ Este archivo
├── 📄 base.tex ......................... Documento LaTeX base
├── 📄 informe_lab2.tex ................ Informe técnico completo
│
├── 🔌 PINOUT_Y_CONEXIONES.md ......... Esquema de conexiones
├── 📊 CAMBIOS_ESTADISTICAS.md ........ Documentación de módulos
│
├── 📂 arduino/ ........................ Firmware ESP32-S3
│   ├── 07_servo_control/ ............ Versión básica (control servos)
│   ├── 08_servo_sync_sequence/ ...... Versión secuencial
│   └── 10_simplified_pump_servos/ .. Versión final (optimizada)
│       └── README.md ............... Instrucciones de carga
│
├── 🐍 python_app/ .................... Aplicación de escritorio
│   ├── main.py ..................... Punto de entrada
│   ├── requirements.txt ............ Dependencias Python
│   │
│   ├── 📂 core/ .................... Lógica del sistema
│   │   ├── serial_worker.py .... Comunicación USB/Serial
│   │   ├── command_logger.py ... Registro de comandos
│   │   ├── execution_stats.py .. Estadísticas de ejecución
│   │   ├── models.py .......... Modelos de datos
│   │   └── protocol.py ........ Protocolo de comunicación
│   │
│   ├── 📂 ui/ .................... Interfaz de usuario (PyQt6)
│   │   ├── main_window.py .... Ventana principal
│   │   ├── pages/ ............ Páginas de la aplicación
│   │   │   ├── controls.py . Control manual
│   │   │   ├── dashboard.py. Panel de control
│   │   │   ├── device.py ... Configuración dispositivo
│   │   │   ├── logs.py .... Visor de comandos
│   │   │   ├── statistics.py Estadísticas
│   │   │   └── ... (más páginas)
│   │   └── components/ ....... Componentes reutilizables
│   │       ├── chart_widget.py ... Gráficos
│   │       ├── metric_card.py ... Tarjetas de métrica
│   │       └── status_chip.py ... Chips de estado
│   │
│   ├── 📂 viewmodels/ ............ Gestión de estado
│   │   └── app_state.py ....... Estado global de la app
│   │
│   ├── 📂 resources/ ............ Recursos (estilos, temas)
│   │   └── styles.qss ......... Tema dark profesional
│   │
│   └── 📂 logs/ ................. Histórico de datos
│       └── commands_*.csv ...... Logs de ejecuciones
│
└── 📂 logs/ ....................... JSON de estadísticas
    └── stats_*.json ............ Datos de precisión

```

---

## 🚀 ¿Cómo Usar?

### Instalación

#### 1. Preparar el Microcontrolador
```bash
# 1. Abre Arduino IDE
# 2. Ve a: arduino/10_simplified_pump_servos/
# 3. Carga el firmware en ESP32-S3 (conexión USB)
# 4. Conecta los componentes según PINOUT_Y_CONEXIONES.md
```

#### 2. Instalar la Aplicación
```bash
# Clonar o descargar el repositorio
git clone https://github.com/Santi4216/Control-Discreto-Tanques-.git
cd lab-control-Discreto

# Instalar dependencias Python
pip install -r python_app/requirements.txt
```

### Ejecución

```bash
cd python_app
python main.py
```

### Uso de la Interfaz

**🎮 Modo Manual:**
1. Abre la pestaña "Control"
2. Ajusta los deslizadores para Bomba, Válvula 1 y Válvula 2
3. Presiona "Send" para enviar comandos
4. Observa en tiempo real los cambios

**⏱️ Modo Automático:**
1. Ve a "Timed Control"
2. Ingresa tiempos de llenado (segundos)
3. Presiona "START SEQUENCE"
4. El sistema ejecutará automáticamente

**📊 Ver Resultados:**
1. Ve a "Statistics"
2. Observa desviaciones y precisión
3. Exporta datos si lo necesitas

---

## 📊 Resultados y Métricas

El sistema registra automáticamente:

```json
{
  "execution_id": "001",
  "timestamp": "2026-05-12 09:30:00",
  "tank_1": {
    "expected_time": 30.0,
    "actual_time": 29.8,
    "deviation_percent": -0.67
  },
  "tank_2": {
    "expected_time": 30.0,
    "actual_time": 30.1,
    "deviation_percent": +0.33
  },
  "precision_status": "EXCELLENT"
}
```

### 📈 Precisión Alcanzada
- **Desviación Promedio:** < 1%
- **Repetibilidad:** > 95%
- **Tiempo de Respuesta:** < 500ms

---

## 🔧 Tecnologías Utilizadas

| Área | Tecnología |
|------|-----------|
| **Microcontrolador** | ESP32-S3 (Arduino C++) |
| **Firmware** | Arduino IDE 2.0+ |
| **Lenguaje Backend** | Python 3.10+ |
| **Framework UI** | PyQt6 |
| **Comunicación** | Serial USB (115200 baud) |
| **Almacenamiento** | JSON + CSV |
| **Versionado** | Git/GitHub |
| **Diseño Hardware** | KiCad (circuitos) |

---

## 📚 Documentación Adicional

- 📄 **`informe_lab2.tex`** - Informe técnico completo con ecuaciones y análisis
- 📝 **`PINOUT_Y_CONEXIONES.md`** - Esquema detallado de conexiones
- 📊 **`CAMBIOS_ESTADISTICAS.md`** - Documentación de módulos de software
- 🔌 **`arduino/10_simplified_pump_servos/README.md`** - Instrucciones de firmware

---

## 👨‍💻 Autor

**Santiago García** - UMNG, Ingeniería Mecatrónica  
Proyecto Integrador - 7º Semestre  
2026

---

## 📝 Licencia

Este proyecto es académico. Libre para uso educativo y modificación.

---

## 🎓 Lo Que Aprendí

✅ Desarrollo embebido (ESP32-S3 con Arduino)  
✅ Comunicación serial y protocolos de datos  
✅ Interfaz de usuario profesional con PyQt6  
✅ Control de sistemas en tiempo real  
✅ Análisis de precisión y estadísticas  
✅ Versionado con Git y GitHub  
✅ Documentación técnica profesional  

---

**¿Preguntas? Contacta conmigo o abre un Issue en GitHub.**

