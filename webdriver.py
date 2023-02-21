from hashlib import new

from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebDriver:
    # Main method
    def get_webpage(self, url):
        """
            Gets the content of the specified webpage as a string

            Args:
                url: The URL of the webpage to get content from
        """

        # Configure Webdriver
        options = Options()
        options.headless = False
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")

        # Setup Webdriver
        driver = webdriver.Chrome(
            options=options)
        driver.get(url)

        # Click through cookie notice
        _ = WebDriverWait(driver=driver, timeout=10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Accept all']"))).click()

        # Wait for page to load
        _ = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ytd-page-manager")))

        # Scroll to page bottom
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            WebDriverWait(driver=driver, timeout=3)

            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Return the page contents
        return driver.page_source

    def get_all_matching_elements(self, page_source, css):
        """
            Gets a list of elements from 'soup' which match 'tag' and 'attrs'

            Args:
                page_source: The string representing the page
                css: The css used to identify the element, string
        """

        return Selector(text=page_source).css(css).getall()
