import os
from pathlib import Path
from urllib import parse
import requests
from dotenv import load_dotenv
import telegram
from pathlib import Path




def download_image(image_url, image_dir, image_name, params=None):
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
    images_urls = []

    images_apis = {
        "spacex": "https://api.spacexdata.com/v4/launches",
        "nasa_apod": "https://api.nasa.gov/planetary/apod",
        "nasa_epic": "https://api.nasa.gov/EPIC/api/natural"
    }
    if source == "spacex":
        launches_url = images_apis["spacex"] # TODO: parametrize as function argument
        response = requests.get(launches_url)
        response.raise_for_status()
        launches = response.json()

        for launch in launches:
            if launch.get("links").get("flickr").get("original"):
                images_urls = launch["links"]["flickr"]["original"]  # TODO: try to access dict only once, seems with break statement
                break

    elif source == "nasa_apod":
        nasa_url = images_apis["nasa_apod"]
        params = {
            "api_key": os.getenv("API_KEY_NASA"),
            "count": 10,  # parametrize via argparse
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

        for photo in photos: #limit to 10
            timestamp = photo["image"].split("_")[-1]
            year = timestamp[0:4]
            month = timestamp[4:6]
            day = timestamp[6:8]
            photo_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{photo['image']}.png" #naming
            images_urls.append(photo_url)

    return images_urls


def get_file_extension_from_url(url):
    unquoted_url_path = parse.unquote(parse.urlsplit(url).path)
    file_name = os.path.split(unquoted_url_path)[-1]
    return os.path.splitext(file_name)[-1]


def fetch_spacex_last_launch():
    image_dir = "images\\spacex"
    image_name = "spacex{}{}"
    images_urls = get_images_urls("spacex")
    for index, image_url in enumerate(images_urls, start=1):
        file_extension = get_file_extension_from_url(image_url)
        if not file_extension:
            continue
        download_image(
            image_url=image_url,
            image_dir=image_dir,
            image_name=image_name.format(index, file_extension),
        )


def fetch_nasa_images():
    image_dir = "images\\nasa_apod"
    image_name = "nasa_apod{}{}"
    images_urls = get_images_urls("nasa_apod")
    params = {
        "api_key": os.getenv("API_KEY_NASA"),
    }
    for index, image_url in enumerate(images_urls, start=1):
        download_image(
            image_url=image_url,
            image_dir=image_dir,
            image_name=image_name.format(index, get_file_extension_from_url(image_url)), params=params
        )


def fetch_nasa_epic_images():
    image_dir = "images\\nasa_epic"
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
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
