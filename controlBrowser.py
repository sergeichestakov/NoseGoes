from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Browser:

    new_tab = "https://developer.mozilla.org/en-US/"
    default_site = "https://stackoverflow.com/"
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.get(Browser.default_site)
        self.populate()

    def populate(self):
        javascript = "window.open('" + Browser.new_tab + "');"
        main_window = self.browser.current_window_handle

        #Open new tabs
        for tab in range(3):
            sleep(1)
            self.browser.execute_script(javascript)
        #Switch back to original tab
        self.browser.switch_to_window(main_window)

    def scroll(self):
        javascript = "window.scrollBy(0, 500);"

        for down in range(15):
            sleep(1)
            self.browser.execute_script(javascript)


    def close(self):
        sleep(10)
        self.browser.close()
        self.browser.quit()


if __name__ == "__main__":
    browser = Browser()
    browser.scroll()
    browser.close()
