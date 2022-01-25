import os
import time
import datetime
import random
from urllib import parse
from pathlib import Path
import requests
from dotenv import load_dotenv
import telegram


SECONDS_IN_24_HOURS = 86400
IMAGES_DIRECTORY = "images"


def download_image(image_url, image_dir, image_name, params=None):
    """Download image to specified directory and return None."""
    if params is None:
        params = {}
    if not image_url:
        return
    full_path = os.path.join(image_dir, image_name)
    Path(image_dir).mkdir(exist_ok=True)
    try:
        response = requests.get(image_url, params=params)
    except requests.HTTPError:
        return
    except requests.ConnectionError:
        return
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


def get_images_urls(source):
    """Get urls of images for specified source and return them as list."""
    images_apis = {
        "spacex": "https://api.spacexdata.com/v4/launches",
        "nasa_apod": "https://api.nasa.gov/planetary/apod",
        "nasa_epic": "https://api.nasa.gov/EPIC/api/natural"
    }
    images_urls = []
    if source == "spacex":
        launches_url = images_apis["spacex"]
        response = requests.get(launches_url)
        response.raise_for_status()
        launches = response.json()

        for launch in launches:
            images_urls = launch.get("links").get("flickr").get("original")
            if images_urls:
                break

    elif source == "nasa_apod":
        nasa_url = images_apis["nasa_apod"]
        params = {
            "api_key": os.getenv("API_KEY_NASA"),
            "count": 50,
        }
        response = requests.get(nasa_url, params=params)
        response.raise_for_status()
        photos = response.json()

        for photo in photos:
            images_urls.append(photo.get("url"))

    elif source == "nasa_epic":
        nasa_epic_url = images_apis["nasa_epic"]
        params = {
            "api_key": os.getenv("API_KEY_NASA"),
        }
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

    return images_urls


def get_file_extension_from_url(url):
    """Get extension of a file and return it as str (e.g. '.txt', '.jpeg' etc.)"""
    unquoted_url_path = parse.unquote(parse.urlsplit(url).path)
    file_name = os.path.split(unquoted_url_path)[-1]
    return os.path.splitext(file_name)[-1]


def fetch_spacex_last_launch():
    image_name = "spacex{}{}"
    images_urls = get_images_urls("spacex")
    for index, image_url in enumerate(images_urls, start=1):
        file_extension = get_file_extension_from_url(image_url)
        if not file_extension:
            continue
        download_image(
            image_url=image_url,
            image_dir=IMAGES_DIRECTORY,
            image_name=image_name.format(index, file_extension),
        )


def fetch_nasa_images():
    image_name = "nasa_apod{}{}"
    images_urls = get_images_urls("nasa_apod")
    params = {
        "api_key": os.getenv("API_KEY_NASA"),
    }
    for index, image_url in enumerate(images_urls, start=1):
        download_image(
            image_url=image_url,
            image_dir=IMAGES_DIRECTORY,
            image_name=image_name.format(
                index,
                get_file_extension_from_url(image_url)
            ),
            params=params
        )


def fetch_nasa_epic_images():
    image_dir = "images"
    image_name = "nasa_epic{}{}"
    images_urls = get_images_urls("nasa_epic")
    params = {
        "api_key": os.getenv("API_KEY_NASA"),
    }
    for index, image_url in enumerate(images_urls, start=1):
        download_image(
            image_url=image_url,
            image_dir=image_dir,
            image_name=image_name.format(
                index,
                get_file_extension_from_url(image_url)
            ),
            params=params
        )


def main():
    load_dotenv()
    telegram_bot = telegram.Bot(token=os.getenv("API_KEY_TG"))
    telegram_send_timeout = int(os.getenv("POST_DELAY_SECONDS")) or SECONDS_IN_24_HOURS
    telegram_send_candidates = []

    fetch_spacex_last_launch()
    fetch_nasa_images()
    fetch_nasa_epic_images()

    for file in os.listdir(IMAGES_DIRECTORY):
        if os.path.isfile(os.path.join(IMAGES_DIRECTORY, file)):
            telegram_send_candidates.append(file)

    while True:
        with open(os.path.join(
                    IMAGES_DIRECTORY,
                    random.choice(telegram_send_candidates)
        ), "rb") as photo:
            telegram_bot.send_photo(
                chat_id=os.getenv('TG_CHAT_ID'),
                photo=photo,
                )
            time.sleep(telegram_send_timeout)


if __name__ == "__main__":
    main()
