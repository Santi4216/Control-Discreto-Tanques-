# 📸 GUÍA: CÓMO AGREGAR FOTOS AL README

> Si tienes capturas de pantalla de la interfaz, esquemas, o fotos del hardware, aquí te muestro cómo agregarlas.

---

## 🎯 Objetivo

Agregar imágenes reales (PNG, JPG) al README para que luzca más profesional.

---

## 📂 Paso 1: Crear Carpeta para Imágenes

En tu repositorio, crea una carpeta llamada `images/` o `screenshots/`:

```
lab-control-Discreto/
├── README.md
├── images/              ← NUEVA CARPETA
│   ├── interface_main.png
│   ├── statistics_view.png
│   ├── hardware_setup.jpg
│   └── circuit_diagram.png
├── python_app/
└── arduino/
```

---

## 📸 Paso 2: Agregar las Imágenes

### Opción A: Si tienes capturas de pantalla

1. **Abre la aplicación Python**
   ```bash
   cd python_app
   python main.py
   ```

2. **Toma capturas con:**
   - `Win + Shift + S` (Windows)
   - `Cmd + Shift + 4` (Mac)
   - `Print Screen` (Linux)

3. **Guarda como PNG en `images/`:**
   - `interface_main.png` - Pantalla principal
   - `statistics_view.png` - Gráficos
   - `device_settings.png` - Configuración

### Opción B: Si tienes fotos del hardware

1. **Toma fotos de:**
   - Placa ESP32-S3
   - Conexiones con protoboard
   - Bomba y servos
   - Componentes completos

2. **Guarda como JPG en `images/`:**
   - `hardware_overview.jpg`
   - `esp32_board.jpg`
   - `connections.jpg`

### Opción C: Exportar diagramas de diseño

- Si usaste KiCad o similar, exporta como PNG
- Si tienes esquemas en PDF, conviérte a PNG

---

## ✏️ Paso 3: Editar el README

Abre `README.md` y busca esta sección:

```markdown
<!-- DESCOMENTAR CUANDO TENGAS LAS FOTOS:

### 🖥️ Captura de Pantalla - Control Manual
![Interfaz Principal](screenshots/interface_main.png)
...

-->
```

Reemplaza `screenshots/` por `images/` y descomenta:

**ANTES:**
```markdown
<!-- COMENTADO
![Interfaz Principal](screenshots/interface_main.png)
-->
```

**DESPUÉS:**
```markdown
![Interfaz Principal](images/interface_main.png)
```

---

## 🎨 Ejemplo Completo

### Así se vería tu README:

```markdown
### 🖥️ Interfaz Gráfica (PyQt6 - Tema Oscuro)

#### Control Manual

![Interfaz Principal](images/interface_main.png)

*La interfaz incluye deslizadores para control en tiempo real,
indicadores de estado, y botones de acción.*

#### Estadísticas en Tiempo Real

![Estadísticas](images/statistics_view.png)

*Gráficos interactivos mostrando precisión, desviaciones,
y histórico de ejecuciones.*

### 🔌 Hardware del Proyecto

#### ESP32-S3 y Conexiones

![Hardware](images/hardware_setup.jpg)

*Placa de desarrollo ESP32-S3 con conexiones a bomba,
válvulas y LED indicador.*

#### Diagrama de Circuito

![Circuito](images/circuit_diagram.png)

*Esquema completo del sistema electrónico.*
```

---

## 🚀 Paso 4: Subir a GitHub

```bash
# Agregar imágenes
git add images/

# Commit
git commit -m "Add project screenshots and diagrams"

# Push
git push
```

---

## 💡 Tips para Mejores Imágenes

### 📐 Tamaño Recomendado
- **Ancho:** 800-1200px máximo
- **Formato:** PNG (para transparencia) o JPG (fotos)
- **Compresión:** Usa herramientas como TinyPNG para reducir

### 📸 Mejores Prácticas

1. **Toma limpio**
   - Buena iluminación
   - Sin objetos distractores
   - Fondo limpio

2. **Redimensiona si es necesario**
   ```bash
   # En Windows (usando PowerShell):
   [reflection.assembly]::LoadWithPartialName("System.Drawing")
   $img = [System.Drawing.Image]::FromFile("image.jpg")
   # Redimensiona a 1000px de ancho
   ```

3. **Agrega descripción debajo**
   ```markdown
   ![Descripción](ruta/imagen.png)
   *Aquí va la descripción de lo que se ve*
   ```

---

## 🎯 Qué Imágenes Agregar

### Imprescindibles (Nivel 1)
- [ ] Captura interfaz principal
- [ ] Captura modo automático
- [ ] Captura estadísticas

### Recomendadas (Nivel 2)
- [ ] Foto del ESP32-S3
- [ ] Foto de las conexiones
- [ ] Esquema de circuito (PNG)

### Opcionales (Nivel 3)
- [ ] Foto de la bomba
- [ ] Foto de los servos
- [ ] Foto de todo el setup

---

## 📱 Alternativas si No Tienes Fotos

Si no puedes tomar fotos, puedes:

1. **Mantener los diagramas ASCII** (que ya tiene el README)
2. **Usar emojis mejorados** para que luzca visual
3. **Agregar diagramas Mermaid** para flujos

Ejemplo Mermaid:

```markdown
graph TB
    A[Aplicación] --> B[ESP32-S3]
    B --> C[Bomba]
    B --> D[Servo 1]
    B --> E[Servo 2]
    C --> F[Tank 1]
    D --> F
    E --> G[Tank 2]
```

---

## ❌ Problemas Comunes

### "Las imágenes no se ven en GitHub"

**Solución:**
- Verifica que estén en la carpeta `images/`
- Usa rutas **relativas**: `images/photo.png`
- NO uses rutas absolutas: `C:/ruta/photo.png`

### "Las imágenes se ven muy grandes"

**Solución:**
```markdown
![Imagen pequeña](image.png){: width="400px"}
```

O en HTML:
```html
<img src="images/photo.png" width="500">
```

### "El archivo es muy pesado"

**Solución:**
1. Reduce resolución a 1024x768 máximo
2. Usa compresión en línea: https://tinypng.com
3. Convierte a PNG y luego comprime

---

## 📋 Checklist para Agregar Fotos

- [ ] Cree carpeta `images/`
- [ ] Tomé capturas de pantalla
- [ ] Redimensioné las imágenes
- [ ] Comprimí los archivos (si es necesario)
- [ ] Coloqué imágenes en `images/`
- [ ] Edité `README.md` con rutas correctas
- [ ] Probé que se ven en GitHub
- [ ] Hice commit y push
- [ ] Verifiqué en GitHub que se ven

---

## 🔗 Recursos Útiles

- **Compresión de imágenes:** https://tinypng.com
- **Editor de capturas:** https://screenshot.net
- **Diagrama online:** https://mermaid.live
- **Iconos:** https://www.flaticon.com
- **Colores:** https://coolors.co

---

## ✨ Ejemplos de READMEs Bonitos

Mira estos proyectos como inspiración:

- https://github.com/microsoft/vscode
- https://github.com/torvalds/linux
- https://github.com/facebook/react
- https://github.com/python/cpython

---

## 🎓 Siguiente Paso

Una vez que tengas las fotos:

1. Agrega imágenes
2. Actualiza README
3. Haz commit y push
4. **¡Tu portfolio se verá profesional!** 🎉

---

**¿Necesitas ayuda? Puedo:**
- Ayudarte a comprimir imágenes
- Ajustar tamaños si es necesario
- Editar el README con tus imágenes

