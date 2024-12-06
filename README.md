# Simulacion-Soldadura-GUI

**Soldadura-Simulacion-GUI** es una herramienta intuitiva para la simulación de procesos de soldadura. Utiliza una interfaz gráfica (GUI) que permite a los usuarios gestionar archivos de entrada, configurar simulaciones con **CalculiX** y visualizar los resultados en **ParaView**.

### 🎯 Propósito
La aplicación está dirigida a investigadores, estudiantes y profesionales en ingeniería mecánica y procesos térmicos. Su propósito es facilitar la simulación, análisis de resultados y conversión de formatos de salida, mejorando los flujos de trabajo en proyectos de simulación complejos.

---

## 🎥 Video de Demostración

Para ver cómo utilizar la herramienta, consulta el siguiente video de demostración:

[![Video de Demostración](https://img.youtube.com/vi/i02AnA2SZ4Y/maxresdefault.jpg)](https://www.youtube.com/watch?v=i02AnA2SZ4Y)

---

## ✨ Características

- **Interfaz gráfica fácil de usar**.
- **Gestión automática de carpetas** (`Input`, `Run` y `Results`) para simular y guardar datos.
- **Configuración automática de ejecutables** de **CalculiX** y **ParaView**.
- **Ejecución de simulaciones** con generación de logs.
- **Conversión automática** de archivos `.frd` a `.vtu`.
- **Visualización** de resultados con ParaView.

---

## 📦 Cómo Descargar y Usar

### 1. Descargar el ejecutable
- Ve a la sección **Releases** de este repositorio: [Releases](https://github.com/tu_usuario/Soldadura-Simulacion-GUI/releases).
- Descarga la última versión del archivo `.exe`.

### 2. Ejecutar la aplicación
- **No necesitas instalar Python ni dependencias**.
- Solo ejecuta el archivo `.exe` descargado.
- Sigue las instrucciones dentro de la aplicación para realizar tus simulaciones.

---

## 🛠️ Si deseas trabajar con el código fuente

### Requisitos
1. **Python**: 3.8 o superior.
2. **Bibliotecas de Python**:
   - `customtkinter`
   - `flask`
   - Otras incluidas en `requerimientos.txt`.
3. **Software adicional**:
   - **CalculiX**: El ejecutable `ccx.exe` se encuentra en la carpeta raíz de este repositorio.
   - **ParaView**: El ejecutable para visualizar los resultados se encuentra también en la carpeta raíz de este repositorio.

### Instalación del código fuente
1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/Soldadura-Simulacion-GUI.git
   cd Soldadura-Simulacion-GUI
