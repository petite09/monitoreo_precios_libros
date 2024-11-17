import pandas as pd
import matplotlib.pyplot as plt

def visualizar_evolucion():
    df = pd.read_csv('precios_libros.csv')

    # Convertir la columna 'Fecha' a tipo datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Agrupar por título de libro y graficar cada uno
    for libro in df['Libro'].unique():
        df_libro = df[df['Libro'] == libro]
        plt.plot(df_libro['Fecha'], df_libro['Precio'], marker='o', label=libro)

    # Configuración del gráfico
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.title('Evolución de precios de los libros')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

# Llamada a la función para visualizar el gráfico
visualizar_evolucion()