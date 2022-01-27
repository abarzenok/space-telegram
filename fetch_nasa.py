"""
This module downloads NASA images
"""
import os
from pathlib import Path
import datetime
from dotenv import load_dotenv
import requests
from download_utils import download_images
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

    Path(IMAGES_DIRECTORY).mkdir(exist_ok=True)
    params = {"api_key": api_key}
    download_images(
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

    Path(IMAGES_DIRECTORY).mkdir(exist_ok=True)
    download_images(
        images_urls,
        IMAGES_DIRECTORY,
        image_name,
        request_params=params
    )


def main():
    """Run images download from NASA's APIs"""
    load_dotenv()
    nasa_api_key = os.getenv("API_KEY_NASA")
    fetch_nasa_apod_images(nasa_api_key)
    fetch_nasa_epic_images(nasa_api_key)


if __name__ == "__main__":
    main()
