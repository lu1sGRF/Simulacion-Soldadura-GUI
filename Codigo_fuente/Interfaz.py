import os
import shutil
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox, Menu, Toplevel, Listbox, Button
from flask import json
from threading import Thread

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue") 

class AppSimulacionSoldadura:
    def guardar_ruta(self, archivo, ruta):
        with open(archivo, 'w') as file:
            json.dump({'ruta': ruta}, file)

    def cargar_ruta_guardada(self, archivo):
        if os.path.exists(archivo):
            with open(archivo, 'r') as file:
                datos = json.load(file)
                return datos.get('ruta', None)
        return None

    def centrar_ventana(self):
        self.raiz.update_idletasks()

        # Obtén el tamaño de la ventana y de la pantalla
        ancho_ventana = self.raiz.winfo_width()
        alto_ventana = self.raiz.winfo_height()
        ancho_pantalla = self.raiz.winfo_screenwidth()
        alto_pantalla = self.raiz.winfo_screenheight()

        # Calcula la posición para centrar
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2
        self.raiz.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")


    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulación de Procesos de Soldadura con CalculiX")
        self.raiz.geometry("600x700")
        self.raiz.resizable(False, False)
        self.centrar_ventana()

        # Inicializar variables
        self.ruta_ejecutable_ccx = self.cargar_ruta_guardada('calculix_path.json')
        self.ruta_paraview = self.cargar_ruta_guardada('paraview_path.json')
        self.ruta_carpeta_padre = None
        self.proceso_en_ejecucion = False
        self.proceso = None
        self.ventana_modificar = None

        self.crear_menu()

        self.crear_widgets() 

    def crear_menu(self):
        menubar = Menu(self.raiz)
        self.raiz.configure(menu=menubar)

        # Menú de opciones
        menu_opciones = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=menu_opciones)
        menu_opciones.add_command(label="Salir", command=self.cerrar_interfaz)
        menu_opciones.add_command(label="Abrir Carpeta Padre", command=self.abrir_carpeta_padre)
        menu_opciones.add_command(label="Instrucciones", command=self.mostrar_instrucciones)  # Nueva opción

        # Menú de configuraciones
        menu_configuraciones = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configuraciones", menu=menu_configuraciones)
        menu_configuraciones.add_command(label="Ejecutable de CalculiX", command=self.seleccionar_ejecutable_ccx)
        menu_configuraciones.add_command(label="Ejecutable de ParaView", command=self.seleccionar_ejecutable_paraview)
        

    def crear_widgets(self):
        # Título principal
        titulo_principal = ctk.CTkLabel(self.raiz, text="Simulación de Procesos de Soldadura", font=("Arial", 30, "bold"))
        titulo_principal.pack(pady=20)

        # Sección: PASO 1 - Archivo de Entrada
        marco_entrada = ctk.CTkFrame(self.raiz); marco_entrada.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(marco_entrada, text="PASO 1: SELECCIÓN DE ARCHIVOS", font=("Arial", 15, "bold")).pack(anchor="center", pady=10)

        self.etiqueta_ruta = ctk.CTkLabel(marco_entrada, text="Ruta: No seleccionada", font=("Arial", 15, "bold"))
        self.etiqueta_ruta.pack(anchor="w", pady=5)

        frame_botones = ctk.CTkFrame(marco_entrada)
        frame_botones.pack(padx=10, pady=5, fill="x")

        self.boton_carpeta_padre = ctk.CTkButton(frame_botones, text="Seleccionar Carpeta Padre",font=("Arial", 13, "bold"), command=self.seleccionar_carpeta_padre, width=200, height=40)
        self.boton_carpeta_padre.grid(row=0, column=0, padx=10, pady=5)

        self.boton_archivos_simulacion = ctk.CTkButton(frame_botones, text="Seleccionar Archivos para la Simulación",font=("Arial", 12, "bold"), command=self.seleccionar_archivos_simulacion,width=200, height=40)
        self.boton_archivos_simulacion.grid(row=0, column=1, padx=10, pady=5)

        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        self.etiqueta_cantidad_archivos_input = ctk.CTkLabel(marco_entrada, text="Cantidad de archivos en la carpeta Input: 0", font=("Arial", 15, "bold"))
        self.etiqueta_cantidad_archivos_input.pack(anchor="center", pady=5)
        self.etiqueta_inp = ctk.CTkLabel(marco_entrada, text="Inp Selecionado: No seleccionado", font=("Arial", 15, "bold"))
        self.etiqueta_inp.pack(anchor="center", pady=5)

        self.boton_inp = ctk.CTkButton(marco_entrada, text="Seleccionar Archivo .inp",font=("Arial", 15, "bold"),command=self.seleccionar_archivo_inp, width=200, height=40)
        self.boton_inp.pack(pady=5)

        self.etiqueta_estado_analisis = ctk.CTkLabel(marco_entrada, text="Estado del análisis del inp: Sin iniciar", font=("Arial", 15, "bold"), text_color="gray")
        self.etiqueta_estado_analisis.pack(anchor="center", pady=5)

        # Sección: PASO 2 - Simulación
        marco_simulacion = ctk.CTkFrame(self.raiz)
        marco_simulacion.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(marco_simulacion, text="PASO 2: Simulación", font=("Arial", 15, "bold")).pack(anchor="center", pady=5)
        self.boton_simulacion = ctk.CTkButton(marco_simulacion,text="Ejecutar Simulación", font=("Arial", 13, "bold"),command=self.ejecutar_simulacion,width=200,height=40,text_color="white")
        self.boton_simulacion.pack(pady=5)

        self.etiqueta_estado_simulacion = ctk.CTkLabel(marco_simulacion,text="Estado de la simulación: (Sin iniciar)",font=("Arial", 15, "bold"), text_color="gray")
        self.etiqueta_estado_simulacion.pack(pady=10)

        # Sección: PASO 3 - Resultados y Conversión
        marco_resultados = ctk.CTkFrame(self.raiz)
        marco_resultados.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(marco_resultados, text="PASO 3: CONVERSIÓN Y RESULTADOS", font=("Arial", 15, "bold")).pack(anchor="center", pady=5)
        self.boton_convertir = ctk.CTkButton(marco_resultados, text="Convertidor de FRD a VTU", command=self.convertir_frd_a_vtu_async,width=200,height=40,text_color="white")
        self.boton_convertir.pack(pady=5)

        self.boton_mostrar_resultados = ctk.CTkButton(marco_resultados, text="Mostrar Resultados en ParaView", font=("Arial", 13, "bold"), command=self.mostrar_resultados_paraview, width=200, height=40)
        self.boton_mostrar_resultados.pack(pady=5)

        self.etiqueta_estado_conversion = ctk.CTkLabel(marco_resultados,text="Estado del convertir: (Sin iniciar)",font=("Arial", 15, "bold"), text_color="gray")
        self.etiqueta_estado_conversion.pack(pady=10)

    def verificar_permisos_carpeta(self, ruta):
        # Verifica si la carpeta tiene permisos de escritura, al igual que si la carpeta no existe, verifica si se puede crear.
        if not os.path.exists(ruta):
            try:
                os.makedirs(ruta)  
                os.rmdir(ruta)  
                return True
            except PermissionError:
                return False
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo verificar los permisos de la carpeta:\n\n{str(e)}")
                return False
        else:
            if os.access(ruta, os.W_OK): 
                return True
            else:
                return False


    def abrir_carpeta_padre(self):
        if self.ruta_carpeta_padre:
            if os.path.exists(self.ruta_carpeta_padre):
                # Abrir la carpeta padre
                os.startfile(self.ruta_carpeta_padre) if os.name == 'nt' else subprocess.call(['open', self.ruta_carpeta_padre])
            else:
                messagebox.showwarning("Advertencia", "No se pudo encontrar la carpeta padre.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una carpeta padre primero.")

    def seleccionar_carpeta_padre(self):
        while True:
            ruta = filedialog.askdirectory(title="Seleccione la Carpeta Padre")
            if ruta:
                respuesta = messagebox.askyesno(
                    "Confirmar Carpeta",
                    f"¿Está seguro de que desea usar esta carpeta como base para la simulación?\n\n{ruta}\n\n"
                    f"Se creará una nueva carpeta llamada 'Simulacion' en este directorio."
                )
                if respuesta:
                    # Crear la carpeta principal de simulación
                    carpeta_simulacion = os.path.join(ruta, "Simulacion")
                    try:
                        if not os.path.exists(carpeta_simulacion):
                            os.makedirs(carpeta_simulacion)
                            messagebox.showinfo(
                                "Carpeta Creada",
                                f"Se creó la carpeta principal 'Simulacion' en:\n\n{carpeta_simulacion}"
                            )
                        else:
                            messagebox.showinfo(
                                "Carpeta Existente",
                                f"La carpeta principal 'Simulacion' ya existe en el directorio seleccionado."
                            )

                        # Crear la subcarpeta "Input" dentro de la carpeta de simulación
                        input_folder = os.path.join(carpeta_simulacion, "Input")
                        if not os.path.exists(input_folder):
                            os.makedirs(input_folder)
                            messagebox.showinfo(
                                "Carpeta Creada",
                                f"La subcarpeta 'Input' se creó en:\n\n{input_folder}"
                            )
                        else:
                            messagebox.showinfo(
                                "Carpeta Existente",
                                f"La subcarpeta 'Input' ya existe en la carpeta 'Simulacion'."
                            )

                        # Contar los archivos existentes en la carpeta Input
                        cantidad_archivos_input = len([
                            f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))
                        ])

                        # Actualizar el label con la cantidad de archivos en Input
                        self.etiqueta_cantidad_archivos_input.configure(
                            text=f"Cantidad de archivos en la carpeta Input: {cantidad_archivos_input}"
                        )

                        # Establecer la ruta principal de la carpeta de simulación
                        self.ruta_carpeta_padre = carpeta_simulacion
                        self.etiqueta_ruta.configure(text=f"Ruta: {carpeta_simulacion}")
                        break

                    except Exception as e:
                        messagebox.showerror(
                            "Error",
                            f"Se produjo un error al crear las carpetas necesarias:\n\n{e}"
                        )
                        return
                else:
                    messagebox.showinfo("Seleccionar Carpeta", "Por favor seleccione otra carpeta.")
            else:
                break

    def seleccionar_archivos_simulacion(self):
        if not self.ruta_carpeta_padre:
            messagebox.showerror("Error", "Seleccione primero una Carpeta Padre para continuar.")
            return

        input_folder = os.path.join(self.ruta_carpeta_padre, "Input")
        extensiones_path = os.path.join(os.getcwd(), "extensiones.txt")

        # Leer las extensiones permitidas desde el archivo "extensiones.txt"
        if os.path.exists(extensiones_path):
            with open(extensiones_path, "r") as file:
                extensiones = [line.strip() for line in file if line.strip()]

            # Crear un filtro combinado y filtros individuales para las extensiones
            filtro_combinado = f"Archivos de Simulación ({'; '.join([f'*{ext}' for ext in extensiones])})"
            filetypes = [(filtro_combinado, ";".join([f"*{ext}" for ext in extensiones]))]
            filetypes.extend([(f"Archivos {ext.upper()}", f"*{ext}") for ext in extensiones])
        else:
            messagebox.showerror("Error", "No se encontró el archivo 'extensiones.txt'.")
            return

        archivos = filedialog.askopenfilenames(title="Seleccione Archivos para la Simulación", filetypes=filetypes)
        if archivos:
            # Confirmación inicial
            confirmacion = messagebox.askyesno(
                "Confirmar Selección",
                f"¿Confirma que los archivos seleccionados son los correctos para realizar la simulación?\n\n"
                f"Los archivos serán copiados a la carpeta padre en la ruta:\n\n{self.ruta_carpeta_padre}"
            )
            if not confirmacion:
                messagebox.showinfo("Acción Cancelada", "No se copiaron los archivos seleccionados.")
                return

            # Verificar permisos de escritura en la carpeta "Input"
            if not os.access(input_folder, os.W_OK):
                messagebox.showerror(
                    "Permisos Insuficientes",
                    f"No se tienen permisos de escritura en la carpeta:\n\n{input_folder}"
                )
                return

            # Verificar si hay archivos previos en la carpeta "Input"
            if os.path.exists(input_folder) and os.listdir(input_folder):
                continuar = messagebox.askyesno(
                    "Archivos Existentes",
                    "La carpeta llamada 'Input' ya contiene archivos.\n\n¿Desea continuar y copiar los nuevos archivos?"
                )
                if not continuar:
                    messagebox.showinfo("Acción Cancelada", "No se copiaron los archivos seleccionados.")
                    return
            else:
                os.makedirs(input_folder, exist_ok=True)

            # Validar extensiones de los archivos seleccionados
            extensiones_permitidas = tuple(extensiones)  # Convertir a tupla para usar con `endswith`
            for archivo in archivos:
                if not archivo.lower().endswith(extensiones_permitidas):
                    messagebox.showerror(
                        "Extensión No Permitida",
                        f"El archivo '{os.path.basename(archivo)}' tiene una extensión no permitida.\n\n"
                        f"Extensión detectada: {os.path.splitext(archivo)[1]}"
                    )
                    return

            # Validar que los archivos seleccionados no provengan de la carpeta "Input"
            for archivo in archivos:
                if os.path.dirname(archivo) == input_folder:
                    messagebox.showerror(
                        "Archivo en la Misma Carpeta",
                        f"El archivo '{os.path.basename(archivo)}' ya está en la carpeta 'Input'.\n\nNo se puede copiar desde la misma carpeta."
                    )
                    return

            # Copiar archivos seleccionados a la carpeta "Input"
            try:
                for archivo in archivos:
                    destino = os.path.join(input_folder, os.path.basename(archivo))

                    # Verificar si el archivo ya existe en la carpeta "Input"
                    if os.path.exists(destino):
                        sobrescribir = messagebox.askyesno(
                            "Archivo Duplicado",
                            f"El archivo '{os.path.basename(archivo)}' ya existe en la carpeta 'Input'.\n\n"
                            "¿Desea sobrescribirlo?"
                        )
                        if not sobrescribir:
                            messagebox.showinfo("Archivo Ignorado", f"Se ignoró el archivo '{os.path.basename(archivo)}'.")
                            continue

                    shutil.copy(archivo, destino)

                # Actualizar la etiqueta de cantidad de archivos
                cantidad_archivos_input = len([f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))])
                self.etiqueta_cantidad_archivos_input.configure(text=f"Cantidad de archivos en Input: {cantidad_archivos_input}")

                messagebox.showinfo("Archivos Copiados", f"Archivos copiados exitosamente en la ruta:\n\n{input_folder}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al copiar los archivos en la ruta:\n{str(e)}")

    def seleccionar_archivo_inp(self):
        if not self.ruta_carpeta_padre:
            messagebox.showerror("Error", "Seleccione primero una Carpeta Padre para continuar.")
            return

        input_folder = os.path.join(self.ruta_carpeta_padre, "Input")
        archivo_inp = filedialog.askopenfilename(
            title="Seleccione Archivo .inp",
            filetypes=[("Archivos de Entrada (*.inp)", "*.inp")],
            initialdir=input_folder
        )

        if archivo_inp:
            self.ruta_archivo_inp = archivo_inp
            self.etiqueta_inp.configure(text=f"INP: {os.path.basename(archivo_inp)}")

            # Actualizar el estado del análisis
            self.etiqueta_estado_analisis.configure(text="Estado del análisis del inp: En proceso...", text_color="orange")

            # Deshabilitar botones al inicio
            self.boton_inp.configure(state="disabled")
            self.boton_carpeta_padre.configure(state="disabled")
            self.boton_archivos_simulacion.configure(state="disabled")
            self.boton_simulacion.configure(state="disabled")

            # Crear un hilo para procesar el archivo
            def procesar_archivo():
                try:
                    with open(archivo_inp, 'rb') as f:
                        contenido_binario = f.read()

                    # Lecutra si contiene caracteres no ASCII
                    es_binario = any(b > 127 or (b < 32 and b not in (9, 10, 13)) for b in contenido_binario)

                    contenido = ""
                    if not es_binario:
                        try:
                            with open(archivo_inp, 'r', encoding='utf-8') as f:
                                contenido = f.read()
                        except UnicodeDecodeError:
                            with open(archivo_inp, 'r', encoding='latin-1') as f:
                                contenido = f.read()

                    palabras_binario = [
                        '*Node Output', '*node output', '*Node output', '*NODE OUTPUT',
                        '*ELEMENT OUTPUT', '*Element Output', '*Element output', '*element output'
                    ]
                    palabras_ascii = [
                        '*NODE FILE', '*node file', '*Node File', '*Node file',
                        '*EL FILE', '*el file', '*El File', '*El file'
                    ]

                    contiene_palabras_binario = any(palabra in contenido for palabra in palabras_binario)
                    contiene_palabras_ascii = any(palabra in contenido for palabra in palabras_ascii)

                    # Mostrar mensajes en base a las detecciones
                    if es_binario:
                        self.raiz.after(0, lambda: messagebox.showwarning(
                            "Formato del archivo",
                            f"El archivo {os.path.basename(archivo_inp)} es BINARIO"
                        ))
                    elif contiene_palabras_binario:
                        self.raiz.after(0, lambda: messagebox.showwarning(
                            "Formato del archivo",
                            f"El archivo {os.path.basename(archivo_inp)} generará un tipo BINARIO"
                        ))
                    elif contiene_palabras_ascii:
                        self.raiz.after(0, lambda: messagebox.showinfo(
                            "Formato del archivo",
                            f"El archivo {os.path.basename(archivo_inp)} generará un tipo ASCII"
                        ))
                    else:
                        self.raiz.after(0, lambda: messagebox.showinfo(
                            "Formato del archivo",
                            f"No se puede determinar el formato del archivo {os.path.basename(archivo_inp)}. Es ASCII pero sin comandos en el archivo INP para generar un archivo de salida correcto"
                        ))

                except Exception as e:
                    self.raiz.after(0, lambda: messagebox.showerror("Error", f"No se pudo leer el archivo: {e}"))

                finally:
                    # Reactivación de los botones y actualización del estado del análisis al finalizar
                    self.raiz.after(0, lambda: [
                        self.boton_inp.configure(state="normal"),
                        self.boton_simulacion.configure(state="normal"),
                        self.boton_carpeta_padre.configure(state="normal"),
                        self.boton_archivos_simulacion.configure(state="normal"),
                        self.etiqueta_estado_analisis.configure(text="Estado del análisis: Completado", text_color="green")
                    ])

            # Ejecutar el procesamiento en un hilo separado
            threading.Thread(target=procesar_archivo).start()

        else:
            self.etiqueta_inp.configure(text="INP: No seleccionado")


    def seleccionar_ejecutable_ccx(self):
        if self.ruta_ejecutable_ccx:
            respuesta = messagebox.askyesno("Ejecutable de CalculiX", f"Ya tiene un ejecutable seleccionado: {self.ruta_ejecutable_ccx}. ¿Desea cambiarlo?")
            if not respuesta:
                return
        
        self.ruta_ejecutable_ccx = filedialog.askopenfilename(filetypes=[("Ejecutable de CalculiX", "*.exe")])
        if self.ruta_ejecutable_ccx:
            messagebox.showinfo("Ejecutable Seleccionado", f"Ejecutable seleccionado: {self.ruta_ejecutable_ccx}")
            self.guardar_ruta('calculix_path.json', self.ruta_ejecutable_ccx)
        else:
            messagebox.showerror("Error", "No se encontró el ejecutable de CalculiX. Verifique la instalación y la ruta del ejecutable.")

    def seleccionar_ejecutable_paraview(self):
        if self.ruta_paraview:
            respuesta = messagebox.askyesno("Ejecutable de ParaView", f"Ya tiene un ejecutable seleccionado: {self.ruta_paraview}. ¿Desea cambiarlo?")
            if not respuesta:
                return
        
        self.ruta_paraview = filedialog.askopenfilename(filetypes=[("Ejecutable de ParaView", "*.exe")])
        if self.ruta_paraview:
            messagebox.showinfo("Ejecutable Seleccionado", f"Ejecutable de ParaView seleccionado: {self.ruta_paraview}")
            self.guardar_ruta('paraview_path.json', self.ruta_paraview)
        else:
            messagebox.showerror("Error", "No se encontró el ejecutable de ParaView. Verifique la instalación y la ruta del ejecutable.")

    def ejecutar_simulacion(self):
        # Validar si el archivo INP y el ejecutable están configurados
        if not hasattr(self, 'ruta_archivo_inp') or not self.ruta_archivo_inp:
            messagebox.showerror("Error", "Seleccione un archivo .inp antes de ejecutar la simulación.")
            return
        if not self.ruta_ejecutable_ccx:
            messagebox.showerror("Error", "Seleccione el ejecutable de CalculiX antes de ejecutar la simulación.")
            return

        # Crear la carpeta "Run" si no existe
        run_folder = os.path.join(self.ruta_carpeta_padre, "Run")
        if not os.path.exists(run_folder):
            os.makedirs(run_folder)

        # Limpiar el contenido de la carpeta "Run" si ya existen archivos
        if os.listdir(run_folder):
            respuesta = messagebox.askyesno(
                "Advertencia",
                "La carpeta 'Run' ya contiene archivos. Estos serán sobrescritos. ¿Está seguro de que desea continuar con la ejecución de la simulación?"
            )
            if respuesta:
                try:
                    # Eliminar todos los archivos y subcarpetas en "Run"
                    for archivo in os.listdir(run_folder):
                        archivo_path = os.path.join(run_folder, archivo)
                        if os.path.isfile(archivo_path):
                            os.remove(archivo_path)
                        elif os.path.isdir(archivo_path):
                            shutil.rmtree(archivo_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Error al limpiar la carpeta 'Run': {str(e)}")
                    return
            else:
                messagebox.showinfo("Información", "La simulación ha sido cancelada.")
                return

        # Copiar el archivo seleccionado a la carpeta Run
        try:
            archivo_destino = os.path.join(run_folder, os.path.basename(self.ruta_archivo_inp))
            shutil.copy(self.ruta_archivo_inp, archivo_destino)
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar el archivo INP seleccionado a la carpeta Run: {str(e)}")
            return

        # Deshabilitar botones durante la simulación
        self.boton_simulacion.configure(state="disabled", fg_color="#3A3A3A", text_color="white")
        self.boton_inp.configure(state="disabled")
        self.boton_carpeta_padre.configure(state="disabled")
        self.boton_archivos_simulacion.configure(state="disabled")
        self.actualizar_estado_simulacion("En proceso...", text_color="orange")

        # Preguntar al usuario si desea generar un log o ejecutar en CMD
        ejecutar_con_log = messagebox.askyesno(
            "Modo de Ejecución",
            "¿Desea ejecutar la simulación generando un archivo log de la simulación? En este modo no podrá ver la ejecución de la simulación desde el CMD."
        )

        # Preparar el nombre del archivo .inp sin extensión
        archivo_inp_nombre = os.path.basename(self.ruta_archivo_inp)
        nombre_archivo_sin_extension = os.path.splitext(archivo_inp_nombre)[0]

        def finalizar_simulacion():
            # Reactivar botones al finalizar la simulación
            self.boton_simulacion.configure(state="normal", fg_color="#1F6AA5", text_color="white")
            self.boton_inp.configure(state="normal")
            self.boton_carpeta_padre.configure(state="normal")
            self.boton_archivos_simulacion.configure(state="normal")
            self.actualizar_estado_simulacion("Simulación completada", text_color="green")

        # Iniciar el proceso de simulación
        if ejecutar_con_log:
            log_file_path = os.path.join(run_folder, f"{nombre_archivo_sin_extension}.log")
            try:
                with open(log_file_path, 'w') as log_file:
                    self.proceso = subprocess.Popen(
                        [self.ruta_ejecutable_ccx, nombre_archivo_sin_extension],
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        cwd=run_folder,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    # Monitorear el proceso en un hilo
                    threading.Thread(target=self.monitorear_proceso, args=(finalizar_simulacion,)).start()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al ejecutar la simulación: {str(e)}")
                finalizar_simulacion()
        else:
            comando = f'start cmd /k "{self.ruta_ejecutable_ccx} {nombre_archivo_sin_extension}"'
            try:
                self.proceso = subprocess.Popen(comando, shell=True, cwd=run_folder)
                threading.Thread(target=self.monitorear_proceso, args=(finalizar_simulacion,)).start()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error durante la simulación: {str(e)}")
                finalizar_simulacion()                      






    def actualizar_estado_simulacion(self, estado, text_color="gray"):
        if hasattr(self, 'etiqueta_estado_simulacion'):self.etiqueta_estado_simulacion.configure(text=f"Estado de la simulación: {estado}", text_color=text_color)


    def monitorear_proceso(self, callback_finalizacion):
        def verificar_estado():
            if self.proceso.poll() is None:
                # Si el proceso sigue corriendo, verificar nuevamente después de 100ms
                self.raiz.after(100, verificar_estado)
            else:
                # Actualizar el estado al finalizar el proceso
                self.actualizar_estado_simulacion("Simulación completada", text_color="green")
                run_folder = os.path.join(self.ruta_carpeta_padre, "Run")
                self.limpiar_archivos(None, run_folder)
                callback_finalizacion()

        # Iniciar el monitoreo del estado
        verificar_estado()

        
    def limpiar_archivos(self, proceso, run_folder):
        try:
            if proceso:
                proceso.wait()

            respuesta = messagebox.askyesno(
                "Simulación Completa",
                "La simulación ha finalizado. ¿Desea eliminar los archivos de entrada utilizados en la carpeta Run?"
            )
            if respuesta:
                # Definir las extensiones de los archivos a eliminar
                extensiones_a_eliminar = ['.inp', '.msh', '.mat', '.rad', '.flm']
                for archivo in os.listdir(run_folder):
                    archivo_path = os.path.join(run_folder, archivo)
                    if os.path.isfile(archivo_path) and any(archivo.endswith(ext) for ext in extensiones_a_eliminar):
                        os.remove(archivo_path)

                messagebox.showinfo("Archivos Eliminados", "Los archivos de entrada han sido eliminados de la carpeta Run.")
            else:
                messagebox.showinfo("Archivos Conservados", "Los archivos no se eliminaron y permanecen en la carpeta Run.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al limpiar los archivos: {str(e)}")

    def convertir_frd_a_vtu_async(self):
        # Ejecutar la conversión en un hilo separado para evitar que la interfaz se congele
        threading.Thread(target=self.convertir_frd_a_vtu).start()

    def convertir_frd_a_vtu(self):
        if not self.ruta_carpeta_padre:
            messagebox.showerror("Error", "Seleccione una Carpeta Padre primero.")
            return

        self.boton_convertir.configure(state="disabled", fg_color="#3A3A3A", text_color="white")
        results_folder = os.path.join(self.ruta_carpeta_padre, "Results")

        # Verificar permisos en la carpeta Results
        if not self.verificar_permisos_carpeta(results_folder):
            messagebox.showerror("Error de Permisos", f"No se tienen permisos de escritura en la carpeta 'Results':\n\n{results_folder}")
            self.boton_convertir.configure(state="normal", fg_color="#1F6AA5", text_color="white")
            return

        # Buscar archivos .frd en la carpeta padre y sus subcarpetas
        frd_files = []
        for root, _, files in os.walk(self.ruta_carpeta_padre):
            for file in files:
                if file.endswith('.frd'):
                    frd_files.append(os.path.join(root, file))

        if not frd_files:
            messagebox.showerror("Error", "No se encontró ningún archivo .frd en la Carpeta Padre")
            self.boton_convertir.configure(state="normal", fg_color="#1F6AA5", text_color="white")
            return

        # Si hay un solo archivo .frd, convertir directamente
        if len(frd_files) == 1:
            frd_file = frd_files[0]
            Thread(target=self.procesar_conversion, args=(frd_file, results_folder)).start()
            return

        # Si hay múltiples archivos .frd, mostrar una ventana para selección
        def seleccionar_archivo():
            try:
                seleccionado = listbox.get(listbox.curselection())
                ventana_seleccion.destroy()
                Thread(target=self.procesar_conversion, args=(seleccionado, results_folder)).start()
            except Exception:
                self.boton_convertir.configure(state="normal", fg_color="#1F6AA5", text_color="white")

        def cerrar_ventana():
            self.boton_convertir.configure(state="normal", fg_color="#1F6AA5", text_color="white")
            ventana_seleccion.destroy()

        ventana_seleccion = Toplevel(self.raiz)
        ventana_seleccion.title("Seleccionar Archivo FRD")
        ventana_seleccion.geometry("500x400")
        ventana_seleccion.transient(self.raiz)
        ventana_seleccion.grab_set()
        ventana_seleccion.protocol("WM_DELETE_WINDOW", cerrar_ventana)

        listbox = Listbox(ventana_seleccion, selectmode="single", font=("Arial", 12))
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        for file in frd_files:
            listbox.insert("end", file)

        boton_aceptar = Button(ventana_seleccion, text="Aceptar", command=seleccionar_archivo)
        boton_aceptar.pack(pady=10)


    def procesar_conversion(self, frd_file, results_folder):
        try:
            # Verificar si el archivo FRD es binario
            with open(frd_file, 'rb') as f:
                contenido_binario = f.read(1024)  # Leer solo una parte del archivo
            es_binario = any(b > 127 or (b < 32 and b not in (9, 10, 13)) for b in contenido_binario)

            if es_binario:
                self.actualizar_estado_conversion("Error: Archivo binario.", text_color="red")
                messagebox.showerror(
                    "Error de Conversión",
                    f"No se puede convertir el archivo {os.path.basename(frd_file)} a VTU, ya que está en formato binario."
                )
                self.boton_convertir.configure(state="normal", fg_color="#1F6AA5", text_color="white")
                return

            # Actualizar estado al iniciar
            self.actualizar_estado_conversion("En progreso...", text_color="orange")

            # Preparar la carpeta Results
            if os.path.exists(results_folder):
                respuesta = messagebox.askyesno(
                    "Confirmación",
                    "La carpeta 'Results' ya existe. ¿Desea eliminarla para continuar con la conversión?"
                )
                if respuesta:
                    try:
                        shutil.rmtree(results_folder)
                        os.makedirs(results_folder)
                    except Exception as e:
                        self.actualizar_estado_conversion("Error al preparar carpeta.")
                        messagebox.showerror("Error", f"No se pudo eliminar la carpeta 'Results': {str(e)}")
                        return
                else:
                    self.actualizar_estado_conversion("Cancelada.")
                    messagebox.showinfo("Información", "Conversión cancelada")
                    return
            else:
                os.makedirs(results_folder)

            # Copiar el archivo .frd seleccionado a Results
            copied_frd_file = os.path.join(results_folder, os.path.basename(frd_file))
            try:
                shutil.copy(frd_file, copied_frd_file)
            except Exception as e:
                self.actualizar_estado_conversion("Error al copiar archivo.")
                messagebox.showerror("Error", f"No se pudo copiar el archivo FRD: {str(e)}")
                return

            # Convertir el archivo .frd copiado
            try:
                self.actualizar_estado_conversion("Convirtiendo archivo...", text_color="orange")
                from ccx2paraview import Converter
                c = Converter(copied_frd_file, ["vtu"])
                c.run()

                self.actualizar_estado_conversion("Conversión completada", text_color="green")
                messagebox.showinfo("Conversión Completa", "El archivo FRD ha sido convertido a VTU exitosamente.")

            except Exception as e:
                self.actualizar_estado_conversion("Error durante la conversión.")
                messagebox.showerror("Error en Conversión", str(e))

        finally:
            self.boton_convertir.configure(state="normal", fg_color="#1F6AA5", text_color="white")


    def actualizar_estado_conversion(self, estado, text_color="gray"):
        if hasattr(self, 'etiqueta_estado_conversion'):
            # Usar 'after' para actualizar el label desde el hilo principal
            self.raiz.after(0, lambda: self.etiqueta_estado_conversion.configure(text=f"Estado del convertidor: {estado}", text_color=text_color))


    def mostrar_resultados_paraview(self):
        # Validar que la ruta de ParaView está configurada
        if not self.ruta_paraview or not os.path.isfile(self.ruta_paraview):
            messagebox.showwarning(
                "Advertencia",
                "Seleccione el ejecutable de ParaView para poder visualizar la simulación."
            )
            return

        # Verificar que la ruta de ParaView es un ejecutable
        if not self.ruta_paraview.lower().endswith(".exe"):
            messagebox.showerror(
                "Error de Configuración",
                "La ruta seleccionada para ParaView no es un archivo ejecutable válido. "
                "Por favor seleccione un ejecutable válido."
            )
            return

        # Validar que existe un archivo .inp asociado
        if not hasattr(self, 'ruta_archivo_inp') or not self.ruta_archivo_inp:
            messagebox.showerror(
                "Error",
                "No se ha seleccionado un archivo .inp válido. Por favor configure la simulación correctamente."
            )
            return

        # Obtener el nombre base del archivo .inp sin extensión
        nombre_base_inp = os.path.splitext(os.path.basename(self.ruta_archivo_inp))[0]
        
        # Construir la ruta del archivo .pvd dentro de la carpeta Results
        results_folder = os.path.join(self.ruta_carpeta_padre, "Results")
        archivo_pvd = os.path.join(results_folder, f"{nombre_base_inp}.pvd")

        # Verificar que la carpeta Results exista
        if not os.path.isdir(results_folder):
            messagebox.showerror(
                "Error",
                f"No se encontró la carpeta 'Results'. Por favor genere los resultados antes de intentar abrir ParaView."
            )
            return

        # Verificar que el archivo PVD existe
        if not os.path.exists(archivo_pvd):
            messagebox.showwarning(
                "Advertencia",
                "No se encontró el archivo PVD generado"
            )
            return

        # Ejecutar ParaView si todas las condiciones están satisfechas
        try:
            # Desactivar el botón antes de abrir ParaView
            self.boton_mostrar_resultados.configure(state="disabled", fg_color="#3A3A3A", text_color="white")

            # Crear un hilo para manejar la ejecución de ParaView
            def abrir_paraview():
                try:
                    proceso = subprocess.Popen([self.ruta_paraview, archivo_pvd])
                    proceso.wait()  # Esperar a que ParaView termine
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir ParaView: {str(e)}")
                finally:
                    # Reactivar los botones después de que ParaView se haya abierto
                    self.raiz.after(0, lambda: self.boton_mostrar_resultados.configure(state="normal", fg_color="#1F6AA5", text_color="white"))

            # Ejecutar ParaView en un hilo separado
            threading.Thread(target=abrir_paraview).start()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir ParaView: {str(e)}")
    

    def mostrar_instrucciones(self):
        ventana_instrucciones = Toplevel(self.raiz)
        ventana_instrucciones.title("Instrucciones de Uso")
        ventana_instrucciones.geometry("900x700")
        ventana_instrucciones.resizable(True, True)

        # Encabezado principal
        encabezado = ctk.CTkLabel(
            ventana_instrucciones,
            text="Instrucciones de Uso",
            font=("Arial", 24, "bold"),
            text_color="#0056b3"
        )
        encabezado.pack(pady=10)

        # Marco principal
        marco_principal = ctk.CTkFrame(ventana_instrucciones, fg_color="#f4f4f4", corner_radius=8)
        marco_principal.pack(fill="both", expand=True, padx=20, pady=10)

        # Canvas para manejar el scroll
        canvas = ctk.CTkCanvas(marco_principal, bg="#f9f9f9", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = ctk.CTkScrollbar(marco_principal, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Marco interno para el contenido
        marco_interno = ctk.CTkFrame(canvas, fg_color="#ffffff", corner_radius=8)
        canvas.create_window((0, 0), window=marco_interno, anchor="nw", width=860)

        # Contenido de las instrucciones
        secciones = [
            {
                "titulo": "PASO 1: Seleccione la Carpeta Padre",
                "contenido": """Seleccione un directorio donde se guardarán las carpetas de los resultados de la simualción:

- Haga clic en el botón **"Seleccionar Carpeta Padre"**.
- Automáticamente se creará una carpeta llamada 'Simulacion' que sera el lugar donde 
  se guardaran todos los archivos de la simulación a ejecutar.""",
            },
            {
                "titulo": "PASO 2: Seleccione los Archivos de Simulación",
                "contenido": """Elija los archivos que necesite para la simulación:

- Haga clic en el botón **"Seleccionar Archivos para la Simulación"**.
- Estos archivos se copiarán automáticamente a la carpeta 'Input', 
  que se creo en la carpeta principal llamada "Simulación".
- Si hay archivos existentes, podrá decidir si desea sobrescribirlos o conservarlos.""",
            },
            {
                "titulo": "PASO 3: Seleccione el Archivo .inp",
                "contenido": """El archivo .inp es esencial para la simulación:

- Haga clic en el botón **"Seleccionar Archivo .inp"**.
- La herramienta analizará el archivo para determinar si es ASCII o BINARIO.
- Para que el usuario determine si seguira la ejecución de la simulacipon si es BINARIO o ASCII.""",
            },
            {
                "titulo": "PASO 4: Configure los Ejecutables",
                "contenido": """Es necesario configurar los ejecutables de CalculiX y ParaView:

- En el menú **"Configuraciones"**, seleccione **Ejecutable de CalculiX** 
  y elija el archivo .exe correspondiente.
- Seleccione **Ejecutable de ParaView** para configurar la herramienta de visualización.
- NOTA: Previamente deberia tener el ejecutable de calculix y paraview""",
            },
            {
                "titulo": "PASO 5: Ejecute la Simulación",
                "contenido": """Una vez configurados los pasos anteriores, ejecute la simulación:

- Haga clic en el botón **"Ejecutar Simulación"**.
- Puede elegir entre generar un archivo log o visualizar la simulación en CMD.
- Los resultados se generarán en la carpeta **Run**.""",
            },
            {
                "titulo": "PASO 6: Convierta Archivos FRD a VTU",
                "contenido": """Para convertir los resultados a un formato compatible con ParaView:

- Haga clic en el botón **"Convertidor de FRD a VTU"**.
- En caso de que tenga mas de un frd en la carpeta Simulacion, seleccione el archivo .frd a generar.
- Si en caso que solo tenga uno, se convertira el frd a Vtu de manera automatica, 
  sin selecionar dicho frd
- El archivo convertido se guardará en la carpeta **Results**.""",
            },
            {
                "titulo": "PASO 7: Visualice los Resultados",
                "contenido": """Después de convertir los archivos a VTU:

- Haga clic en el botón **"Mostrar Resultados en ParaView"**.
- El programa abrirá ParaView automáticamente con los resultados generados.""",
            },
            {
                "titulo": "Notas Importantes",
                "contenido": """- Asegúrese de configurar correctamente los ejecutables antes de iniciar cualquier simulación.

- Verifique los permisos de escritura en las carpetas seleccionadas.
- Consulte la documentación técnica para más información sobre los archivos necesarios.""",
            }
        ]

        for seccion in secciones:
            # Título de la sección
            titulo = ctk.CTkLabel(
                marco_interno,
                text=seccion["titulo"],
                font=("Arial", 18, "bold"),
                text_color="#003366",
                anchor="w",
                width=800
            )
            titulo.pack(pady=(10, 5), anchor="w", padx=10)

            # Contenido de la sección
            contenido = ctk.CTkLabel(
                marco_interno,
                text=seccion["contenido"],
                font=("Arial", 14),
                wraplength=800,
                justify="left",
                text_color="#333333",
                anchor="w",
            )
            contenido.pack(pady=(0, 10), anchor="w", padx=10)

            # Separador
            separador = ctk.CTkFrame(marco_interno, height=2, fg_color="#cccccc")
            separador.pack(fill="x", pady=10, padx=10)

        # Ajustar el tamaño del contenido
        marco_interno.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Botón de cierre
        boton_cerrar = ctk.CTkButton(ventana_instrucciones, text="Cerrar", command=ventana_instrucciones.destroy)
        boton_cerrar.pack(pady=10)




    def cerrar_interfaz(self):
        self.raiz.quit()

def iniciar_interfaz():
    raiz = ctk.CTk()
    app = AppSimulacionSoldadura(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
