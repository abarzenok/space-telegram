import requests


def main():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    image_name = "hubble.jpg"

    response = requests.get(image_url)
    response.raise_for_status()

    with open(image_name, "wb") as file:
        file.write(response.content)


if __name__ == '__main__':
    main()
