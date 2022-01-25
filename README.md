# Space Telegram
The program is a Telegram bot that sends an astronomical picture every day.

## How to install
To run the bot, the following prerequisites must be met:
1. Register a new bot and get an API key for it. Please follow the official [Telegram documentation](https://core.telegram.org/bots#6-botfather)
2. Get a NASA API key. This can be done at the [NASA APIs page](https://api.nasa.gov/#signUp)
3. Get the ID of the channel you want to send space photos to. You can see it in the channel description (for example, @your_channel_name). If you don't have one, you can create a [new Telegram channel](https://telegram.org/faq_channels#q-what-39s-a-channel).

You will then need to create a `.env` file in the same directory as the `main.py` file. And fill it in like this (without `<` and `>`, they are just for markup):
```commandline
API_KEY_NASA=<paste your NASA API key>
API_KEY_TG=<paste your Telegram API key>
TG_CHAT_ID=@your_channel_name
```
Optionally, for debugging purposes, you can add a custom Telegram message delay `POST_DELAY_SECONDS`. 
```commandline
POST_DELAY_SECONDS=10
```
The default delay is `86400` seconds, which is equal to 24 hours. It is applied when it's not specified in the `.env` file.

Python3 should already be installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

`pip install -r requirements.txt`
## Project Goals
The code is written for educational purposes on online-course for web-developers, dvmn.org.