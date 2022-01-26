import requests
from main import get_file_extension_from_url, IMAGES_DIRECTORY, download_image, create_images_directory


def fetch_spacex_last_launch():
    images_api = "https://api.spacexdata.com/v4/launches"
    images_urls = []
    image_name = "spacex{}{}"
    response = requests.get(images_api)
    response.raise_for_status()
    launches = response.json()
    for launch in launches:
        images_urls = launch.get("links").get("flickr").get("original")
        if images_urls:
            break
    create_images_directory(IMAGES_DIRECTORY)

    for index, image_url in enumerate(images_urls, start=1): # function candidate
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
