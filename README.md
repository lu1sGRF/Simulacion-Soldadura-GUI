# Soldadura-Simulacion-GUI

**Soldadura-Simulacion-GUI** es una interfaz intuitiva que facilita la simulación de procesos de soldadura. Desarrollada como una interfaz gráfica (GUI), permite a los usuarios gestionar archivos de entrada, configurar simulaciones con **CalculiX** y visualizar los resultados en **ParaView**.

---

## 🎥 Video de Demostración

[![Video de Demostración](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

---

## ✨ Características

- Gestión de archivos de entrada para simulaciones (carpetas automáticas `Input` y `Run`).
- Configuración rápida de ejecutables para CalculiX y ParaView.
- Ejecución de simulaciones con opción de generar logs.
- Conversión de resultados (`.frd`) a formatos compatibles con ParaView (`.vtu`).
- Visualización automatizada de resultados utilizando ParaView.
- Análisis del archivo `.inp` para determinar si es binario o ASCII.

---

## 📋 Requisitos Previos

1. **Python**: 3.8 o superior.
2. **Bibliotecas de Python**:
   - `customtkinter`
   - `flask`
   - Cualquier otra especificada en `requirements.txt`.
3. **Software adicional**:
   - **CalculiX**: Necesitas el ejecutable `ccx.exe`.
   - **ParaView**: Necesitas el ejecutable de ParaView para la visualización.

---

## 🛠️ Instalación

Sigue estos pasos para instalar y ejecutar la aplicación:

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/Soldadura-Simulacion-GUI.git
   cd Soldadura-Simulacion-GUI
