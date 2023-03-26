
import os
from selenium import webdriver

# THE SYSTEM PATH WHERE DRIVER IS LOCATED
os.environ['PATH'] += r"C:\Program Files\ChromeDriver"


def start_discord_meeting(my_name='', conference_id='', conference_pass='', username='User'):

    try:
        browser = webdriver.Chrome()
        browser.get('http://discord.gg/' + conference_id)
        browser.close()
        print("Работа потока встречи завершена в штатном режиме")
        exit(0)
    except:
        print(r"Отсутствует webdriver в C:\Program Files\ChromeDriver\.")
        exit(1)
