# GUI-Run-Calculix - Simulacion-Soldadura-GUI
Esta es una GUI intuitiva para la simulación de procesos de soldadura. Utiliza una interfaz gráfica (GUI) que permite a los usuarios gestionar archivos de entrada, configurar simulaciones con **CalculiX** y visualizar los resultados en **ParaView**.

### Propósito
La aplicación está dirigida a investigadores, estudiantes y profesionales en ingeniería mecánica y procesos térmicos. Su propósito es facilitar la simulación, análisis de resultados y conversión de formatos de salida, mejorando los flujos de trabajo en proyectos de simulación complejos.

---

## 🎥 Video de utilización de la interfaz visual de simulación de soldadura con software libre

Para ver cómo utilizar la interfaz, consulta el siguiente video donde se muestra desde la descarga, hasta la utilización de la interfaz completa:

[![Video de Comparación](https://img.youtube.com/vi/GXUdsil8EW0/maxresdefault.jpg)](https://www.youtube.com/watch?v=GXUdsil8EW0)

--

## ✨ Características de la interfaz

- **Interfaz gráfica fácil de usar**.
- **Gestión automática de carpetas** (`Input`, `Run` y `Results`) para simular y guardar datos.
- **Configuración automática de ejecutables** de **CalculiX** y **ParaView**.
- **Ejecución de simulaciones** con generación de logs o datos de la ejecución desde el CMD.
- **Conversión automática** de archivos `.frd` a `.vtu`.
- **Visualización** de resultados con ParaView.

---


## 🎥 Video de comparación entre la interfaz GUI-Run-Calculix y el solver PrePoMax

En este video se compara la funcionalidad y eficiencia de la GUI-Simulacion-Soldadura con el solver PrePoMax. Descubre cómo GUI-Simulacion-Soldadura ofrece una experiencia más personalizada y optimizada para procesos de soldadura.

[![Video de Comparación](https://img.youtube.com/vi/6xPa1QLKiuc/maxresdefault.jpg)](https://www.youtube.com/watch?v=6xPa1QLKiuc)

### 🛠️ Beneficios de utilizar GUI-Run-Calculix sobre PrePoMax

1. **Optimización para soldadura**:  
   GUI-Run-Calculix está diseñada específicamente para procesos de soldadura, mientras que PrePoMax es un entorno generalista que carece de herramientas específicas para este tipo de simulaciones.

2. **Gestión automatizada de carpetas**:  
   La GUI crea y organiza automáticamente las carpetas necesarias para la simulación (`Input`, `Run`, `Results`), lo que simplifica el flujo de trabajo y minimiza errores.

3. **Conversión directa de formatos**:  
   Integra un conversor que transforma archivos `.frd` a `.vtu` de forma automática, eliminando pasos adicionales para la visualización en **ParaView**.

4. **Análisis del archivo `.inp`**:  
   Analiza automáticamente el archivo de entrada para determinar si está en formato ASCII o binario, y brinda al usuario opciones basadas en este análisis.

5. **Interfaz gráfica intuitiva**:  
   Ofrece una GUI más amigable que evita la necesidad de comandos complejos en consola, algo que en PrePoMax puede requerir mayor conocimiento técnico.

6. **Ejecución simplificada**:  
   Permite configurar y ejecutar simulaciones directamente desde la interfaz, con opciones para visualizar el progreso en CMD o generar archivos de log.

7. **Flexibilidad de configuración**:  
   Facilita la configuración de los ejecutables de **CalculiX** y **ParaView**, asegurando compatibilidad y funcionalidad inmediata.

8. **Diseño portable**:  
   No requiere instalación de Python o dependencias adicionales, algo que reduce los problemas de compatibilidad en distintos sistemas.

Con GUI-Run-Calculix, los usuarios tienen una herramienta especializada, automatizada y lista para optimizar sus proyectos de simulación de soldadura.


---

## 📂 Estructura del Proyecto

La siguiente estructura muestra los principales directorios y archivos del proyecto:

## Código_fuente/
- `Interfaz.py`         # Código principal de la interfaz gráfica
- `LOGO_LF.ico`         # Ícono de la aplicación
- `extensiones.txt`     # Lista de extensiones soportadas
- `requerimientos.txt`  # Dependencias necesarias para ejecutar el proyecto

## Ejecutable_interfaz/
- `Ejemplo_basico/`     # Prueba básica y rapida para probar las funcionalidades de la interfaz
- `extensiones.txt`     # Lista de extensiones soportada
- `interfaz.exe`        # Ejecutable listo para usar
- `requerimientos.txt`  # Dependencias adicionales

## Librerias/ccx2paraview/
- `__init__.py`         # Inicialización del módulo
- `ccx2paraview.py`     # Conversor de resultados de CalculiX a ParaView

## Otros archivos
- `build_GUI/interfaz`      # Recursos generados de la interfaz
- `.gitignore`              # Archivos y carpetas a excluir del repositorio
- `LICENSE`                 # Licencia del proyecto
- `README.md`               # Documentación del proyecto


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
   - **CalculiX**: El ejecutable `ccx.exe` lo puedes encuentrar en este [github de CCX](https://github.com/PacoOMG2/Ccx-welding-simulation) en la carpeta llamada **Additive/02_Compiled/ccx/x64/install** se encuentra el ccxMKL.exe.
   - NOTA: Se recomienda descargar la carpeta completa del ccx/x64/install
   - **ParaView**: El ejecutable para visualizar los resultados se encuentra en su [Pagina oficial de descarga](https://www.paraview.org/download/).

### Instalación del código fuente
1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/lu1sGRF/Simulacion-Soldadura-GUI.git
   cd Soldadura-Simulacion-GUI
