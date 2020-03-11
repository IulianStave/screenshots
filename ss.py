""" Save a screenshot from spotify.com in current directory. 
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from os import path
from common.common import (
    get_browser,
    build_cmd_arguments,
)

OUTPUT = 'output'
DRIVERS = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    # 'edge': webdriver.Edge,
    # 'ie': webdriver.Ie,
    # 'safari': webdriver.Safari,
}

BASE_URL = 'https://atmosphere.copernicus.eu/'

DRIVER = 'chromedriver'

HEADLESS_OPTIONS = {
    'chrome': ChromeOptions,
    'firefox': FirefoxOptions
}

RESOLUTIONS = [
    (1024, 768),
    (800, 600),
    (2048, 1024),
]

sourceList = 'urls.conf'
start = ''


class ScreenShots:

    def __init__(self, sourceList):
        self.sourceList = sourceList
        self.start = ''
        # self.driver = driver
    
    def BTCscreenshot(self, suffix: str = ''):
        """ Capture a screeenshot.
            Uses `suffix` if given or the current browser url.
        """
        suffix = suffix or self._get_screenshot_suffix()
        name = '{}/screenshot_{}.png'.format(os.getcwd(), suffix)
        self.driver.save_screenshot(name)

    def _get_screenshot_suffix(self, url) -> str:
        return ''.join(url.split('#')[0].split('/')[2:]) 

    def run(self):
        parser = build_cmd_arguments()
        args = parser.parse_args()
        print(args.source)
        if args.source:
            self.sourceList = args.source
        if args.suffix:
            self.start = args.suffix
        # print('URLs source file', self.sourceList)
        if path.exists(sourceList):
            print(f'Reading the list of websites from {self.sourceList} file')
            with open(sourceList) as f:
                websitesL = f.read().splitlines()
                # print(f'URL addresses that will be captured')
                for website in websitesL:
                    print(f'Taking screenshots of {website}')
                    for driver in DRIVERS:
                        print(f'>Running screen capture for `{driver}`')
                        browser = get_browser(driver)
                        browser.get(website)
                        
                        for resolution in RESOLUTIONS:
                            print(f'...Taking screenshot in resolution {resolution}')
                            browser.set_window_size(*resolution)
                            sw, sh = resolution
                            """
                            suffix = ''.join(browser.current_url.split('#')[
                                            0].split('/')[2:])
                            """
                            suffix = self._get_screenshot_suffix(
                                browser.current_url
                                )
                            if self.start:
                                suffix = f'{self.start}_{suffix}'
                            capture_filename = f'{OUTPUT}/{suffix}_{driver}_{sw}x{sh}.png'
                            if browser.save_screenshot(capture_filename):
                                print(f'>>Saved screenshot {capture_filename}')
                        browser.quit()


ScreenShots(sourceList).run()
