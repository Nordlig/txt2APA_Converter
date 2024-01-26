import os

def procesar_cadena(cadena):
    # Lista de preposiciones y artículos que queremos detectar y convertir a minúsculas
    preposiciones_articulos = ['a', 'an', 'and', 'the', 'in', 'on', 'at', 'by', 'for', 'with', 'to', 'of']
    cadena.capitalize()
    # Dividir la cadena en palabras
    palabras = cadena.split()

    # Procesar cada palabra
    resultado = []
    for palabra in palabras:
        # Convertir a minúsculas si es una preposición o artículo
        if palabra.lower() in preposiciones_articulos:
            resultado.append(palabra.lower())
        else:
            # Capitalizar la primera letra en caso contrario
            resultado.append(palabra.capitalize())

    # Unir las palabras procesadas en una cadena
    resultado_cadena = ' '.join(resultado)

    return resultado_cadena

def directorio_de_trabajo():
    # Obtiene la ruta del archivo .py actual
    file_path_actual = os.path.abspath(__file__)

    # Obtiene el directorio del archivo .py
    current_directory = os.path.dirname(file_path_actual)

    # Establece el directorio de trabajo actual al directorio del archivo .py
    os.chdir(current_directory)

    # Devuelve el directorio de trabajo actual
    return os.getcwd()


def procesar_archivo(nombre_archivo):
    datos_totales = []  # Lista para almacenar los diccionarios de claves y valores
    datos_actual = {}   # Diccionario actual

    claves_permitidas = ["AU", "PY", "TI", "SO", "VL", "IS", "BP", "EP", "DE", "ID", "EC", "FN", "VR", "PT", "AF", "DT", "PD", "AR", "DI", "EA", "WC", "SC", "ER", "SE"]

    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            partes = linea.split(None, 1)
            if len(partes) > 1:
                clave, valor = partes
            else:
                clave, = partes
                valor = ""

            if clave == 'PT':
                # Inicia un nuevo diccionario solo si no estamos ya dentro de uno
                if not datos_actual:
                    datos_actual = {'PT': valor}
            elif clave == 'ER':
                # Finaliza el diccionario actual solo si estamos dentro de uno
                if datos_actual:
                    datos_actual['ER'] = valor
                    datos_totales.append(datos_actual)
                    datos_actual = {}
            elif clave in claves_permitidas:

                # Procesa las claves permitidas y almacena los valores en el diccionario actual si estamos dentro de uno
                if datos_actual:
                    if clave == "AU":
                        autores = [autor.strip() for autor in valor.split('\n') if autor.strip()]
                        autores_formateados = []
                        
                        for autor in autores:
                            partes = autor.split(', ')
                            if len(partes) == 2:
                                apellido, nombres = partes
                                autores_formateados.append(f"{apellido}, {nombres}")
                            else:
                                autores_formateados.append(autor)
                        
                        valor = '; '.join(autores_formateados)



                    if clave in ["DE", "ID"]:
                        valor = valor.lower()
                        # Agregar corchetes a cada palabra o frase separada por comas
                        palabras = [f'[{p.strip()}] ' for p in valor.split(';')]
                        # Unir las palabras sin punto y coma y quitar corchetes adicionales
                        valor = ''.join(palabras)


                    if clave == "SO":
                        valor = procesar_cadena(valor)

                    datos_actual[clave] = valor

    # Agregar el último diccionario si hay uno pendiente
    if datos_actual:
        datos_totales.append(datos_actual)

    print(datos_totales, "\n\n")
    return datos_totales


def exportar_a_archivo(datos_totales, nombre_archivo_salida='newrefs.txt'):
    with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo_salida:
        for datos in datos_totales:
            for clave, valor in datos.items():
                linea = f"{clave}: {valor}\n"
                if clave == 'ER':
                    linea = f"{clave}: {valor}\n\n"

                archivo_salida.write(linea)  # Separador entre diccionarios



if __name__ == "__main__":
    try:
        # Llama a la función para establecer el directorio de trabajo actual
        directorio_de_trabajo_actual = directorio_de_trabajo()

        # Reemplaza 'ruta/al/archivo.txt' con la ruta real de tu archivo
        ruta_del_archivo = "biblio2.txt"
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