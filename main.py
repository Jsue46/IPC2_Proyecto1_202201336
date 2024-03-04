import xml.etree.ElementTree as ET

def leer_archivo(nombre_archivo):
    try:
        tree = ET.parse(nombre_archivo)
        root = tree.getroot()
        return root
    except FileNotFoundError:
        print("El archivo especificado no se encontró.")
        return None
    except ET.ParseError:
        print("Error al parsear el archivo XML.")
        return None

def mostrar_pisos(root):
    if root is None:
        return
    
    pisos = root.findall('piso')
    for piso in pisos:
        nombre = piso.get('nombre')
        print(f"Piso: {nombre}")
        for child in piso:
            if child.tag == 'patrones':
                print("Patrones:")
                patrones = child.findall('patron')
                for patron in patrones:
                    codigo = patron.get('codigo')
                    patron_texto = patron.text.strip()
                    print(f"Código: {codigo}, Patron: {patron_texto}")

def main():
    nombre_archivo = input("Ingrese el nombre del archivo XML: ")
    root = leer_archivo(nombre_archivo)
    if root is not None:
        mostrar_pisos(root)

if __name__ == "__main__":
    main()

