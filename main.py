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


def create_images_directory(directory_path):
    Path(directory_path).mkdir(exist_ok=True)


def download_image(image_url, image_dir, image_name, params=None):
    """Download image to specified directory and return None."""
    if not image_url:
        return
    full_path = os.path.join(image_dir, image_name)

    response = requests.get(image_url, params=params)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


def get_file_extension_from_url(url):
    """Get extension of a file and return it as str (e.g. '.txt', '.jpeg' etc.)"""
    unquoted_url_path = parse.unquote(parse.urlsplit(url).path)
    file_name = os.path.split(unquoted_url_path)[-1]
    return os.path.splitext(file_name)[-1]


def main():
    load_dotenv()
    telegram_bot = telegram.Bot(token=os.getenv("API_KEY_TG"))
    telegram_send_timeout = int(os.getenv("POST_DELAY_SECONDS"), SECONDS_IN_24_HOURS)
    telegram_send_candidates = []

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
