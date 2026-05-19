# 🚀 GUÍA RÁPIDA DE INSTALACIÓN

> Para que puedas tener el proyecto funcionando en **5 minutos**

---

## 📋 Pre-requisitos

- ✅ Windows 10+ (o Linux/Mac)
- ✅ Python 3.10 o superior instalado
- ✅ ESP32-S3 DevKit (opcional si solo quieres ver la interfaz)
- ✅ Git instalado

---

## 🔧 Instalación Paso a Paso

### Paso 1: Clonar el Proyecto
```bash
git clone https://github.com/Santi4216/Control-Discreto-Tanques-.git
cd lab-control-Discreto
```

### Paso 2: Instalar Dependencias
```bash
cd python_app
pip install -r requirements.txt
```

### Paso 3: Ejecutar la Aplicación
```bash
python main.py
```

**¡Listo! 🎉 La aplicación debería abrirse.**

---

## 📁 Estructura Básica

```
lab-control-Discreto/
├── README.md ..................... 📖 Documentación principal
├── RESUMEN_EJECUTIVO.md ......... 👨‍💼 Para no-técnicos
├── GUIA_RAPIDA.md ............... 🚀 (Este archivo)
├── PINOUT_Y_CONEXIONES.md ....... 🔌 Esquema electrónico
├── CAMBIOS_ESTADISTICAS.md ...... 📊 Técnico
├── informe_lab2.tex ............. 📄 Informe formal
│
├── python_app/
│   ├── main.py .................. Iniciar aplicación aquí
│   ├── requirements.txt ......... Dependencias
│   ├── core/ .................... Lógica del sistema
│   ├── ui/ ...................... Interfaz gráfica
│   └── resources/ ............... Temas y estilos
│
└── arduino/
    └── 10_simplified_pump_servos/ Firmware para ESP32
```

---

## 🎮 Primer Uso

1. **Abre la aplicación**
   ```bash
   python main.py
   ```

2. **Ve a la pestaña "Control"**

3. **Prueba sin hardware:**
   - Los deslizadores funcionan aunque no esté conectado
   - Verás mensajes en la consola

4. **Si tienes hardware:**
   - Conecta el ESP32 por USB
   - La app detectará automáticamente el puerto
   - Prueba los botones de control

---

## 🐛 Solución de Problemas

### "No encuentra Python"
```bash
# Usa la ruta completa
C:\Python313\python.exe main.py
```

### "Falta PyQt6"
```bash
pip install PyQt6 --upgrade
```

### "No detecta el puerto USB"
- Asegúrate que el ESP32 esté conectado
- Ve a Administrador de dispositivos → Puertos COM
- Instala drivers de CH340 si es necesario

### "Error de permisos en Windows"
```bash
# Ejecuta PowerShell como Administrador
```

---

## 📊 Pestaña por Pestaña

### 🎮 Control
- Control manual de bomba y válvulas
- Para experimentar sin tiempos

### ⏱️ Timed Control
- Ingresa tiempos de llenado
- El sistema llena automáticamente
- Ve la precisión en tiempo real

### 📊 Statistics
- Histórico de todas las ejecuciones
- Desviaciones y análisis
- Exporta datos a CSV

### 📋 Logs
- Ver comandos enviados
- Timestamps exactos
- Debugging

### ⚙️ Device
- Seleccionar puerto COM
- Conexión/desconexión
- Estado del hardware

---

## 💡 Próximos Pasos

### Para Programadores
1. Modifica `python_app/ui/pages/` para agregar nuevas funciones
2. Edita `python_app/core/protocol.py` para cambiar comandos
3. Personaliza `python_app/resources/styles.qss` para el tema

### Para Ingenieros Electrónicos
1. Ve a `arduino/10_simplified_pump_servos/README.md`
2. Modifica los pines en `#define GPIO_xxx`
3. Ajusta velocidades y rangos de servos

### Para Análisis
1. Los datos se guardan en `python_app/logs/`
2. Son archivos CSV fáciles de importar a Excel/Python
3. Usa `pandas` para análisis avanzado

---

## 📞 Contacto y Soporte

- **GitHub:** https://github.com/Santi4216/Control-Discreto-Tanques-
- **Autor:** Santiago García
- **Carrera:** Ingeniería en Control - UMNG

---

## ✅ Checklist de Verificación

- [ ] Python instalado (`python --version`)
- [ ] Git instalado (`git --version`)
- [ ] Repositorio clonado
- [ ] Dependencias instaladas (`pip list | grep PyQt6`)
- [ ] Aplicación inicia sin errores
- [ ] Al menos una pestaña se abre correctamente

**Si todo está marcado ✓, ¡estás listo!**

---

## 🎓 Recursos Útiles

- [Documentación PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [ESP32 Arduino Core](https://docs.espressif.com/projects/arduino-esp32/en/latest/)
- [Python Serial](https://pyserial.readthedocs.io/)
- [Git Basics](https://git-scm.com/book/es/v2)

---

**Última actualización:** Mayo 2026

