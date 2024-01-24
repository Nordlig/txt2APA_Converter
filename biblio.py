# Descomenta la línea siguiente si estás ejecutando el script en un sistema UNIX
# #!/usr/bin/env python

# -*- coding: utf-8 -*-
# Campos FN VR PT AU AF TI SO DT DE ID PD PY VL IS BP EP AR DI EA WC SC ER
__autor__ = "Ivar Bergelin"
__version__ = "1.0"
__maintainer__ = "Ivar Bergelin"
__email__ = "ivar.bergelin@gmail.com"
__status__ = "Dev"

'''Este script convierte datos bibliográficos en un archivo llamado biblio.txt en referencias bibliográficas en formato APA para ser escritas en el archivo de salida newrefs.txt'''
'''import os
import pandas as pd
biblio_list = []

# Función para convertir SO a minúsculas con la primera letra de cada palabra en mayúsculas
def convertir_so(valor):
    return ' '.join(word.capitalize() for word in valor.split())

try:
    with open("biblio.txt", "r", encoding="utf-8") as file:
        biblio_dict = {}    
        # Itera sobre cada línea del archivo
        for line in file:
            # Si la línea está vacía, significa que hemos completado un bloque
            if not line.strip():
                # Agrega el diccionario actual a la lista y reinicia para el siguiente bloque
                if biblio_dict:
                    biblio_list.append(biblio_dict)
                    biblio_dict = {}
            else:
                # Divide la línea en campo y valor usando el primer espacio en blanco
                parts = line.strip().split(" ", 1)
                
                # Asegúrate de que haya al menos dos partes antes de agregar al diccionario
                if len(parts) == 2:
                    key, value = parts
                    # Aplica la conversión especial para el campo SO
                    if key == "SO":
                        value = convertir_so(value)
                    biblio_dict[key] = biblio_dict.get(key, "") + " " + value.strip()

                elif len(parts) == 1:
                    # Si hay solo una parte, asumimos que el campo está presente pero sin valor
                    key = parts[0]
                    biblio_dict[key] = ""
                elif key == "AU" and ',' in parts[1]:
                    # Si el campo es "AU" y contiene una coma, divide el nombre del autor
                    last_name, first_names = parts[1].split(",", 1)
                    biblio_dict[key] = last_name.strip() + ", " + first_names.strip()

    # Agrega el último diccionario a la lista si hay algún bloque al final del archivo
    if biblio_dict:
        biblio_list.append(biblio_dict)
    # Imprime la lista de diccionarios resultante
    for block in biblio_list:
        # Formatea los nombres de los autores
        authors = block.get("AU", "").split("; ")
        formatted_authors = ", ".join(author.strip() for author in authors)

        # Formatea la salida del diccionario
        formatted_output = (
            f"{formatted_authors} ({block.get('PY', '')}). {block.get('TI', '')}. {block.get('SO', '')}, "
            f"{block.get('VL', '')}({block.get('IS', '')}), {block.get('BP', '')}-{block.get('EP', '')}. "
        )

        # Agrega DE (palabras clave) si presente
        keywords_de = block.get('DE', '')
        if keywords_de:
            # Transforma y agrega los corchetes
            formatted_output += " ".join([f"[{keyword.strip().lower()}]" for keyword in keywords_de.split(';')])

        # Agrega ID (palabras clave) si presente
        keywords_id = block.get('ID', '')
        if keywords_id:
            # Transforma y agrega los corchetes
            formatted_output += " ".join([f"[{keyword.strip().lower()}]" for keyword in keywords_id.split(';')])

        print(formatted_output)
        print()

except FileNotFoundError:
    print("biblio.txt no encontrado en el directorio actual. Por favor, verifica la existencia del archivo.")

    current_directory = os.getcwd()

    # Obtén la lista de archivos en el directorio actual
    files_in_directory = os.listdir(current_directory)

    # Muestra los archivos en el directorio actual
    print("Los archivos encontrados son:", files_in_directory)

except Exception as e:
    print(f"Se produjo un error: {e}")'''

import re
import os

# Lista para almacenar los diccionarios
biblio_list = []

# Diccionario actual en proceso
current_dict = {}

# Función para convertir SO a minúsculas con la primera letra de cada palabra en mayúsculas
def convertir_so(valor):
    return ' '.join(word.capitalize() for word in valor.split())

# Función para limpiar y agregar datos al diccionario
def process_line(key, value):
    # Limpia la clave
    key = key.strip()
    
    # Limpia el valor y elimina espacios en blanco al principio de cada valor
    value = ' '.join(part.strip() for part in value.split())

    # Aplica la conversión especial para el campo SO
    if key == "SO":
        value = convertir_so(value)

    # Agrega al diccionario actual
    current_dict[key] = value

try:
# Lee el archivo
    with open("biblio.txt", "r", encoding="utf-8") as file:
        for line in file:
            # Verifica si la línea comienza con una cadena de clave
            #match = re.match(r'^(\w+)\s(.+)$', line.strip())
            match = re.match(r'^([A-Z]{2})\s*(.*)$', line.strip())
            if match:
                key, value = match.groups()
                process_line(key, value)
            elif not line.strip() and current_dict:
                # Agrega el diccionario actual a la lista
                biblio_list.append(current_dict)
                # Reinicia el diccionario para el próximo bloque
                current_dict = {}

    # Agrega el último diccionario a la lista si hay algún bloque al final del archivo
    if current_dict:
        biblio_list.append(current_dict)


    # Imprime la lista de diccionarios resultante
        for block in biblio_list:
            # Formatea los nombres de los autores
            authors = block.get("AU", "").split("; ")
            formatted_authors = ", ".join(author.strip() for author in authors)

            # Formatea la salida del diccionario
            formatted_output = (
                f"{formatted_authors} ({block.get('PY', '')}). {block.get('TI', '')}. {block.get('SO', '')}. "
            f"{block.get('VL', '')}({block.get('IS')}),{block.get('BP')} -{block.get('EP')}. "
            )

            # Agrega DE (palabras clave) si presente
            keywords_de = block.get('DE', '')
            if keywords_de:
                # Transforma y agrega los corchetes
                formatted_output += "".join([f"[{keyword.strip().lower()}]" for keyword in keywords_de.split(';')])

            # Agrega ID (palabras clave) si presente
            keywords_id = block.get('ID', ' .')
            if keywords_id:
                # Transforma y agrega los corchetes
                formatted_output += "".join([f"[{keyword.strip().lower()}]" for keyword in keywords_id.split(';')])

            print(formatted_output)
            print()

except FileNotFoundError:
    print("biblio.txt no encontrado en el directorio actual. Por favor, verifica la existencia del archivo.")

    current_directory = os.getcwd()

    # Obtén la lista de archivos en el directorio actual
    files_in_directory = os.listdir(current_directory)

    # Muestra los archivos en el directorio actual
    print("Los archivos encontrados son:", files_in_directory)

except Exception as e:
    print(f"Se produjo un error: {e}")