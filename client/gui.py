import tkinter as tk 
from tkinter import messagebox, filedialog
from tkinter import ttk

# Variables globales para almacenar el número de entradas, salidas y patrones
num_entradas_global = None
num_salidas_global = None
num_patrones_global = None

# Lista global para almacenar los patrones de entrada
patrones_entrada = []

def cargar_bd(archivo):
    try:
        with open(archivo, 'r') as archivo:
            lineas = archivo.readlines()
            datos = [linea.strip().split(',') for linea in lineas]  
        return datos
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de base de datos.")

def mostrar_tabla(datos):
    # Crear la ventana de tabla
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Tabla de Datos")
    
    tabla = ttk.Treeview(ventana_tabla)
    
    # Asumiendo que todas las filas tienen la misma longitud
    num_columnas = len(datos[0])
    tabla['columns'] = tuple(range(1, num_columnas + 1))  # Cambiamos el rango para omitir la Columna 0
    
    for columna in tabla['columns']:
        tabla.column(columna, anchor=tk.CENTER)
        # No agregamos encabezado para omitir Columna 0
    
    for i, fila in enumerate(datos, start=1):
        tabla.insert(parent='', index='end', iid=i, values=tuple(fila))
    
    tabla.pack(fill="both", expand=True)
    
    # Botón para abrir la ventana de ingresar valores
    btn_ingresar_valores = tk.Button(ventana_tabla, text="Ingresar valores", command=abrir_ventana_ingresar_valores)
    btn_ingresar_valores.pack()

def cargar_base_de_datos_click():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de base de datos", filetypes=[("Archivos de texto", "*.txt")])
    if not archivo:
        return
    
    try:
        datos = cargar_bd(archivo)
        if datos:
            # Llamar a la función mostrar_tabla para mostrar los datos cargados
            mostrar_tabla(datos)
            
            # Solicitar al usuario el número de entradas, salidas y patrones
            if num_entradas_global is None:
                ingresar_valores(tk.Toplevel())  # Pasar la ventana actual como argumento

    except ValueError:
        messagebox.showerror("Error", "Ocurrió un error al cargar la base de datos.")

def abrir_ventana_ingresar_valores():
    ventana_valores = tk.Toplevel()
    ventana_valores.title("Ingresar valores")
    
    # Campos de entrada para los valores
    tk.Label(ventana_valores, text="Número de entradas:").grid(row=0, column=0)
    entry_entradas = tk.Entry(ventana_valores)
    entry_entradas.grid(row=0, column=1)
    
    tk.Label(ventana_valores, text="Número de salidas:").grid(row=1, column=0)
    entry_salidas = tk.Entry(ventana_valores)
    entry_salidas.grid(row=1, column=1)
    
    tk.Label(ventana_valores, text="Número de patrones:").grid(row=2, column=0)
    entry_patrones = tk.Entry(ventana_valores)
    entry_patrones.grid(row=2, column=1)
    
    # Botón para aplicar los valores
    btn_aplicar = tk.Button(ventana_valores, text="Aplicar", command=lambda: aplicar_valores(entry_entradas.get(), entry_salidas.get(), entry_patrones.get(), ventana_valores))
    btn_aplicar.grid(row=3, columnspan=2)
    
def aplicar_valores(num_entradas, num_salidas, num_patrones, parent):
    valores_umbral = []  # Aquí deberías obtener los valores del umbral desde la interfaz
    valores_peso = []    # Aquí deberías obtener los valores del peso desde la interfaz
    
    global m, n, p
    m = int(num_entradas)
    n = int(num_salidas)
    p = int(num_patrones)
    
    # Calcular los tamaños de las matrices
    tamano_umbral, tamano_peso = calcular_matrices(m, n, p)
    
    # Cerrar la ventana de ingreso de valores
    parent.destroy()
    
    # Guardar los valores en el archivo pe.txt
    guardar_valores(m, n, p, valores_umbral, valores_peso, tamano_umbral, tamano_peso)


def calcular_matrices(num_entradas, num_salidas, num_patrones):
    # Calcular el tamaño de la matriz umbral U[n]
    tamano_umbral = num_salidas
    
    # Calcular el tamaño de la matriz de peso W
    tamano_peso = num_entradas * num_salidas
    
    return tamano_umbral, tamano_peso

def guardar_valores(num_entradas, num_salidas, num_patrones, valores_umbral, valores_peso, tamano_umbral, tamano_peso):
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], title="Guardar valores como")
    
    if nombre_archivo:
        try:
            with open(nombre_archivo, "w") as f:
                # Escribir la información sobre los tamaños de las matrices y los números de entradas, salidas y patrones
                f.write(f"{tamano_umbral}\n")  # Guarda el tamaño de la matriz umbral
                f.write(f"{tamano_peso}\n")  # Guarda el tamaño de la matriz de peso
                f.write(f"{num_entradas}\n")  # Guarda el número de entradas
                f.write(f"{num_salidas}\n")  # Guarda el número de salidas
                f.write(f"{num_patrones}\n\n")  # Guarda el número de patrones
             
            messagebox.showinfo("Información", f"Valores y tamaños de las matrices guardados exitosamente en '{nombre_archivo}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los valores y tamaños de las matrices: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó un nombre de archivo.")



