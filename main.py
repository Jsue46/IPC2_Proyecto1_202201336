import xml.etree.ElementTree as ET
from graphviz import Digraph

class NodoPiso:
    def __init__(self, nombre, R, C, F, S, patrones):
        self.nombre = nombre
        self.R = R
        self.C = C
        self.F = F
        self.S = S
        self.patrones = patrones

class NodoInstruccion:
    def __init__(self, instruccion=None, siguiente=None):
        self.instruccion = instruccion
        self.siguiente = siguiente

def calcular_costo_minimo(patron_origen, patron_destino, F, S):
    costo = 0
    instrucciones = None

    cambios = 0
    cambios_maximos = 2

    instrucciones = ListaEnlazada()

    for i in range(len(patron_origen)):
        if patron_origen[i] != patron_destino[i]:
            cambios += 1

            if cambios <= cambios_maximos:
                if costo + F <= S:
                    costo += F
                    instrucciones.agregar(f"Voltear el azulejo en la posición {i + 1}")
                else:
                    costo += S
                    instrucciones.agregar(f"Intercambiar el azulejo en la posición {i + 1} con el siguiente")
            else:
                costo += S
                instrucciones.agregar(f"Intercambiar el azulejo en la posición {i + 1} con el siguiente")


    if cambios > 0 and instrucciones is not None:
        return costo, instrucciones.obtener_instrucciones()
    else:
        return None, None

