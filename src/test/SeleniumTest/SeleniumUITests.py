import time
import unittest
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, JavascriptException
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dotenv_path = find_dotenv()  # finds the .env file path
        load_dotenv(dotenv_path)  # loads the .env file from the path found above
        chrome_driver_path = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(name="detach", value=True)
        service = ChromeService(executable_path=chrome_driver_path)
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.maximize_window()

    def setUp(self):
        # This method runs before each test method
        self.driver.get("http://localhost:8314")  # Navigate to a start page or reset state

    def test_login(self):
        error_count: int = 0
        try:
            login_button = self.driver.find_element(by=By.XPATH,
                                                    value='//*[@id="root"]/div/form/button[1]')
            login_button.click()

            username = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/form/div[2]/input')
            username.send_keys(os.getenv("ECHO_USERNAME"))  # Gets the echo_username from .env

            password = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/form/div[3]/input')
            password.send_keys(os.getenv("ECHO_PASSWORD"))  # Gets the echo_password from .env

            login_button = self.driver.find_element(by=By.CLASS_NAME, value='btn-primary')
            login_button.click()

        except selenium.common.JavascriptException as e:
            error_count += 1

        expected: str = "http://localhost:8314/homepage"
        url: str = self.driver.current_url

        self.assertEqual(error_count, 0)
        self.assertEqual(expected, url)

    def test_guest_login(self):
        error_count: int = 0
        try:
            login_button = self.driver.find_element(by=By.XPATH,
                                                    value='//*[@id="root"]/div/form/button[1]')
            login_button.click()
            # Wait for the guest button to be visible and clickable
            guest_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/form/p[2]/a'))
            )
            guest_button.click()

        except (selenium.common.JavascriptException, selenium.common.TimeoutException)as e:
            error_count += 1
            print(f"Exception: {e}")

        expected: str = "http://localhost:8314/homepage"
        url: str = self.driver.current_url

        self.assertEqual(error_count, 0)
        self.assertEqual(expected, url)

    def test_post(self):
        pass

    def test_post_guest(self):
        pass

    def test_profile_page(self):
        self.test_login()  # Login and go to homepage

        profile_button = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/div[1]/div/a[6]/b')
        profile_button.click()

        expected_url: str = "http://localhost:8314/profile"
        actual_url: str = self.driver.current_url

        time.sleep(3)

        self.assertEqual(expected_url, actual_url)

    def test_profile_page_as_guest(self):
        pass

    def test_feed_page(self):
        pass

    def test_about_us(self):
        pass

    def test_about_us_to_home(self):
        pass

    def test_about_us_to_profile(self):
        pass

    def test_about_us_to_feed(self):
        pass

    def test_profile_to_about(self):
        pass

    def test_profile_to_feed(self):
        self.test_login()  # Login and go to homepage

        profile_button = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/div[1]/div/a[6]/b')
        profile_button.click()

        expected_url: str = "http://localhost:8314/profile"
        actual_url: str = self.driver.current_url

        self.assertEqual(expected_url, actual_url)  # Confirm we are on the about page

        home_button = self.driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/div/section[1]/div[1]'
                                                                  '/div/div[1]/div[1]/div[2]/div[1]/div/div/div/div[1]'
                                                                  '/div/a/div')
        home_button.click()

        expected_url: str = "http://localhost:8314/homepage"
        actual_url: str = self.driver.current_url

        self.assertEqual(expected_url, actual_url)

    @classmethod
    def tearDownClass(cls):
        # This method runs once after all tests are done
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()

