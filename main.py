import os
from pathlib import Path
import requests



def main():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    image_name = "hubble.jpg"
    image_dir = "images"
    full_path = os.path.join(image_dir, image_name)

    Path(image_dir).mkdir(exist_ok=True)

    response = requests.get(image_url)
    response.raise_for_status()

    with open(full_path, "wb") as file:
        file.write(response.content)


if __name__ == '__main__':
    main()
