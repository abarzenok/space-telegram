"""
This module downloads NASA images
"""
import os
import datetime
from dotenv import load_dotenv
import requests
from download_utils import create_images_directory, download_images_from_list
from main import IMAGES_DIRECTORY


def fetch_nasa_apod_images(api_key):
    """Get and download random list of NASA APOD pictures"""
    images_api = "https://api.nasa.gov/planetary/apod"
    image_name = "nasa_apod{}{}"
    images_urls = []
    params = {
        "api_key": api_key,
        "count": 50,
    }
    response = requests.get(images_api, params=params)
    response.raise_for_status()
    photos = response.json()

    for photo in photos:
        images_urls.append(photo.get("url"))

    create_images_directory(IMAGES_DIRECTORY)
    params = {"api_key": api_key}
    download_images_from_list(
        images_urls,
        IMAGES_DIRECTORY,
        image_name,
        request_params=params
    )


def fetch_nasa_epic_images(api_key):
    """Get and download list of NASA EPIC images"""
    images_api = "https://api.nasa.gov/EPIC/api/natural"
    image_name = "nasa_epic{}{}"
    images_urls = []
    params = {
        "api_key": api_key,
    }
    response = requests.get(images_api, params=params)
    response.raise_for_status()
    photos = response.json()

    for photo in photos:
        download_url = "https://api.nasa.gov/EPIC/archive/natural"
        photo_date = datetime.datetime.fromisoformat(photo["date"])
        year = photo_date.year
        month = "{:02d}".format(photo_date.month)
        day = "{:02d}".format(photo_date.day)
        photo_url = f"{download_url}/{year}/{month}/{day}/png/{photo['image']}.png"
        images_urls.append(photo_url)

    create_images_directory(IMAGES_DIRECTORY)
    download_images_from_list(
        images_urls,
        IMAGES_DIRECTORY,
        image_name,
        request_params=params
    )


if __name__ == '__main__':
    load_dotenv()
    API_KEY_NASA = os.getenv("API_KEY_NASA")
    fetch_nasa_apod_images(API_KEY_NASA)
    fetch_nasa_epic_images(API_KEY_NASA)
