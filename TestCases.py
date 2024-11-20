from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class TestCases:
    def __init__(self, login_details):
        self.login_details = login_details

        # Set Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        chrome_options.add_argument('--no-sandbox')  # For CI environments
        chrome_options.add_argument('--disable-dev-shm-usage')  # For CI environments
        chrome_options.add_argument('--remote-debugging-port=9222')  # Allow debugging in headless mode
        chrome_options.add_argument('--disable-gpu')  # Disable GPU for headless mode
        chrome_options.add_argument('--start-maximized')  # Maximize window size
        chrome_options.add_argument('--disable-software-rasterizer')  # Prevent issues with rendering
        chrome_options.add_argument('--disable-extensions')  # Disable any Chrome extensions
        chrome_options.add_argument('--disable-logging')  # Disable logging
        chrome_options.add_argument('--log-level=3')  # Suppress logs

        try:
            # Ensure correct path to the ChromeDriver binary is set if necessary
            # You can manually specify the path to ChromeDriver as well
            service = Service(executable_path='/path/to/chromedriver')  # Adjust the path if necessary

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()  # Maximize the window
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
            self.driver = None

    def __del__(self):
        # Check if the driver was initialized before attempting to quit
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error quitting WebDriver: {e}")

    def login(self, report_obj):
        if not self.driver:
            print("WebDriver not initialized. Skipping login.")
            return

        try:
            self.driver.get(self.login_details.url)
            username_input = self.driver.find_element(By.NAME, "username")
            username_input.send_keys(self.login_details.username)

            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.login_details.password)

            sign_in_button = self.driver.find_element(By.CSS_SELECTOR, ".mdc-button")
            sign_in_button.click()

            device_link = self.driver.find_element(By.LINK_TEXT, "Devices")
            assert device_link.text == "Devices"

            print("Login successful!")
        except Exception as e:
            print(f"An error occurred during login: {e}")

    def check_devices(self, report_obj):
        if not self.driver:
            print("WebDriver not initialized. Skipping device check.")
            return

        try:
            device_link = self.driver.find_element(By.LINK_TEXT, "Devices")
            device_link.click()

            while True:
                time.sleep(5)
                device_rows = self.driver.find_elements(By.CSS_SELECTOR, "table#DataTables_Table_1 tbody tr")
                for row in device_rows:
                    print(row.text)

                try:
                    next_button = self.driver.find_element(By.ID, "DataTables_Table_1_next")
                    if "disabled" in next_button.get_attribute("class"):
                        print("Reached the last page.")
                        break
                    next_button.click()
                except Exception as e:
                    print(f"Error navigating to next page: {e}")
                    break
        except Exception as e:
            print(f"An error occurred while checking devices: {e}")
