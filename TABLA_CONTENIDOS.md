# 📑 ÍNDICE DE DOCUMENTACIÓN

> Guía de navegación para entender rápidamente qué documentos leer según tu perfil

---

## 👤 ¿Quién Eres? Elige tu Ruta

### 🧑‍💼 Reclutador / Manager (5 min de lectura)
**Tu objetivo:** Entender rápidamente de qué trata el proyecto

📖 **Lee esto:**
1. [`README.md`](README.md) - Introducción y características
2. [`RESUMEN_EJECUTIVO.md`](RESUMEN_EJECUTIVO.md) - Explicación ejecutiva
3. Mira el código en `python_app/` - Verifica calidad

**⏱️ Tiempo recomendado:** 5-10 minutos  
**✅ Resultado:** Entiendes qué hizo y por qué importa

---

### 👨‍💻 Programador / Desarrollador (30 min)
**Tu objetivo:** Entender la arquitectura y el código

📖 **Lee esto:**
1. [`GUIA_RAPIDA.md`](GUIA_RAPIDA.md) - Instala y ejecuta
2. [`README.md`](README.md) - Sección "Estructura del Proyecto"
3. [`CAMBIOS_ESTADISTICAS.md`](CAMBIOS_ESTADISTICAS.md) - Módulos técnicos
4. Explora `python_app/` - Código bien documentado

**⏱️ Tiempo recomendado:** 20-30 minutos  
**✅ Resultado:** Sabes cómo está construido y cómo contribuir

---

### 🔌 Ingeniero Electrónico / Hardware (20 min)
**Tu objetivo:** Entender circuitos, conexiones y firmware

📖 **Lee esto:**
1. [`PINOUT_Y_CONEXIONES.md`](PINOUT_Y_CONEXIONES.md) - Esquema visual
2. `arduino/10_simplified_pump_servos/README.md` - Instrucciones de firmware
3. [`README.md`](README.md) - Sección "Componentes"
4. Revisa `arduino/10_simplified_pump_servos/*.ino` - Código del microcontrolador

**⏱️ Tiempo recomendado:** 15-20 minutos  
**✅ Resultado:** Sabes cómo está conectado y cómo reprogramar

---

### 📊 Analista de Datos / Científico (15 min)
**Tu objetivo:** Entender métricas, precisión y análisis

📖 **Lee esto:**
1. [`CAMBIOS_ESTADISTICAS.md`](CAMBIOS_ESTADISTICAS.md) - Sistema de stats
2. Revisa `python_app/logs/` - Datos en CSV y JSON
3. [`README.md`](README.md) - Sección "Resultados y Métricas"

**⏱️ Tiempo recomendado:** 10-15 minutos  
**✅ Resultado:** Entiendes cómo se capturan y analizan datos

---

### 🎓 Estudiante / Aprendiz (45 min)
**Tu objetivo:** Aprender todo de principio a fin

📖 **Lee esto (en orden):**
1. [`RESUMEN_EJECUTIVO.md`](RESUMEN_EJECUTIVO.md) - Visión general
2. [`README.md`](README.md) - Descripción completa
3. [`GUIA_RAPIDA.md`](GUIA_RAPIDA.md) - Instala y experimenta
4. [`PINOUT_Y_CONEXIONES.md`](PINOUT_Y_CONEXIONES.md) - Aprende electrónica
5. Explora el código de `python_app/` - Aprende a programar
6. Lee `informe_lab2.tex` - Teoría en profundidad

**⏱️ Tiempo recomendado:** 45-60 minutos  
**✅ Resultado:** Comprendes completamente el proyecto y aprendes nuevas habilidades

---

## 📂 Mapa de Archivos

```
lab-control-Discreto/
│
├── 📄 README.md ........................... ⭐ EMPEZA AQUÍ
│   └─ Descripción completa, características, tecnologías
│
├── 📄 RESUMEN_EJECUTIVO.md ............... 👨‍💼 Para no-técnicos
│   └─ Explicación simple, "por qué importa"
│
├── 📄 GUIA_RAPIDA.md .................... 🚀 Instalar y ejecutar
│   └─ 5 minutos para tener funcionando
│
├── 📄 TABLA_CONTENIDOS.md ............... 📑 (Este archivo)
│   └─ Navega según tu perfil
│
├── 📄 PINOUT_Y_CONEXIONES.md ........... 🔌 Esquema electrónico
│   └─ Hardware, circuitos, GPIO
│
├── 📄 CAMBIOS_ESTADISTICAS.md .......... 📊 Especificación técnica
│   └─ Módulos, clases, métodos
│
├── 📄 informe_lab2.tex ................. 📋 Informe formal
│   └─ Teoría, ecuaciones, análisis académico
│
├── 🐍 python_app/ ....................... Código fuente Python
│   ├── main.py ..................... Ejecutable principal
│   ├── core/ ....................... Lógica y comunicación
│   ├── ui/ ......................... Interfaz gráfica (PyQt6)
│   ├── viewmodels/ ................. Gestión de estado
│   └── resources/ .................. Temas y estilos
│
├── 🔌 arduino/ .......................... Firmware ESP32
│   └── 10_simplified_pump_servos/
│       ├── *.ino ................... Código C++
│       └── README.md ............... Instrucciones
│
└── 📂 logs/ ............................ Histórico de datos
    └── stats_*.json .................. Ejecuciones guardadas
```

