""" Save a screenshot from spotify.com in current directory.
    Run the script reading the urls from urls.conf and start
    the name for the screenshots with xyx_
    python3 capture.py --suffix xyx
    Or from another file, for instance aaa.txt
    python3 capture.py --suffix xyx -S aaa.txt
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
HEADLESS_OPTIONS = {
    'chrome': ChromeOptions,
    'firefox': FirefoxOptions
}

RESOLUTIONS = [
    (1024, 768),
    (800, 600),
    (2048, 1024),
]

URLS_LIST = 'urls.conf'
START_NAME = ''


class ScreenShots:

    def __init__(self, sourceList=URLS_LIST):
        self.sourceList = sourceList
        self.start = START_NAME
        # self.driver = None

    def _get_screenshot_suffix(self, url) -> str:
        return ''.join(url.split('#')[0].split('/')[2:])

    def run(self):
        parser = build_cmd_arguments()
        args = parser.parse_args()
        if args.source:
            self.sourceList = args.source
        if args.suffix:
            self.start = args.suffix
        if path.exists(self.sourceList):
            print(f'Reading the list of websites from {self.sourceList}')
            with open(self.sourceList) as f:
                websitesL = f.read().splitlines()
                for website in websitesL:
                    print(f'\nTaking screenshots of {website}')
                    for driver in DRIVERS:
                        print(f'> Running screen capture in `{driver}`')
                        browser = get_browser(driver)
                        browser.get(website)
                        for resolution in RESOLUTIONS:
                            browser.set_window_size(*resolution)
                            sw, sh = resolution
                            suffix = self._get_screenshot_suffix(
                                browser.current_url
                                )
                            if self.start:
                                suffix = f'{self.start}_{suffix}'
                            name = f'{OUTPUT}/{suffix}_{driver}_{sw}x{sh}.png'
                            if browser.save_screenshot(name):
                                print(f'...Saved screenshot {name}')
                        browser.quit()


ScreenShots().run()