def salir(root):
    if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
        root.destroy()

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack()
        self.config(bg='black')
        
        # Crear el título llamativo
        self.lbl_titulo = tk.Label(self, text="RED DE APRENDIZAJE SUPERVIZADO", font=("Times New Roman", 16, "bold"))
        self.lbl_titulo.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        # Crear el botón de Inicio
        self.btn_inicio = tk.Button(self, text="Cargar base de datos BD", command=cargar_base_de_datos_click)
        self.btn_inicio.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Botón para cargar archivo de umbral y peso
        btn_cargar_umbral_peso = tk.Button(self, text="Cargar archivo de umbral y peso", command=cargar_archivo_umbral_peso)
        btn_cargar_umbral_peso.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Botón para mostrar el archivo de matriz de umbral y peso
        btn_mostrar_umbral_peso = tk.Button(self, text="Mostrar matriz de umbral y peso", command=mostrar_umbral_peso)
        btn_mostrar_umbral_peso.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        # Crear el botón de Salir
        self.btn_salir = tk.Button(self, text="Salir", command=lambda: salir(root))
        self.btn_salir.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        

def cargar_archivo_umbral_peso():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de umbral y peso", filetypes=[("Archivos de texto", "*.txt")])
    if not archivo:
        return
    
    try:
        with open(archivo, 'r') as f:
            # Leer los dos primeros números para obtener el tamaño de la matriz umbral y de peso
            tamano_umbral = int(f.readline())
            tamano_peso = int(f.readline())

            messagebox.showinfo("Información", f"Tamaño de la matriz umbral: {tamano_umbral}\n"
                                                f"Tamaño de la matriz de peso: {tamano_peso}" )

            # Llamar a la función para ingresar los datos de umbral y peso con los valores obtenidos
            ingresar_datos_umbral_peso(tamano_umbral, tamano_peso)

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de umbral y peso.")

def ingresar_datos_umbral_peso(tamano_umbral, tamano_peso):
    ventana_valores = tk.Toplevel()
    ventana_valores.title("Ingresar valores de umbral y peso")

    # Campos de entrada para los valores de umbral
    tk.Label(ventana_valores, text="Valores de umbral (separados por comas):").grid(row=0, column=0)
    entry_umbral = tk.Entry(ventana_valores)
    entry_umbral.grid(row=0, column=1)

    # Campos de entrada para los valores de peso
    tk.Label(ventana_valores, text="Valores de peso (separados por comas y filas por punto y coma):").grid(row=1, column=0)
    entry_peso = tk.Entry(ventana_valores)
    entry_peso.grid(row=1, column=1)

    # Función para guardar los valores ingresados
    def guardar():
        valores_umbral = entry_umbral.get()
        valores_peso = entry_peso.get()

        # Guardar los valores en un archivo
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], title="Guardar valores como")
        if nombre_archivo:
            try:
                with open(nombre_archivo, "w") as f:
                    f.write(valores_umbral + "\n")
                    
                    f.write(valores_peso + "\n")

                messagebox.showinfo("Información", f"Valores de umbral y peso guardados exitosamente en '{nombre_archivo}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar los valores: {str(e)}")

        ventana_valores.destroy()

    # Botón para guardar los valores ingresados
    btn_guardar = tk.Button(ventana_valores, text="Guardar", command=guardar)
    btn_guardar.grid(row=2, columnspan=2)

def aplicar_valores_umbral_peso(valores_umbral, valores_peso, ventana_padre):
    # Convertir los valores ingresados a listas
    valores_umbral = valores_umbral.split(',')
    valores_peso = [fila.split(';') for fila in valores_peso.split(';')]  # Suponiendo que las filas están separadas por ';'

    # Convertir a números en lugar de strings
    valores_umbral = [float(valor) for valor in valores_umbral]
    valores_peso = [[float(valor) for valor in fila] for fila in valores_peso]

    # Llamar a la función para inicializar las matrices con los valores ingresados
    inicializar_matrices(valores_umbral, valores_peso)

    # Cerrar la ventana de ingreso de valores
    ventana_padre.destroy()
def mostrar_umbral_peso():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de umbral y peso", filetypes=[("Archivos de texto", "*.txt")])
    if not archivo:
        return
    
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()
            messagebox.showinfo("Contenido del archivo", f"Contenido del archivo de umbral y peso:\n\n{contenido}")
            
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de umbral y peso.")
