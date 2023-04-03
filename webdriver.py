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

        # Zoom out page to show all playlists at once
        driver.execute_script(
            "document.body.style.transform='scale(0.1, 0.1)'")
        _ = WebDriverWait(driver=driver, timeout=10).until(lambda browser: len(
            browser.find_elements(By.CSS_SELECTOR, ".ytd-grid-renderer")) >= int(104))

        # Return the page contents
        return driver.page_source

    def get_all_matching_elements(self, page_source, css):
        """
            Gets a list of elements as strings from 'page_source' which match 'css' selector

            Args:
                page_source: The string representing the page
                css: The css used to identify the element, string
        """

        return Selector(text=page_source).css(css).getall()

    def get_element_attribute(self, text, css, attr):
        """
            Gets the string value of 'attr' for the element uniquely identified by 'css' inside 'text'

            Args:
                text: The string representing the element
                css: The css used to identify the element, string
                attr: The attribute found within the element, string
        """

        return Selector(text=text).css(css).attrib[attr]
