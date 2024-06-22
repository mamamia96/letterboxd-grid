from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from threading import Thread

import time

class WebThreadContainer:

    html: str

    def __init__(self, _url: str) -> None:
        self.url = _url

        # create selenium webdriver
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

        
        # self.get_html_with_js(self.url, self. results, self.index)

    def _get_html_with_js(self):
        return Thread(target=self.get_html_with_js)

    def get_html_with_js(self) -> str:
        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # # options.headless = True
        # driver = webdriver.Firefox(options=options)

        t0 = time.time()

        self.driver.get(self.url)

        # time.sleep(4)
        # Wait until the page has finished loading
        WebDriverWait(self.driver, 10, poll_frequency=0.25).until(poster_url_loaded)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located)
        t1 = time.time()
        # Get the HTML content of the page
        self.html = self.driver.page_source

        # print("Headless Firefox Initialized")
        self.driver.quit()
        print(f'THREAD[{self.url}] finished {t1-t0} ')
        # print(f'{t1-t0}')


def poster_url_loaded(driver) -> bool:
    # checking to see if the data needed has been populated yet
    if not driver.page_source: return False

    soup = BeautifulSoup(driver.page_source,'html5lib')

    div_tag = soup.find('a', attrs={'data-js-trigger':'postermodal'})
    return div_tag != None

def get_html_with_js(url: str, results: list, index: int) -> str:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Wait until the page has finished loading
    WebDriverWait(driver, 10).until(poster_url_loaded)

    # Get the HTML content of the page
    html = driver.page_source

    driver.quit()
    
    results[index] = html
    print(f'THREAD[{index}] finished')
