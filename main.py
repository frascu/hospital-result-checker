import argparse
import os
import time
import telepot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def check_uploaded_document(url, with_window, username, password, code, telegram_bot_token=None):
    # set preferences
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", os.getcwd())
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.download.viewableInternally.enabledTypes", "")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/pdf;text/plain;application/text;text/xml;application/xml")
    options.set_preference("pdfjs.disabled", True)
    if not with_window:
        options.add_argument('--headless')

    # create driver
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    
    username_input = driver.find_element(by=By.ID, value='j_username')
    username_input.send_keys(username)

    username_input = driver.find_element(by=By.ID, value='j_password')
    username_input.send_keys(password)

    access_button = None
    input_buttons = driver.find_elements(by=By.XPATH, value="//input[@class='button']")
    for input_button in input_buttons:
        if input_button.get_attribute('value') == 'Accedi':
            access_button = input_button
            break

    if not access_button:
        print("Access button not found")
        driver.quit()
        return False
    else:
        access_button.click()

    print("Logging...")

    menu = driver.find_element(by=By.ID, value='bottommenu')

    search_button = menu.find_element(by=By.TAG_NAME, value='input')
    search_button.click()

    col2 = driver.find_element(by=By.XPATH, value="//div[@class='col2']")

    input_button = col2.find_elements(by=By.TAG_NAME, value='input')[0]
    input_button.send_keys(code)

    search_button = col2.find_elements(by=By.TAG_NAME, value='input')[1]
    search_button.click()

    tbody = driver.find_elements(by=By.TAG_NAME, value='tbody')[1]

    if not tbody:
        print("Document not found")
        driver.quit()
        return False

    tr_elements = tbody.find_elements(by=By.TAG_NAME, value='tr')
    for tr_element in tr_elements:
        td_elements = tr_element.find_elements(by=By.TAG_NAME, value='td')

        if len(td_elements) < 3:
            print("Document not found")
            driver.quit()
            return False

        print("Downloading...")
        download_button = td_elements[2].find_element(by=By.TAG_NAME, value='input')
        download_button.click()
        print("Document downloaded")

    driver.quit()

    if telegram_bot_token:
        bot = telepot.Bot(telegram_bot_token)

        for file in os.listdir("."):
            if file.endswith(".pdf"):
                print(file)
                bot.sendDocument(chat_id=25094661, document=open(file, 'rb'))

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', '-u', default=None, help='Username')
    parser.add_argument('--password', '-p', default=None, help='Password')
    parser.add_argument('--code', '-c', default=None, help='Code')
    parser.add_argument('--telegram-bot-token', '-t', default=None, help='Telegram Bot Token')
    args = parser.parse_args()

    # check params
    if args.username is None:
        raise ValueError('Must provide username')
    if args.password is None:
        raise ValueError('Must provide password')
    if args.code is None:
        raise ValueError('Must provide code')

    document_uploaded = False
    while not document_uploaded:
        document_uploaded = check_uploaded_document(url='https://referti.miulli.it:4430/galileo/public/menu.faces',
                                                    with_window=False,
                                                    username=args.username,
                                                    password=args.password,
                                                    code=args.code,
                                                    telegram_bot_token=args.telegram_bot_token)

        print("Waiting...")
        time.sleep(300)
    else:
        print("Document uploaded")