class NodoDato:
    def __init__(self, dato=None, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente

class ListaPisos:
    def __init__(self):
        self.cabeza = None

    def agregar_piso(self, nombre, R, C, F, S, patrones):
        nuevo_piso = NodoPiso(nombre, R, C, F, S, patrones)
        if not self.cabeza:
            self.cabeza = nuevo_piso
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_piso

    def buscar_piso(self, nombre_piso):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre_piso:
                return actual
            actual = actual.siguiente
        return None

# Mantenemos la clase ListaEnlazada sin modificar
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = NodoDato(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_instrucciones(self):
        instrucciones = []
        actual = self.cabeza
        while actual:
            instrucciones.append(actual.dato)
            actual = actual.siguiente
        return instrucciones

    def buscar_piso(self, nombre_piso):
        actual = self.cabeza
        while actual:
            if actual.dato.nombre == nombre_piso:
                return actual 
            actual = actual.siguiente
        return None

def menu():

    print("Bienvenido a Pisos de Guatemala, S.A.")
    print("Menú Principal")
    print("1. Cargar archivo.")
    print("2. Mostrar gráficamente el patrón.")
    print("3. Seleccionar un nuevo código de patrón")
    print("4. Mostrar pisos cargados")
    print("5. Salir")

def mostrar_patron(patron_data, R, C):
    dot = Digraph(comment='Patrón')
    dot.node('tab', label=f'<<TABLE>{generar_tabla(patron_data, R, C)}</TABLE>>', shape='none')
    dot.attr(fontsize='10', style='filled', fillcolor='lightgray', penwidth='0.5')
    dot.render('patron', format='png', cleanup=True)
    print("El patrón se ha mostrado gráficamente.")

def seleccionar_codigo_patron(piso):
    codigo_patron = input("Ingrese el código del patrón deseado: ")
    patron_data = None
    actual = piso.patrones.cabeza
    while actual:
        codigo, patron = actual.dato
        if codigo == codigo_patron:
            patron_data = patron
            break
        actual = actual.siguiente

    if patron_data is None:
        print("El código de patrón ingresado no corresponde a ningún patrón disponible.")
        return
    
    nuevo_codigo = input("Ingrese el nuevo código de patrón: ")
    costo, instrucciones = calcular_costo_minimo(piso.patrones.cabeza.dato[1], patron_data, piso.S, piso.F) # Corregir aquí

    if instrucciones is None:
        print("No se encontraron instrucciones para realizar el cambio.")
        return

    print(f"El costo mínimo para realizar el cambio hacia el nuevo patrón es: {costo} Quetzales.")
    opcion = input("¿Desea mostrar las instrucciones en consola o en un archivo? (consola/archivo): ").lower()
    if opcion == "consola":
        for instruccion in instrucciones:
            print(instruccion)
    elif opcion == "archivo":
        with open("instrucciones.txt", "w") as f:
            for instruccion in instrucciones:
                f.write(instruccion + "\n")
        print("Las instrucciones se han guardado en el archivo 'instrucciones.txt'.")
    else:
        print("Opción no válida.")


def mostrar_instrucciones(instrucciones):
    actual = instrucciones
    while actual:
        print(actual.instruccion)
        actual = actual.siguiente

def guardar_instrucciones_en_archivo(instrucciones):
    with open("instrucciones.txt", "w") as f:
        actual = instrucciones
        while actual:
            f.write(actual.instruccion + "\n")
            actual = actual.siguiente
    print("Las instrucciones se han guardado en el archivo 'instrucciones.txt'.")

def mostrar_pisos_y_patrones(lista_pisos):
    actual = lista_pisos.cabeza
    while actual:
        piso = actual.dato
        print(f"Piso: {piso.nombre}")
        print("Códigos de patrones disponibles:")
        actual_patron = piso.patrones.cabeza
        while actual_patron:
            codigo, _ = actual_patron.dato
            print(f"- Código: {codigo}")
            actual_patron = actual_patron.siguiente
        print()
        actual = actual.siguiente

def leer_archivo(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        lista_pisos = ListaEnlazada()
        for piso in root.findall('piso'):
            nombre = piso.get('nombre')
            R = int(piso.find('R').text)
            C = int(piso.find('C').text)
            F = int(piso.find('F').text)
            S = int(piso.find('S').text)
            patrones = ListaEnlazada()
            for patron in piso.find('patrones').findall('patron'):
                codigo = patron.get('codigo')
                patron_data = patron.text.strip()
                patrones.agregar((codigo, patron_data))
            nuevo_piso = NodoPiso(nombre, R, C, F, S, patrones)
            lista_pisos.agregar(nuevo_piso)
        return lista_pisos
    except FileNotFoundError:
        print("El archivo especificado no existe.")
        return None

def generar_tabla(patron_data, R, C):
    table = ""
    for i in range(R):
        table += "<TR>"
        for j in range(C):
            color = '#000000' if patron_data[i * C + j] == 'B' else '#FFFFFF'
            table += f'<TD BGCOLOR="{color}" WIDTH="10" HEIGHT="10"></TD>'  # Añadido el tamaño de los cuadros
        table += "</TR>"
    return table


if __name__ == "__main__":
    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        
        if opcion == "1":
            filename = input("Ingrese el nombre del archivo XML: ")
            lista_pisos = leer_archivo(filename)
            if lista_pisos is not None:
                print("Archivo leído correctamente")
                print("Los pisos y patrones se han cargado correctamente.")
                print("")
                print("")
            else:
                print("El archivo especificado no existe.")

        

        elif opcion == "2":
            nombre_piso = input("Ingrese el nombre del piso: ")
            codigo_patron = input("Ingrese el código del patrón: ")
            piso_nodo = lista_pisos.buscar_piso(nombre_piso)
            if piso_nodo and piso_nodo.dato:   
                patron_data = None
                actual = piso_nodo.dato.patrones.cabeza 
                while actual:
                    codigo, data = actual.dato
                    if codigo == codigo_patron:
                        patron_data = data
                        break
                    actual = actual.siguiente
                if patron_data:
                    mostrar_patron(patron_data, piso_nodo.dato.R, piso_nodo.dato.C)
                else:
                    print("El código de patrón ingresado no corresponde a ningún patrón disponible.")
            else:
                print("El nombre del piso ingresado no corresponde a ningún piso disponible.")
        
        elif opcion == "3":
            nombre_piso = input("Ingrese el nombre del piso: ")
            codigo_patron = input("Ingrese el código del patrón: ")
            piso_nodo = lista_pisos.buscar_piso(nombre_piso)
            if piso_nodo and piso_nodo.dato:  
                seleccionar_codigo_patron(piso_nodo.dato)
            else:
                print("El nombre del piso ingresado no corresponde a ningún piso disponible.")
        
        elif opcion == "4":
            print()
            mostrar_pisos_y_patrones(lista_pisos)
        
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