---

## 🎯 Preguntas Frecuentes: ¿Qué Documento Leo?

| Pregunta | Documento |
|----------|-----------|
| "¿Qué es este proyecto?" | [`README.md`](README.md) |
| "¿Cómo lo instalo?" | [`GUIA_RAPIDA.md`](GUIA_RAPIDA.md) |
| "¿Cómo está conectado?" | [`PINOUT_Y_CONEXIONES.md`](PINOUT_Y_CONEXIONES.md) |
| "¿Cómo es el código?" | [`CAMBIOS_ESTADISTICAS.md`](CAMBIOS_ESTADISTICAS.md) |
| "¿Cuál es la teoría?" | [`informe_lab2.tex`](informe_lab2.tex) |
| "¿Por qué es importante?" | [`RESUMEN_EJECUTIVO.md`](RESUMEN_EJECUTIVO.md) |
| "¿Qué carpeta veo primero?" | Revisa [`TABLA_CONTENIDOS.md`](TABLA_CONTENIDOS.md) (aquí) |
| "¿Cómo hago cambios?" | Lee código en `python_app/` |
| "¿Cómo añado funciones?" | Lee `python_app/ui/pages/` |
| "¿Cómo modifico hardware?" | Lee `arduino/` |

---

## 🚦 Flujo de Lectura Recomendado

```
                    ┌──────────────────┐
                    │ Alguien nuevo    │
                    └────────┬─────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
        ┌──────────────┐ ┌──────────┐ ┌──────────────┐
        │ No-técnico   │ │Developer │ │Hardware Eng. │
        │ (Manager)    │ │(Prog.)   │ │(Electrónica) │
        └──────┬───────┘ └────┬─────┘ └──────┬───────┘
               │              │              │
        README│ RESUMEJ       │              │
            ──┼──           │ README        │ PINOUT
               │            │ + CODE      │ + ARDUINO
               │            │              │
        ┌──────┴──────┬─────┴────────┬─────┴────────┐
        │             │              │              │
        ▼             ▼              ▼              ▼
    Entiende    Contribuye      Maneja          Reprograma
    Proyecto    Código          Hardware         Firmware
```

---

## 💡 Consejos de Lectura

### Para Reclutadores
- ✅ Lee solo **README + RESUMEN_EJECUTIVO** (10 min)
- ✅ Luego abre GitHub y mira la estructura
- ✅ Si te interesa, pide una demo

### Para Desarrolladores
- ✅ Empieza con **GUIA_RAPIDA** (instala localmente)
- ✅ Luego lee **estructura** en README
- ✅ Explora `python_app/` con tu editor favorito
- ✅ Lee docstrings en el código

### Para Ingenieros
- ✅ Ve directo a **PINOUT** (esquema)
- ✅ Luego **arduino/README.md** (firmware)
- ✅ Revisa `informe_lab2.tex` para teoría

### Para Estudiantes
- ✅ Lee **RESUMEN** primero (contexto)
- ✅ Luego **README** (completo)
- ✅ Luego instala con **GUIA_RAPIDA**
- ✅ Experimenta con el código
- ✅ Lee **informe_lab2.tex** (profundidad)

---

## 📚 Orden Sugerido Completo

1. ⭐ Este archivo (TABLA_CONTENIDOS.md)
2. 📖 [README.md](README.md) - Visión general
3. 🚀 [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Instalación
4. 👨‍💼 [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - Contexto
5. 🔌 [PINOUT_Y_CONEXIONES.md](PINOUT_Y_CONEXIONES.md) - Hardware
6. 📊 [CAMBIOS_ESTADISTICAS.md](CAMBIOS_ESTADISTICAS.md) - Código
7. 📋 [informe_lab2.tex](informe_lab2.tex) - Teoría
8. 💻 Explora `/python_app` - Código fuente
9. 🔧 Explora `/arduino` - Firmware
10. 📂 Revisa `/logs` - Datos capturados

---

## 🎯 Objetivo Final

**Después de leer estos documentos, deberías poder:**

- ✅ Explicar el proyecto a cualquiera
- ✅ Instalar y ejecutar la aplicación
- ✅ Entender la arquitectura completa
- ✅ Modificar el código si lo necesitas
- ✅ Reprogramar el microcontrolador
- ✅ Analizar los datos capturados
- ✅ Presentarlo en entrevistas de trabajo

---

## 🔗 Enlaces Rápidos

- **GitHub Repo:** https://github.com/Santi4216/Control-Discreto-Tanques-
- **Autor:** Santiago García
- **Universidad:** UMNG
- **Carrera:** Ingeniería en Control
- **Semestre:** 8vo
- **Año:** 2026

---

**Última actualización:** Mayo 2026

