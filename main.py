import os
from pathlib import Path
from urllib  import parse
import requests
from dotenv import load_dotenv



def download_image(image_url, image_dir, image_name):
    full_path = os.path.join(image_dir, image_name)
    Path(image_dir).mkdir(exist_ok=True)

    response = requests.get(image_url)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


def get_images_urls():  # spacex only
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


def get_file_extension_from_url(url):
    unquoted_url_path = parse.unquote(parse.urlsplit(url).path)
    file_name = os.path.split(unquoted_url_path)[-1]
    return os.path.splitext(file_name)[-1]


def fetch_spacex_last_launch():
    image_dir = "images"
    image_name = "spacex{}{}"
    images_urls = get_images_urls()
    for index, image_url in enumerate(images_urls, start=1):
        download_image(
            image_url=image_url,
            image_dir=image_dir,
            image_name=image_name.format(index, get_file_extension_from_url(image_url)),
        )


def main():
    load_dotenv()
    print(os.getenv('API_KEY_NASA'))
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
