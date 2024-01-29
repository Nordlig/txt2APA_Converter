import os

def procesar_cadena(cadena):
    # Lista de preposiciones y artículos que queremos detectar y convertir a minúsculas
    preposiciones_articulos = ['a', 'an', 'and', 'the', 'in', 'on', 'at', 'by', 'for', 'with', 'to', 'of', 'e']

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

def informacion_procesada(ruta_del_archivo):
    # Abre el archivo en modo lectura
    with open("biblio.txt", "r") as archivo:
        # Inicializa una lista para almacenar los diccionarios
        lista_diccionarios = []
        # Inicializa el diccionario actual para almacenar los datos entre PT y ER
        diccionario_actual = {}
        # Inicializa la clave_actual fuera del bucle for
        clave_actual = None
        # Itera sobre cada línea del archivo
        for linea in archivo:
            # Elimina espacios en blanco al principio y al final de la línea
            linea = linea.strip()

            # Verifica si la línea comienza con palabras de dos letras en mayúsculas
            if len(linea) >= 2 and linea[:2].isalpha() and linea[:2].isupper():
                # Establece la palabra como clave y elimina espacios
                clave_actual = linea[:2].strip()
                # Verifica si también hay un valor en la misma línea
                if len(linea) > 2:
                    valor_actual = linea[2:].strip()
                    # Inicializa la clave en el diccionario actual si no existe
                    diccionario_actual.setdefault(clave_actual, "")
                    # Agrega los valores a la clave actual en el diccionario actual
                    diccionario_actual[clave_actual] += " " + valor_actual
                else:
                    diccionario_actual[clave_actual] = ""
            elif clave_actual is not None:
                # Si no es una clave, asume que es un valor y lo agrega al valor actual del diccionario actual
                diccionario_actual.setdefault(clave_actual, "")  # Inicializa la clave si no existe
                diccionario_actual[clave_actual] += " " + linea

            # Cierra el diccionario actual cuando se encuentra la clave "ER"
            if clave_actual == "ER":
                # Verifica si las claves obligatorias tienen valores
                if all(diccionario_actual.get(clave, "") != "" for clave in ["AU", "PY", "TI", "SO", "VL", "BP", "EP"]):
                    # Convierte DE e ID a minúsculas y ajusta el formato de los valores
                    diccionario_actual["DE"] = ['[{}]'.format(valor.strip().replace('\'', '').lower()) for valor in diccionario_actual.get("DE", "").split(";") if valor.strip()]
                    diccionario_actual["ID"] = ['[{}]'.format(valor.strip().replace('\'', '').lower()) for valor in diccionario_actual.get("ID", "").split(";") if valor.strip()]
                    #print(diccionario_actual)
                    
                    # Agrega el diccionario actual a la lista de diccionarios
                    lista_diccionarios.append(diccionario_actual)
                # Restablece el diccionario actual a un diccionario vacío
                diccionario_actual = {}

        # Elimina las claves no deseadas de cada diccionario en la lista
        claves_permitidas = ["AU", "PY", "TI", "SO", "VL", "IS", "BP", "EP", "DE", "ID", "ER"]
        for diccionario in lista_diccionarios:
            for key in list(diccionario.keys()):
                if key not in claves_permitidas:
                    del diccionario[key]

        # Agrega un punto al final de cada valor en la clave "AU" y cuenta el número de autores
        for diccionario in lista_diccionarios:
            if 'AU' in diccionario:
                autores = diccionario['AU'].split()
                autores_formateados = []

                i = 0
                while i < len(autores):
                    # Manejar apellido compuesto
                    apellido = autores[i]
                    siguiente = autores[i + 1]

                    if ',' in siguiente:
                        apellido += f" {siguiente}"
                        i += 1  # Saltar siguiente elemento en caso de apellido compuesto

                    iniciales = autores[i + 1]
                    iniciales_formateadas = '.'.join(iniciales)

                    autor_formateado = f"{apellido} {iniciales_formateadas}."
                    autores_formateados.append(autor_formateado)

                    i += 2  # Avanzar dos posiciones para pasar al siguiente autor

                # Agregar ", &" entre los autores si hay más de uno
                if len(autores_formateados) > 1:
                    diccionario['AU'] = ', & '.join(autores_formateados)
                else:
                    diccionario['AU'] = autores_formateados[0]

        return lista_diccionarios

def formatear_autores(autor):
    # Divide los autores por ', &'
    autores = autor.split(', &')
    
    # Formatea cada autor
    autores_formateados = []

    # Une los autores formateados con ', &'
    return ', & '.join(autores_formateados) if len(autores_formateados) > 1 else autores_formateados[0]


def exportar_a_archivo(datos, nombre_archivo_salida='newrefs.txt'):
    with open(nombre_archivo_salida, 'w') as archivo_salida:
        for diccionario in datos:
            # Extrae los valores de las claves en el orden deseado
            #autor = formatear_autores(diccionario.get('AU', '').strip())
            autor = diccionario.get('AU', '').strip()            
            #print(autor)
            year = diccionario.get('PY', '').strip()
            titulo = diccionario.get('TI', '').strip()
            journal = diccionario.get('SO', '').strip().lower()
            volumen = diccionario.get('VL', '').strip()
            issue = diccionario.get('IS', '').strip()
            primera_pagina = diccionario.get('BP', '').strip()
            ultima_pagina = diccionario.get('EP', '').strip()
            keywords = diccionario.get('DE', '')
            identificador = diccionario.get('ID', '')         

            # Para 'DE', que es una lista
            keywords = diccionario.get('DE', '')
            if isinstance(keywords, list):
                keywords = ', '.join([str(valor).strip() for valor in keywords])
            else:
                keywords = str(keywords).strip()

            # Para 'ID', que es una lista
            identificador = diccionario.get('ID', '')
            if isinstance(identificador, list):
                identificador = ', '.join([str(valor).strip() for valor in identificador])
            else:
                identificador = str(identificador).strip()
            
            
            # Elimina corchetes y comillas simples del keywords y quita las comas en DE
            keywords = ''.join([valor.strip("''") for valor in keywords.split(",")])
            # Elimina corchetes y comillas simples del identificador y quita las comas en ID
            identificador = ''.join([valor.strip("''") for valor in identificador.split(",")])

            journal = procesar_cadena(journal)

            # Escribe la línea en el archivo
            linea = f"{autor} ({year}). {titulo}. {journal}. {volumen}({issue}), {primera_pagina}-{ultima_pagina}. {keywords} {identificador}\n"
            archivo_salida.write(linea)

if __name__ == "__main__":

    try:
        # Reemplaza 'biblio.txt' con la ruta de su archivo
        ruta_del_archivo = "biblio.txt"
        informacion_procesada_resultado = informacion_procesada(ruta_del_archivo)

        # Exportar a un nuevo archivo
        exportar_a_archivo(informacion_procesada_resultado)

    except FileNotFoundError:
        print("biblio.txt no encontrado en el directorio actual. Por favor, verifica la existencia del archivo.")
        current_directory = os.getcwd()
        # Obtén la lista de archivos en el directorio actual
        files_in_directory = os.listdir(current_directory)
        # Muestra los archivos en el directorio actual
        print("Los archivos encontrados son:", files_in_directory)

    except Exception as e:
        print(f"Se produjo un error: {e}")