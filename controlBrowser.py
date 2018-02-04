from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

browser = webdriver.Firefox()
browser.get("https://www.google.com/")

for tab in range(3):
    sleep(1)
    browser.execute_script('''window.open("http://bing.com","_blank");''')

main_window = browser.current_window_handle

sleep(2)
browser.close()
browser.quit()
