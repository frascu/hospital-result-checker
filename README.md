# Hospital result checker

## History
Last weekend, I took the Covid-19 test. At the end of the test, the nurse gave me a sheet of paper describing how
to check my result. There were the credentials in order to check the result on their platform.

Instead of checking manually every 5 minutes if something had been uploaded, I preferred to create this small scraper
that did everything for me. At the end, I received the document by a telegram message.

The script is general, so you can reuse with your credentials.
Of course, it can be reused to check results published by the Miulli Hospital located in Acquaviva delle Fonti 
or other hospitals that use the same platform.

## Install 
```shell
pip install -r requirements.txt
```
Make sure you have also installed [geckodriver](https://github.com/mozilla/geckodriver).

## Parameters
The parameters are:

- `--username` `-u` - provided username
- `--password` `-p` - provided password
- `--code` `-c` - provided code 
- `--telegram-bot-token` `-t` (optional) - Telegram bot token that you can generate with [BotFather](https://t.me/botfather)

### Usage
```shell
python main.py --username 123456 --password 123456 --code 123456 --telegram-bot-token 5s6r5ge2fv56wg
```

The script will remain active until the result is published.
