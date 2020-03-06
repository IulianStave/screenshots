""" Save a screenshot from spotify.com in current directory. 
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import sys
from common.common import (
    get_browser,
    build_cmd_arguments,
)

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


"""
driver = webdriver.Chrome(DRIVER)
driver.get(BASE_URL)
screenshot = driver.save_screenshot('my_screenshot.png')
driver.quit()
"""


class ScreenShots:

    def __init__(self, base_url):
        self.base_url = base_url
        # self.driver = driver

    def BTCscreenshot(self, suffix: str = ''):
        """ Capture a screeenshot.
            Uses `suffix` if given or the current browser url.
        """
        suffix = suffix or self._get_screenshot_suffix()
        name = '{}/screenshot_{}.png'.format(os.getcwd(), suffix)
        self.driver.save_screenshot(name)

    def _get_screenshot_suffix(self) -> str:
        return '_'.join(self.driver.current_url.split('#')[0].split('/')[2:])

    def run(self):
        parser = build_cmd_arguments()
        args = parser.parse_args()
        print('URL', self.base_url)
        for driver in DRIVERS:
            print(f'Running screen capture for `{driver}`')
            browser = get_browser(driver)
            browser.get(args.url if args.url else self.base_url)
            for resolution in RESOLUTIONS:
                print(f'...Running screen capture for resolution {resolution}')
                browser.set_window_size(*resolution)
                sw, sh = resolution
                suffix = ''.join(browser.current_url.split('#')[
                                  0].split('/')[2:])
                capture_filename = f'{suffix}_{driver}_{sw}x{sh}.png'
                if browser.save_screenshot(capture_filename):
                    print(f'...Saved screenshot {capture_filename}')
            browser.quit()
        """
        browser = get_browser(args.browser, args.headless, args.browserpath)
        resolution = (args.screenwidth, args.screenheight)
        browser.set_window_size(*resolution)
        browser.get(args.url if args.url else self.base_url)
        capture_filename = args.browser+str(args.screenwidth)+'x'+str(args.screenheight)+'.png'
        screenshot = browser.save_screenshot(capture_filename)

        """
        """
        test_suite = unittest.TestSuite()
        for test in self.tests:
            # get the available tests
            for name in test.all_tests():
                test_case = test(
                    name,
                    browser,
                    args.url if args.url else self.base_url
                )
                test_suite.addTest(test_case)
        """
        # runner = unittest.TextTestRunner(verbosity=args.verbose)
        # success = runner.run(test_suite).wasSuccessful()
        # browser.quit()
        # sys.exit(0 if success else 1)


ScreenShots(BASE_URL).run()
