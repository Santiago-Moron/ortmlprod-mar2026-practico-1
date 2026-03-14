import logging
import os

from bs4 import BeautifulSoup
import requests


# Configure basic logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("Scraper")


# Configuración
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def is_valid_image_url(url: str) -> bool:
    """
    Verifica si una URL corresponde a una imagen válida.

    Args:
        url: URL a verificar

    Returns:
        bool: True si la URL es válida y tiene una extensión de imagen permitida
    """
    if not url:
        return False

    # Permitir URLs relativas que empiecen con /
    if not url.startswith(("http", "/")):
        return False

    if not any(url.lower().endswith(ext) for ext in VALID_EXTENSIONS):
        return False

    return True


def download_images(url: str, target_dir: str) -> None:
    """
    Descarga todas las imágenes de la página web

    Args:
        url: URL de la página web
        target_dir: Directorio donde se guardarán las imágenes

    Returns:
        None
    """
    # Crear el directorio si no existe
    os.makedirs(target_dir, exist_ok=True)

    # Limpiar archivos existentes en el directorio
    logger.info(f"Limpiando directorio {target_dir}")
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Error al eliminar {file_path}: {e}")

    # Acceder a la página web
    logger.info(f"Descargando página {url}")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa

    # Parsear el HTML
    logger.info("Parseando HTML")
    soup = BeautifulSoup(response.content, "html.parser")
    img_tags = soup.find_all("img")

    # Descargar imágenes
    logger.info(f"Descargando {len(img_tags)} imágenes")
    n_of_downloaded_images = 0
    for i, img in enumerate(img_tags):
        img_url = img.get("src", "")
        logger.debug(f"Procesando imagen {i+1:03d}: URL = {img_url}")
        if img_url and is_valid_image_url(img_url):
            img_name = os.path.basename(img_url)
            logger.info(
                f"Descargando imagen {i+1:03d} de {len(img_tags):03d}: {img_name}"
            )
            with open(
                f"{target_dir}/{n_of_downloaded_images+1:03d}_{img_name}", "wb"
            ) as img_file:
                img_data = requests.get(img_url).content
                img_file.write(img_data)
            n_of_downloaded_images += 1
        else:
            logger.warning(f"La imagen {i+1:03d} no es válida: {img_url}")


if __name__ == "__main__":
    # Configuración
    url = "https://www.gallito.com.uy/casa-en-venta-en-pocitos-impecable-4-dormitorios-barbacoa-inmuebles-26963508"
    target_dir = "data/images"

    # Descargar imágenes
    logger.info("Iniciando descarga de imágenes")
    download_images(url, target_dir)
    logger.info("Descarga de imágenes completada")


# Docker
# docker build -t scraper .
# docker run --name scraper -v "$(pwd)/data/images:/app/data/images" scraper python scraper.py
