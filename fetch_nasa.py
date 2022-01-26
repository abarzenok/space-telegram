import os
import datetime
from dotenv import load_dotenv
from main import get_file_extension_from_url, IMAGES_DIRECTORY, download_image,create_images_directory
import requests


def fetch_nasa_apod_images(api_key):
    nasa_url = "https://api.nasa.gov/planetary/apod"
    image_name = "nasa_apod{}{}"
    images_urls = []
    params = {
        "api_key": api_key,
        "count": 50, # may break
    }

    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    photos = response.json()

    for photo in photos:
        images_urls.append(photo.get("url"))

    create_images_directory(IMAGES_DIRECTORY)

    params = {
        "api_key": api_key, # duplicate
    }
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
    images_urls = []
    params = {
        "api_key": api_key,
    }
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural"

    response = requests.get(nasa_epic_url, params=params)
    response.raise_for_status()
    photos = response.json()

    for photo in photos:
        photo_date = datetime.datetime.fromisoformat(photo["date"])
        year = photo_date.year
        month = "{:02d}".format(photo_date.month)
        day = "{:02d}".format(photo_date.day)
        photo_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{photo['image']}.png"
        images_urls.append(photo_url)

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
