from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Browser:

    new_tab = "https://developer.mozilla.org/en-US/"
    default_site = "https://stackoverflow.com/"
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.execute_script("window.location.href = '" + self.default_site + "'")
        self.populate()

    def populate(self):
        javascript = "window.open('" + Browser.new_tab + "');"
        main_window = self.browser.current_window_handle

        #Open new tabs
        for tab in range(4):
            sleep(1)
            self.browser.execute_script(javascript)
        #Switch back to original tab
        self.browser.switch_to_window(main_window)

    def run(self):
        while(True):
            sleep(2)
            self.switchTabs('right')
            sleep(2)
            self.switchTabs('left')

    #Switch tabs left and right: direction should be 'left' or 'right'
    def switchTabs(self, direction):
        tabs = self.browser.window_handles
        currTab = self.browser.current_window_handle
        currIndex = tabs.index(currTab)

        newIndex = self.getNewIndex(currIndex, direction)

        self.browser.switch_to_window(tabs[newIndex])

    def getNewIndex(self, currIndex, direction):
        length = len(self.browser.window_handles)
        if(direction == 'left'):
            return currIndex - 1 if currIndex > 0 else length - 1
        elif(direction == 'right'):
            return currIndex + 1 if currIndex < length - 1 else 0

    def getScroll(self, direction):
        return {
            'up': -1000,
            'down': 1000
        }[direction]

    #Scrolls up and down the page: direction should be 'up' or 'down'
    def scroll(self, direction):
        scrollValue = self.getScroll(direction)
        javascript = "window.scrollBy(0," + str(scrollValue) + ");"

        self.browser.execute_script(javascript)

    def close(self):
        sleep(10)
        self.browser.close()
        self.browser.quit()

def main():
    browser = Browser()
    browser.run()
    browser.close()

if __name__ == "__main__":
    main()
