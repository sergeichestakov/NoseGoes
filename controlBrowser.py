from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Browser:

    default_site = "https://stackoverflow.com/"
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.get(Browser.default_site)
        #self.populate()

    def populate(self):
        for tab in range(3):
            sleep(1)
            self.browser.execute_script('''window.open("http://bing.com","_blank");''')

    def scroll(self):
        javascript = "window.scroll(0, window.innerHeight);"

        for down in range(10):
        	self.browser.execute_script(javascript)


    def close(self):
        sleep(5)
        self.browser.close()
        self.browser.quit()


if __name__ == "__main__":
    browser = Browser()

    browser.scroll()
    browser.close()
