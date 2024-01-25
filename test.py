import os

def procesar_archivo(nombre_archivo):
    datos_totales = []  # Lista para almacenar los diccionarios de claves y valores
    clave_actual = None
    valor_actual = ""

    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            # Eliminar espacios y saltos de línea al inicio y al final de la línea
            linea = linea.strip()

            # Si la línea está vacía, continuar con la siguiente iteración
            if not linea:
                # Verificar si hay una clave anterior
                if clave_actual is not None:
                    datos[clave_actual] = valor_actual.strip()
                    clave_actual = None
                    valor_actual = ""
                continue

            # Dividir la línea en clave y valor
            partes = linea.split(None, 1)
            if len(partes) > 1:
                clave, valor = partes
            else:
                clave, = partes
                valor = ""

            # Convertir a minúsculas los valores asociados con las claves 'DE' e 'ID'
            if clave in ["DE", "ID"]:
                valor = valor.lower()

            # Capitalizar la primera letra de los valores asociados con la clave 'SO'
            if clave == "SO":
                valor = valor.capitalize()           

            # Detectar claves y valores
            if clave in ["FN", "VR", "PT", "AU", "AF", "TI", "SO", "DT", "DE", "ID", "PD", "PY", "VL", "IS", "BP", "EP", "AR", "DI", "EA", "WC", "SC", "ER", "SE", "EC"]:
                # Almacenar el valor actual en el diccionario si hay una clave anterior
                if clave_actual is not None:
                    datos = {clave_actual: valor_actual.strip()}
                    datos_totales.append(datos)

                # Iniciar una nueva clave
                clave_actual = clave
                valor_actual = valor
            else:
                # Concatenar el valor actual
                valor_actual += " " + linea

        # Almacenar el último valor después de salir del bucle si hay una clave anterior
        if clave_actual is not None:
            datos = {clave_actual: valor_actual.strip()}
            datos_totales.append(datos)
        print(datos_totales, "\n\n")
        return datos_totales


def exportar_a_archivo(datos_totales, nombre_archivo_salida='newrefs.txt'):
    with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo_salida:
        for datos in datos_totales:
            if 'PT' in datos:
                archivo_salida.write("\n")  # Agregar un salto de línea antes de la clave PT

            linea = ' '.join([f"{clave}: {valor}" for clave, valor in datos.items()])
            archivo_salida.write(linea + "\n")  # Separador entre bloques


if __name__ == "__main__":
    try:
        # Reemplaza 'ruta/al/archivo.txt' con la ruta real de tu archivo
        ruta_del_archivo = "biblio.txt"
        informacion_procesada = procesar_archivo(ruta_del_archivo)

        # Exportar a un nuevo archivo
        exportar_a_archivo(informacion_procesada, 'newrefs.txt')

    except FileNotFoundError:
        print("biblio.txt no encontrado en el directorio actual. Por favor, verifica la existencia del archivo.")

        current_directory = os.getcwd()

        # Obtén la lista de archivos en el directorio actual
        files_in_directory = os.listdir(current_directory)

        # Muestra los archivos en el directorio actual
        print("Los archivos encontrados son:", files_in_directory)

    except Exception as e:
        print(f"Se produjo un error: {e}")