def leer_archivo(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contenido = file.read()
    return contenido

def analizar_datos(contenido):
    articulos = []
    articulo_actual = {}

    lineas = contenido.split('\n')
    
    for linea in lineas:
        if not linea.strip():
            continue  # Ignorar líneas en blanco
        elif linea.startswith("PT"):
            if articulo_actual:
                articulos.append(articulo_actual)
                articulo_actual = {}
        else:
            partes = linea.split(maxsplit=1)
            clave = partes[0].strip()
            valor = partes[1].strip() if len(partes) > 1 else ""

            if clave == 'AU':
                if clave in articulo_actual:
                    articulo_actual[clave].append(valor)
                else:
                    articulo_actual[clave] = [valor]
            elif clave in articulo_actual:
                articulo_actual[clave] += f' {valor}'
            else:
                articulo_actual[clave] = valor
    
    if articulo_actual:
        articulos.append(articulo_actual)
    
    return articulos

def main():
    file_path = 'biblio2.txt'
    contenido = leer_archivo(file_path)
    articulos = analizar_datos(contenido)
    
    for articulo in articulos:
        print(articulo)

if __name__ == "__main__":
    main()
