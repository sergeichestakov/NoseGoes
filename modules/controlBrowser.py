from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Browser:

    new_tabs = ["https://developer.mozilla.org/en-US/", "https://stackoverflow.com/", "https://www.reddit.com/", "https://news.ycombinator.com/"]
    default_site = "https://en.wikipedia.org/wiki/Main_Page"
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.maximize_window()
        self.populate()

    def populate(self):
        main_window = self.browser.current_window_handle
        self.browser.execute_script("window.location.href = '" + self.default_site + "'")

        #Open new tabs
        for tab in Browser.new_tabs:
            javascript = "window.open('" + tab + "');"
            self.browser.execute_script(javascript)
            sleep(0.2)

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
        maxIndex = len(self.browser.window_handles) - 1
        if(direction == 'left'):
            return currIndex - 1 if currIndex > 0 else maxIndex
        elif(direction == 'right'):
            return currIndex + 1 if currIndex < maxIndex else 0

    def getScroll(self, direction):
        return {
            'up': -500,
            'down': 500
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
