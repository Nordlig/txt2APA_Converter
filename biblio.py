import os
import re
import unicodedata
from tqdm import tqdm

def detectar_etiqueta_html(palabra):
    """
    Función para detectar si una palabra contiene alguna etiqueta HTML.
    """
    # Patrón de expresión regular para detectar etiquetas HTML
    patron_html = r'<\w+>.*?</\w+>'

    # Utilizar la expresión regular para buscar la palabra dentro de las etiquetas HTML
    if re.match(patron_html, palabra):
        return True
    else:
        return False

def capitalizar_despues_de_guion(palabras):
    resultado = []
    
    for palabra in palabras:
        if '-' in palabra:
            palabras_divididas = palabra.split('-')
            palabra_capitalizada = '-'.join([palabra.capitalize() for palabra in palabras_divididas])
            resultado.append(palabra_capitalizada)
            
        else:
            resultado.append(palabra.capitalize())
    
    return ' '.join(resultado)

def empieza_con_letra_griega(palabra):
    # Rangos Unicode para letras griegas
    rangos_griegos = [
        (0x0391, 0x03A9),  # Mayúsculas
        (0x03B1, 0x03C9)   # Minúsculas
    ]
    
    # Obtener el código Unicode del primer carácter
    codigo = ord(palabra[0])
    
    # Verificar si el código Unicode está en algún rango de letras griegas
    for rango in rangos_griegos:
        if rango[0] <= codigo <= rango[1]:
            return True
    
    return False
   
def not_alpha(palabra):

    palabra_comillas = ''
    encontro_primera_letra = False

    for caracter in palabra:
        if caracter.isalpha() and not encontro_primera_letra:
            palabra_comillas += caracter.upper()  # Capitalizar la primera letra alfabética
            encontro_primera_letra = True
        else:
            palabra_comillas += caracter

    return palabra_comillas

def procesar_cadena(cadena):
    # Lista de preposiciones y artículos que queremos detectar y convertir a minúsculas
    preposiciones_articulos = ['a', 'an', 'and', 'the', 'in', 'on', 'at', 'by', 'for', 'with', 
                               'to', 'of', 'e', 'about', 'above', 'across', 'after', 'against', 
                               'along', 'among', 'around', 'as', 'before', 'behind', 'below', 
                               'beneath', 'beside', 'between', 'beyond', 'despite', 'down', 
                               'during', 'except', 'from', 'inside', 'into', 'like', 'near', 
                               'off', 'onto', 'opposite', 'out', 'outside', 'over', 'past', 
                               'round', 'since', 'than', 'to', 'through', 'towards', 'under', 
                               'underneath', 'unlike', 'until', 'up', 'upon', 'via', 'within', 
                               'without', 'y', 'o', 'e', 'u']

    
    palabras = cadena.split()
    
    # Procesar cada palabra
    resultado = []
    capitalizar_siguiente = False
    palabras = capitalizar_despues_de_guion(palabras).split()
    
    for i, palabra in enumerate(palabras):
            
        if palabra.endswith(':'):
            
            if not palabra[0].isalpha() and not detectar_etiqueta_html(palabra):
                
                palabra_comillas = not_alpha(palabra)
                resultado.append(palabra_comillas)
                
            else:
                palabra_comillas = palabra.capitalize()
                resultado.append(palabra_comillas)
                
            capitalizar_siguiente = True
            
        elif palabra.startswith('<i>'):
            
            etiqueta, contenido = palabra.split('>', 1)  # Dividir la etiqueta en etiqueta y contenido
            etiqueta += '>'

            contenido = contenido.capitalize()
            resultado.append(etiqueta + contenido)  # Agregar la etiqueta y el contenido procesado como una cadena'''
            
        else:
            
            if capitalizar_siguiente:
                
                resultado.append(palabra.capitalize())
                capitalizar_siguiente = False            
                
            elif empieza_con_letra_griega(palabra):
              
                palabra_comillas = ''
                not_alpha(palabra)
                resultado.append(palabra_comillas)
            
            elif i != 0 and palabra.lower() in preposiciones_articulos and not detectar_etiqueta_html(palabra):
                
                resultado.append(palabra.lower())

            elif '-' in palabra:
                
                resultado.append(palabra)

            else:

                # Capitalizar la primera letra en caso contrario
                palabra_comillas = not_alpha(palabra)
                resultado.append(palabra_comillas)
                #resultado.append(palabra.capitalize())
    # Recorremos la lista resultado
    for i in range(len(resultado)):
        # Reemplazamos "</I>" por "</i>"
        resultado[i] = resultado[i].replace("</I>", "</i>")
        #resultado = capitalizar_despues_de_guion(resultado).split()

    # Unir las palabras procesadas en una cadena
    resultado_cadena = ' '.join(resultado)
    return resultado_cadena

