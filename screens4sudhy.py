import os
import re 

from time import sleep, perf_counter, thread_time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


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


def get_chrome_driver(driver_path: str) -> webdriver.Chrome:
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


def create_todays_directory() -> str:
    base = "screenshots"
    if not os.path.isdir(base):
        os.mkdir("screenshots")

    today = str(datetime.now().date())
    todays_path = os.path.join(base, today)
    if not os.path.isdir(todays_path):
        os.mkdir(todays_path)

    return todays_path


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
    def __init__(self, directory: str = "screenshots", num_workers: int = 10, driver_path: str = r"/chromedriver/stable/chromedriver") -> None:
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

    def take_screenshots(self) -> None:
        with ThreadPoolExecutor(max_workers=self.num_workers) as thread:
            thread.map(self.take_screenshot_to_file, WEBPAGES)
        
        
def main_singlethread():
    driver = get_chrome_driver(r"/chromedriver/stable/chromedriver")
    todays_directory = create_todays_directory()

    screenshotter = Screenshotter(driver, todays_directory)
    screenshotter.take_screenshots()

    driver.quit()


def main_multithread():
    todays_directory = create_todays_directory()
    
    screenshotter = ScreenshotterMultiThread(todays_directory, 10, r"/chromedriver/stable/chromedriver")
    screenshotter.take_screenshots()


if __name__ == "__main__":
    tic = perf_counter()
    main_multithread()
    print(f"Multithread: {perf_counter() - tic}")
