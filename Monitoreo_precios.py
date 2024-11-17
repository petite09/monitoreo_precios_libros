# Obtener el HTML de las páginas de libros

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


# Función para obtener el HTML de una página
def obtener_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error al obtener la página: {response.status_code} para la URL: {url}")
        return None

# Función para extraer el precio del script que contiene dataLayer
def extraer_precio(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Buscar el script que contiene dataLayer
    script_tag = soup.find('script', string=re.compile('dataLayer'))

    if script_tag:
        # Usar una expresión regular para extraer el precio del script
        match = re.search(r"'precio_producto':\s*'(\d+)'", script_tag.string)
        if match:
            precio = match.group(1)  # Captura el valor del precio
            return int(precio)
        else:
            print("No se pudo encontrar el precio en el script.")
            return None
    else:
        print("No se encontró el script de dataLayer.")
        return None

# Función para registrar el precio en un archivo CSV
def registrar_precio(libro, precio):
    fecha = datetime.now().strftime('%Y-%m-%d')
    data = {'Fecha': [fecha], 'Libro': [libro], 'Precio': [precio]}

    df = pd.DataFrame(data)

    # Guardar o añadir al archivo CSV
    try:
        df_existing = pd.read_csv('precios_libros.csv')
        df = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv('precios_libros.csv', index=False)

# Lista de URLs de los libros en Buscalibre
libros = [
    {"titulo": "Entremuros", "url": "https://www.buscalibre.cl/libro-entremuros/9789878474458/p/54393883"},
    {"titulo": "El pájaro que bebe lágrimas", "url": "https://www.buscalibre.cl/libro-el-pajaro-que-bebe-lagrimas-n-01-04-el-corazon-del-naga/9788445017098/p/62013231"},
    {"titulo": "La era del mito", "url": "https://www.buscalibre.cl/libro-la-era-del-mito/9789583056949/p/50543764"},
    {"titulo": "El límite del cielo", "url": "https://www.buscalibre.cl/libro-el-limite-del-cielo/9788410163171/p/56764769"}
]

# Iterar sobre cada URL y procesar los datos
for libro in libros:
    html = obtener_html(libro["url"])
    if html:
        precio = extraer_precio(html)
        if precio:
            registrar_precio(libro["titulo"], precio)
            print(f"El precio de '{libro['titulo']}' es: {precio}")
        else:
            print(f"No se pudo extraer el precio para el libro: {libro['titulo']}")
    else:
        print(f"No se pudo obtener el HTML para el libro: {libro['titulo']}")



