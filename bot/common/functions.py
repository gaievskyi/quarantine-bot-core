from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .settings import browser


def query_selector(selector, timeout=0) -> WebElement:
    """Find element by its CSS selector"""
    try:
        element = EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        WebDriverWait(browser, timeout).until(element)
        return browser.find_element_by_css_selector(selector)

    except exceptions.TimeoutException:
        return None
