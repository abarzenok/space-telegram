"""Module includes helpful functions for photos downloading."""
import os
from urllib import parse
import requests


def get_file_extension_from_url(url):
    """Get extension of a file and return it as str (e.g. '.jpg')"""
    unquoted_url_path = parse.unquote(parse.urlsplit(url).path)
    file_name = os.path.split(unquoted_url_path)[-1]
    return os.path.splitext(file_name)[-1]


def download_image(image_url, image_dir, image_name, params=None):
    """Download image to specified directory and return None."""
    full_path = os.path.join(image_dir, image_name)

    response = requests.get(image_url, params=params)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


def download_images(images_urls, images_directory, image_name,
                    request_params=None):
    """Go through the list and try to download every photo in it"""
    for index, image_url in enumerate(images_urls, start=1):
        file_extension = get_file_extension_from_url(image_url)
        if not file_extension:
            continue
        try:
            download_image(
                image_url=image_url,
                image_dir=images_directory,
                image_name=image_name.format(index, file_extension),
                params=request_params
            )
        except requests.HTTPError:
            continue
        except requests.ConnectionError:
            continue
