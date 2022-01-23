import os
from pathlib import Path
import requests


def download_image(image_url, image_dir, image_name):
    full_path = os.path.join(image_dir, image_name)
    Path(image_dir).mkdir(exist_ok=True)

    response = requests.get(image_url)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


def main():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    image_dir = "images"
    image_name = "hubble.jpg"

    download_image(
        image_url=image_url,
        image_dir=image_dir,
        image_name=image_name,
    )


if __name__ == '__main__':
    main()
