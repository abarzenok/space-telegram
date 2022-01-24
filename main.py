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


def get_images_urls():
    launches_url = "https://api.spacexdata.com/v4/launches"  # TODO: parametrize as function argument
    response = requests.get(launches_url)
    response.raise_for_status()
    launches = response.json()
    images_urls = []

    for launch in launches:
        if launch.get("links").get("flickr").get("original"):
            images_urls = launch["links"]["flickr"]["original"]  # TODO: try to access dict only once
            break

    return images_urls


def fetch_spacex_last_launch():
    image_dir = "images"
    image_name = "spacex{}.jpg"
    images_urls = get_images_urls()
    for index, image_url in enumerate(images_urls, start=1):
        download_image(
            image_url=image_url,
            image_dir=image_dir,
            image_name=image_name.format(index),
        )


def main():
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
