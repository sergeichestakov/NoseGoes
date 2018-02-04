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

    def run(self):
        #Scroll up and down just for funsies
        while(True):
            self.scroll()
            sleep(2)
            self.scroll(False)
            sleep(2)

    def switchTabs(self):
        handles = self.browser.window_handles
        #Loop through the tabs
        for handle in handles:
            sleep(1)
            self.browser.switch_to_window(handle)

    def scroll(self, down=True):
        scrollValue = 1000 if down else -1000
        javascript = "window.scrollBy(0," + str(scrollValue) + ");"

        self.browser.execute_script(javascript)


    def close(self):
        sleep(10)
        self.browser.close()
        self.browser.quit()


if __name__ == "__main__":
    browser = Browser()
    browser.run()
    browser.close()
