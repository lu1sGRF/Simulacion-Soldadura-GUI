# Simulacion-Soldadura-GUI

**Soldadura-Simulacion-GUI** es una herramienta intuitiva para la simulación de procesos de soldadura. Utiliza una interfaz gráfica (GUI) que permite a los usuarios gestionar archivos de entrada, configurar simulaciones con **CalculiX** y visualizar los resultados en **ParaView**.

### Propósito
La aplicación está dirigida a investigadores, estudiantes y profesionales en ingeniería mecánica y procesos térmicos. Su propósito es facilitar la simulación, análisis de resultados y conversión de formatos de salida, mejorando los flujos de trabajo en proyectos de simulación complejos.

---

## 🎥 Video de utilización de la interfaz visual de simulación de soldadura de software libre

Para ver cómo utilizar la interfaz, consulta el siguiente video donde se muestra desde la descarga, hasta la utilización de la interfaz completa:

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

## 📂 Estructura del Proyecto

Estructura del Proyecto
La siguiente estructura muestra los principales directorios y archivos del proyecto:

Código_fuente/
├── Interfaz.py         # Código principal de la interfaz gráfica
├── LOGO_LF.ico         # Ícono de la aplicación
├── extensiones.txt     # Lista de extensiones soportadas
└── requerimientos.txt  # Dependencias necesarias para ejecutar el proyecto

Ejecutable_interfaz/
└── Ejemplo_basico/
    ├── extensiones.txt     # Prueba básica de funcionalidades
    ├── interfaz.exe        # Ejecutable listo para usar
    └── requerimientos.txt  # Dependencias adicionales (si aplica)

Librerias/ccx2paraview/
├── __init__.py         # Inicialización del módulo
└── ccx2paraview.py     # Conversor de resultados de CalculiX a ParaView

build_GUI/interfaz      # Recursos generados de la interfaz
.gitignore              # Archivos y carpetas a excluir del repositorio
LICENSE                 # Licencia del proyecto
README.md               # Documentación del proyecto


--

## 📦 Cómo Descargar y Usar

### 1. Descargar
- Descarga este repositorio o solo la carpeta llamada [Ejecutable interfaz](https://github.com/lu1sGRF/Simulacion-Soldadura-GUI/tree/main/Ejecutable_intefaz).
- Ya descargada, descomprime la carpeta zip si fue el caso que descargaste el repositorio completo, si no es asi solo abre la carpeta **Ejecutable_interfaz**.

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
   - **CalculiX**: El ejecutable `ccx.exe` lo puedes encuentrar en este [github de CCX](https://github.com/PacoOMG2/Ccx-welding-simulation) en la carpeta llamada **ccx_compilado**.
   - **ParaView**: El ejecutable para visualizar los resultados se encuentra en su [Pagina oficial de descarga](https://www.paraview.org/download/).

### Instalación del código fuente
1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/lu1sGRF/Simulacion-Soldadura-GUI.git
   cd Soldadura-Simulacion-GUI
