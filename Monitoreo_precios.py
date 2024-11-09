import requests

def obtener_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.txt
    else:
        print(f"Error al obtener la página: {response.status_code}")
        return None

#URL de un libro de buscalibre