import os
import re 

from time import sleep, perf_counter, thread_time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


WEBPAGES = [
    "https://www.coles.com.au/search?q=room spray",
    "https://www.coles.com.au/search?q=air freshener",
    "https://www.coles.com.au/search?q=candles",
    "https://www.coles.com.au/browse/household/air-fresheners-home-fragrance",
    "https://www.coles.com.au/search?q=dishwasher tablets",
    "https://www.coles.com.au/search?q=dishwashing tablets",
    "https://www.coles.com.au/search?q=dishwashing",
    "https://www.coles.com.au/browse/household/dishwashing",
    "https://www.coles.com.au/search?q=kitchen cleaner",
    "https://www.coles.com.au/search?q=cleaning wipes",
    "https://www.coles.com.au/search?q=cleaning spray",
    "https://www.coles.com.au/search?q=disinfectant",
    "https://www.coles.com.au/browse/household/cleaning-goods",
    "https://www.coles.com.au/search?q=stain removal",
    "https://www.coles.com.au/search?q=laundry",
    "https://www.coles.com.au/browse/household/laundry/stain-removal-pre-wash",
    "https://www.coles.com.au/browse/household/laundry",
    "https://www.coles.com.au/search?q=toilet",
    "https://www.coles.com.au/search?q=toilet cleaner",
    "https://www.coles.com.au/browse/household/cleaning-goods/toilet-cleaning",
    "https://www.coles.com.au/search?q=fly spray",
    "https://www.coles.com.au/search?q=pest control",
    "https://www.coles.com.au/search?q=insect repellent",
    "https://www.coles.com.au/browse/household/pest-control"
]

DRIVER_PATH = r"chromedriver"

BASE_PATH = "screenshots"


def get_chrome_driver(driver_path: str = DRIVER_PATH) -> webdriver.Chrome:
    service = Service(driver_path)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-features=Automation")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1580,1280")

    return webdriver.Chrome(service=service, options=options)


def get_chrome_driver_from_manager() -> webdriver.Chrome:
    cdm = ChromeDriverManager(path=".")
    path = cdm.install()
    return webdriver.Chrome(service=Service(path))


def create_todays_directory() -> str:
    base = BASE_PATH
    if not os.path.isdir(base):
        os.mkdir("screenshots")

    todays_path = get_todays_path()
    if not os.path.isdir(todays_path):
        os.mkdir(todays_path)

    return todays_path


def get_todays_path() -> str:
    today = str(datetime.now().date())
    return os.path.join(BASE_PATH, today)


class Screenshotter:
    def __init__(self, driver: webdriver.Chrome, directory: str) -> None:
        self.driver = driver
        self.directory = directory

    def _generate_filepath(self, url: str) -> str:
        return os.path.join(self.directory, re.sub(r"\W+", "", url) + ".png")

    def take_screenshot_to_file(self, url: str) -> None:
        self.driver.get(url)
        self.driver.get_screenshot_as_file(self._generate_filepath(url))

    def take_screenshots(self) -> None:
        [self.take_screenshot_to_file(webpage) for webpage in WEBPAGES]


class ScreenshotterMultiThread:
    def __init__(self, directory: str = "screenshots", num_workers: int = 10, driver_path: str = DRIVER_PATH) -> None:
        self.directory = directory
        self.num_workers = num_workers
        self.driver_path = driver_path

    def _generate_filepath(self, url: str) -> str:
        return os.path.join(self.directory, re.sub(r"\W+", "", url) + ".png")

    def take_screenshot_to_file(self, url: str) -> None:
        driver = get_chrome_driver(self.driver_path)
        driver.get(url)
        driver.get_screenshot_as_file(self._generate_filepath(url))
        driver.quit()

    def take_screenshots(self, urls=WEBPAGES) -> None:
        with ThreadPoolExecutor(max_workers=self.num_workers) as thread:
            thread.map(self.take_screenshot_to_file, urls)
        
        
def main_singlethread():
    driver = get_chrome_driver()
    todays_directory = create_todays_directory()

    screenshotter = Screenshotter(driver, todays_directory)
    screenshotter.take_screenshots()

    driver.quit()


def main_multithread(urls=WEBPAGES):
    todays_directory = create_todays_directory()
    
    screenshotter = ScreenshotterMultiThread(todays_directory)
    screenshotter.take_screenshots(urls)

    return todays_directory


def take_all_screenshots():
    return main_multithread()


def take_screenshots(urls):
    return main_multithread(urls)



if __name__ == "__main__":
    tic = perf_counter()
    main_multithread()
    print(f"Multithread: {perf_counter() - tic}")
