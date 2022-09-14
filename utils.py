import os

# Función rápida para la construcción de una matriz
def create_matrix(size, defValue = None):
    handle = []
    for _ in range(0, size):
        handle.append([defValue] * size)
    return handle

# Función para la representación en el sistema de una ubicación de una imagen
def get_url_image(image_url):
    return os.path.join(os.path.abspath(os.getcwd()), 'images', image_url)