def procesar_autores(autores):
    autores_formateados = []

    i = 0
    while i < len(autores):
        # Verificar si el autor es [Anonymous]
        if autores[i] == "[Anonymous]":
            autores_formateados.append("[Anonymous]")
            break

        # Manejar apellido compuesto

        # Capitalizar todos los apellidos compuestos y sepaados con "-" 
        apellido_parts = [part.strip().capitalize() for part in autores[i].split('-')]
        apellido = '-'.join(apellido_parts)

        # Verificar si hay al menos un elemento más después del apellido del autor actual
        if i + 1 < len(autores):
            siguiente = autores[i + 1]
            if ',' in siguiente:
                apellido += f" {siguiente}"
                i += 1  # Saltar siguiente elemento en caso de apellido compuesto

            # Obtener las iniciales si hay al menos un elemento más después del apellido del autor actual
            if i + 1 < len(autores):
                iniciales = autores[i + 1]

            else:
                iniciales = None
        else:
            iniciales = None

        # Verificar si hay iniciales
        if iniciales:
            iniciales_formateadas = '. '.join(iniciales)
            autor_formateado = f"{apellido} {iniciales_formateadas}."
        else:
            autor_formateado = f"{apellido}."

        autores_formateados.append(autor_formateado)

        i += 2  # Avanzar dos posiciones para pasar al siguiente autor

    return autores_formateados

def informacion_procesada(ruta_del_archivo):
        
    tags_principales = [
        "FN", "VR", "PT", "AU", "AF", "BA", "BF", "CA", "GP", "BE",
        "TI", "SO", "SE", "BS", "LA", "DT", "CT", "CY", "CL", "SP",
        "HO", "DE", "ID", "AB", "C1", "RP", "EM", "RI", "OI", "FU",
        "FX", "CR", "NR", "TC", "Z9", "U1", "U2", "PU", "PI", "PA",
        "SN", "EI", "BN", "J9", "JI", "PD", "PY", "VL", "IS", "SI",
        "PN", "SU", "MA", "BP", "EP", "AR", "DI", "D2", "EA", "EY",
        "PG", "P2", "WC", "SC", "GA", "PM", "UT", "OA", "HP", "HC",
        "DA", "ER", "EF"
    ]

    # Claves obligatorias
    claves_obligatorias = ["AU", "PY", "TI", "SO", "VL", "BP", "EP"]
    
    # Abre el archivo en modo lectura
    with open(ruta_del_archivo, "r") as archivo:
        
        # Inicializa una lista para almacenar los diccionarios
        lista_diccionarios = []
        # Inicializa el diccionario actual para almacenar los datos entre PT y ER
        diccionario_actual = {}
        # Itera sobre cada línea del archivo
        for linea in archivo:
            # Elimina espacios en blanco al principio y al final de la línea
            linea = linea.strip()
            palabras = linea.split(maxsplit=1)

            # Verifica si la línea comienza con una etiqueta principal
            if palabras and palabras[0] in tags_principales:
                # Si es una etiqueta principal, establece la clave_actual
                clave_actual = palabras[0]
                # Si hay datos después de la etiqueta, guárdalos como el valor para esa clave
                if len(palabras) > 1:
                    valor_actual = ' '.join(palabras[1:]).strip()
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
                
            if clave_actual == 'ER':

                if all(diccionario_actual.get(clave, "") != "" for clave in claves_obligatorias):
                    
                    # Procesar los autores de acuerdo al formato de entrada
                    if '\t' in diccionario_actual['AU']:
                        autores = diccionario_actual['AU'].split('\t')
                    else:
                        autores = diccionario_actual['AU'].split()

                    autores_formateados = procesar_autores(autores)

                    # Agregar ", &" entre los autores si hay más de uno
                    if len(autores_formateados) > 1:
                        diccionario_actual['AU'] = ', & '.join(autores_formateados)
                    else:
                        diccionario_actual['AU'] = autores_formateados[0]


                    # Agrega el diccionario actual a la lista de diccionarios
                    if diccionario_actual['AU'] != "[Anonymous]" and "Article" in diccionario_actual['DT']: 
                        lista_diccionarios.append(diccionario_actual)


                # Reiniciamos el diccionario actual
                diccionario_actual = {}

        # Elimina las claves no deseadas de cada diccionario en la lista
        claves_obligatorias = ["AU", "PY", "TI", "SO", "VL", "IS", "BP", "EP", "DE", "ID"]
        for diccionario in lista_diccionarios:
            for key in list(diccionario.keys()):
                if key not in claves_obligatorias:
                    del diccionario[key]

        return lista_diccionarios

