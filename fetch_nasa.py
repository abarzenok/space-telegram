import os
from dotenv import load_dotenv
from main import get_images_urls, get_file_extension_from_url, IMAGES_DIRECTORY, download_image,create_images_directory
import requests


def fetch_nasa_apod_images(api_key):
    image_name = "nasa_apod{}{}"
    images_urls = get_images_urls("nasa_apod")
    params = {
        "api_key": api_key,
    }
    create_images_directory(IMAGES_DIRECTORY)
    for index, image_url in enumerate(images_urls, start=1):
        file_extension = get_file_extension_from_url(image_url)
        if not file_extension:
            continue
        try:
            download_image(
                image_url=image_url,
                image_dir=IMAGES_DIRECTORY,
                image_name=image_name.format(
                    index,
                    get_file_extension_from_url(image_url)
                ),
                params=params
            )
        except requests.HTTPError:
            continue
        except requests.ConnectionError:
            continue


def fetch_nasa_epic_images(api_key):
    image_dir = "images"
    image_name = "nasa_epic{}{}"
    images_urls = get_images_urls("nasa_epic")
    params = {
        "api_key": api_key,
    }
    create_images_directory(IMAGES_DIRECTORY)
    for index, image_url in enumerate(images_urls, start=1):
        file_extension = get_file_extension_from_url(image_url)
        if not file_extension:
            continue
        try:
            download_image(
                image_url=image_url,
                image_dir=image_dir,
                image_name=image_name.format(
                    index,
                    get_file_extension_from_url(image_url)
                ),
                params=params
            )
        except requests.HTTPError:
            continue
        except requests.ConnectionError:
            continue


if __name__ == '__main__':
    load_dotenv()
    API_KEY_NASA = os.getenv("API_KEY_NASA")
    fetch_nasa_apod_images(API_KEY_NASA)
    fetch_nasa_epic_images(API_KEY_NASA)
