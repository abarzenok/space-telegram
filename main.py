"""
This module launches Telegram bot sender
"""
import os
import time
import random
from dotenv import load_dotenv
import telegram


SEC_IN_24_HRS = "86400"
IMAGES_DIRECTORY = "images"


def main():
    """Start Telegram bot to send photos"""
    load_dotenv()
    telegram_bot = telegram.Bot(token=os.getenv("API_KEY_TG"))
    telegram_send_timeout = int(os.getenv("POST_DELAY_SECONDS", SEC_IN_24_HRS))
    telegram_send_candidates = []

    for file in os.listdir(IMAGES_DIRECTORY):
        if os.path.isfile(os.path.join(IMAGES_DIRECTORY, file)):
            telegram_send_candidates.append(file)

    while True:
        photo_to_send = os.path.join(
            IMAGES_DIRECTORY,
            random.choice(telegram_send_candidates)
        )
        with open(photo_to_send, "rb") as photo:
            telegram_bot.send_photo(
                chat_id=os.getenv('TG_CHAT_ID'),
                photo=photo,
            )
            time.sleep(telegram_send_timeout)


if __name__ == "__main__":
    main()
