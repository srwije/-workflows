from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestCases:
    def __init__(self, login_details):
        self.login_details = login_details
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait_conditions = WebDriverWait(self.driver, 10)
        self.processed_devices = set()

    def __del__(self):
        self.driver.quit()

    def login(self, report_obj):
        try:
            self.driver.get(self.login_details.url)
            username_input = self.wait_conditions.until(EC.element_to_be_clickable((By.NAME, "username")))
            username_input.send_keys(self.login_details.username)

            password_input = self.wait_conditions.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_input.send_keys(self.login_details.password)

            sign_in_button = self.wait_conditions.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mdc-button")))
            sign_in_button.click()

            device_link = self.wait_conditions.until(EC.presence_of_element_located((By.LINK_TEXT, "Devices")))
            assert device_link.text == "Devices"

            print("Login successful!")
            #report_obj.passed_tests.append(("Login Test", "Login Successful"))
        except Exception as e:
            print(f"An error occurred during login: {e}")
            #report_obj.failed_tests.append(("Login Test", f"Failed to login: {e}"))

    def check_devices(self, report_obj):
        try:
            device_link = self.wait_conditions.until(EC.presence_of_element_located((By.LINK_TEXT, "Devices")))
            device_link.click()

            while True:
                self.wait_conditions.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "table#DataTables_Table_1 tbody tr")) > 0)
                device_rows = self.driver.find_elements(By.CSS_SELECTOR, "table#DataTables_Table_1 tbody tr")

                for row in device_rows:
                    retries = 2
                    while retries > 0:
                        try:
                            device_info = row.text
                            device_id = device_info.split()[0]

                            if device_id not in self.processed_devices:
                                self.check_last_updated_time(row, device_id, report_obj)
                                self.processed_devices.add(device_id)
                            break
                        except (StaleElementReferenceException, NoSuchElementException) as e:
                            retries -= 1
                            time.sleep(1)
                            if retries == 0:
                                print(f"Skipping row due to error: {e}")
                                #report_obj.failed_tests.append(("Device List", "Error processing a device row"))

                time.sleep(5)
                try:
                    next_button = self.driver.find_element(By.ID, "DataTables_Table_1_next")
                    if "disabled" in next_button.get_attribute("class"):
                        print("Reached the last page.")
                        break
                    next_button.click()
                    time.sleep(1)
                except NoSuchElementException:
                    print("Pagination 'Next' button not found.")
                    break
        except TimeoutException:
            print("Device list did not load in time.")
            #report_obj.failed_tests.append(("Device List", "Error Loading List"))

    def check_last_updated_time(self, row, device_id, report_obj):
        try:
            tolerance = timedelta(hours=2)
            current_time = datetime.now()

            last_updated_text = row.find_element(By.CSS_SELECTOR, "td:nth-child(6) span").text.strip()
            last_updated_time = datetime.strptime(last_updated_text, "%Y-%m-%d %H:%M:%S")

            if (current_time - last_updated_time) <= tolerance:
                print(f"Device {device_id} is up to date.")
                report_obj.passed_tests.append(("Device", f"Device {device_id} is up to date ({last_updated_text})"))
            else:
                print(f"Device {device_id} is NOT up to date.")
                report_obj.failed_tests.append(("Device", f"Device {device_id} is NOT up to date ({last_updated_text})"))
        except Exception as e:
            print(f"Error checking last updated time for device {device_id}: {e}")
            #report_obj.failed_tests.append(("Device List", "Error checking last updated time"))
