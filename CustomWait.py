from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CustomWait:
    def __init__(self, driver, timeout=10):
        self.wait = WebDriverWait(driver, timeout)

    def until_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def until_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
