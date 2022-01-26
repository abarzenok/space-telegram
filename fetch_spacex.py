import requests
from download_utils import create_images_directory, download_images_from_list
from main import IMAGES_DIRECTORY


def fetch_spacex_last_launch():
    images_api = "https://api.spacexdata.com/v4/launches"
    image_name = "spacex{}{}"
    images_urls = []
    response = requests.get(images_api)
    response.raise_for_status()
    launches = response.json()

    for launch in launches:
        images_urls = launch.get("links").get("flickr").get("original")
        if images_urls:
            break

    create_images_directory(IMAGES_DIRECTORY)
    download_images_from_list(
        images_urls,
        IMAGES_DIRECTORY,
        image_name,
        request_params=None
    )


if __name__ == '__main__':
    fetch_spacex_last_launch()
