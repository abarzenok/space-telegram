import requests
from main import get_images_urls, get_file_extension_from_url, IMAGES_DIRECTORY, download_image


def fetch_spacex_last_launch():
    image_name = "spacex{}{}"
    images_urls = get_images_urls("spacex")
    for index, image_url in enumerate(images_urls, start=1):
        file_extension = get_file_extension_from_url(image_url)
        if not file_extension:
            continue
        try:
            download_image(
                image_url=image_url,
                image_dir=IMAGES_DIRECTORY,
                image_name=image_name.format(index, file_extension),
            )
        except requests.HTTPError:
            continue
        except requests.ConnectionError:
            continue


if __name__ == '__main__':
    fetch_spacex_last_launch()
