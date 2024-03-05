import xml.etree.ElementTree as ET
import os

class Azulejo:
    def __init__(self, color):
        self.color = color
        self.siguiente = None

class Patron:
    def __init__(self, codigo):
        self.codigo = codigo
        self.primero = None

    def agregar_azulejo(self, color):
        nuevo_azulejo = Azulejo(color)
        if not self.primero:
            self.primero = nuevo_azulejo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_azulejo

class Piso:
    def __init__(self, nombre, R, C, F, S):
        self.nombre = nombre
        self.R = R
        self.C = C
        self.F = F
        self.S = S
        self.patrones = ListaEnlazada()

    def agregar_patron(self, patron):
        self.patrones.insertar(patron)

class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None

class ListaEnlazada:
    def __init__(self):
        self.head = None

    def insertar(self, data):
        nuevo_nodo = Nodo(data)
        if self.head is None:
            self.head = nuevo_nodo
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = nuevo_nodo

    # Método para mostrar la lista enlazada
    def mostrar(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

# Función para cargar el archivo XML y almacenar los datos en listas enlazadas
def cargar_datos_desde_archivo(nombre_archivo):
    return cargar_archivo_xml(nombre_archivo)

# Función para cargar el archivo XML
def cargar_archivo_xml(nombre_archivo):
    try:
        ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()

        pisos = ListaEnlazada()  # Lista enlazada para almacenar los pisos

        for piso_xml in root.findall('piso'):
            nombre = piso_xml.get('nombre')
            R = int(piso_xml.find('R').text)
            C = int(piso_xml.find('C').text)
            F = int(piso_xml.find('F').text)
            S = int(piso_xml.find('S').text)

            piso = Piso(nombre, R, C, F, S)

            patrones_xml = piso_xml.find('patrones')
            for patron_xml in patrones_xml.findall('patron'):
                codigo = patron_xml.get('codigo')
                patron_str = patron_xml.text.strip()
                patron = Patron(codigo)
                for letra in patron_str:
                    patron.agregar_azulejo(letra)
                piso.agregar_patron(patron)

            pisos.insertar(piso)

        return pisos
    except FileNotFoundError:
        print("El archivo especificado no se encontró.")
        return None
    except ET.ParseError:
        print("Error al parsear el archivo XML.")
        return None
   

def mostrar_menu_principal():
    print("\nMenú Principal:")
    print("1. Cargar archivo XML")
    print("2. Mostrar Patrón Gráfico")
    print("3. Cambiar Patrón")
    print("4. Mostrar Todos los Pisos")
    print("5. Salir")


def main():
    lista_pisos = ListaEnlazada()  #lista enlazada para almacenar pisos
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
          
            nombre_archivo = input("Ingrese el nombre del archivo XML: ")
            datos_pisos = cargar_datos_desde_archivo(nombre_archivo)
            if datos_pisos:
                print("Archivo cargado correctamente.")
            else:
                print("No se pudo cargar el archivo.")
        elif opcion == "2":
           
            print("Mostrando patrón gráfico...")
        elif opcion == "3":
            
            print("Cambiando patrón...")
        elif opcion == "4":
            
            print("Mostrando todos los pisos...")
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")