def exportar_a_archivo(datos, nombre_archivo_salida='newrefs.txt'):
    with open(nombre_archivo_salida, 'w', encoding = 'ansi') as archivo_salida:

        # Odenamos alfabbeticamente los autores
        for diccionario in sorted(datos, key=lambda x: x.get('AU', '').strip()):

            # Extrae los valores de las claves en el orden deseado
            autor = diccionario.get('AU', '').strip()            
            year = diccionario.get('PY', '').strip()
            titulo = procesar_cadena(diccionario.get('TI', '').strip())
            journal = procesar_cadena(diccionario.get('SO', '').strip())
            volumen = diccionario.get('VL', '').strip()
            
            if diccionario.get('IS', ''):
                issue = f"({diccionario.get('IS', '').strip()})"
            else:
                issue = ''

            primera_pagina = diccionario.get('BP', '').strip()
            ultima_pagina = diccionario.get('EP', '').strip()
            keywords = diccionario.get('DE', '')
            identificador = diccionario.get('ID', '')  

            keywords = ' '.join([f"[{valor.strip().lower()}]" for valor in keywords.split(';') if valor.strip()]) if keywords else ''
            identificador = ' '.join([f"[{valor.strip().lower()}]" for valor in identificador.split(';') if valor.strip()]) if identificador else ''
            
            if keywords and identificador:
                linea = f"{autor} ({year}). {titulo}. {journal}, {volumen}{issue}, {primera_pagina}-{ultima_pagina}. [{keywords} {identificador}]\n\n"
            elif keywords:
                linea = f"{autor} ({year}). {titulo}. {journal}, {volumen}{issue}, {primera_pagina}-{ultima_pagina}. [{keywords}]\n\n"
            elif identificador:
                linea = f"{autor} ({year}). {titulo}. {journal}, {volumen}{issue}, {primera_pagina}-{ultima_pagina}. [{identificador}]\n\n"
            else:
                linea = f"{autor} ({year}). {titulo}. {journal}, {volumen}{issue}, {primera_pagina}-{ultima_pagina}.\n\n"
                
            archivo_salida.write(linea)
            
if __name__ == "__main__":

    try:
        # Reemplaza 'biblio.txt' con la
        #  ruta de su archivo
        ruta_del_archivo = "biblio.txt"
        informacion_procesada_resultado = informacion_procesada(ruta_del_archivo)

        # Inicializar la barra de progreso con el número total de diccionarios
        with tqdm(total=len(informacion_procesada_resultado), desc="Procesando") as pbar:
            for diccionario in informacion_procesada_resultado:
                # Actualizar la barra de progreso
                pbar.update(1)

        # Exportar a un nuevo archivo
        exportar_a_archivo(informacion_procesada_resultado)

        print("Archivo procesado correctamente.")
        
        # Esperar a que el usuario presione Enter
        #input("\nPresiona Enter para cerrar el programa.")

    except FileNotFoundError:
        print("biblio.txt no encontrado en el directorio actual. Por favor, verifica la existencia del archivo.")
        current_directory = os.getcwd()
        # Obtén la lista de archivos en el directorio actual
        files_in_directory = os.listdir(current_directory)
        # Muestra los archivos en el directorio actual
        print("Los archivos encontrados son:", files_in_directory)
        #input("Presiona Enter para cerrar el programa.")

    except Exception as e:
        print(f"Se produjo un error: {e}")
        #input("Presiona Enter para cerrar el programa.")
