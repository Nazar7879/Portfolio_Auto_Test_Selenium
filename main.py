import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SauceDemo:###
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        self.screenshot_folder = "screenshots"  # Folder name for screenshots

        # Check if the folder exists, if not, create it##
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
    
    # Method to open the SauceDemo page
    def open_page(self):
        self.driver.get(self.url)
        self.driver.maximize_window()  # Maximize the window for better visibility
    
    # Method to login to the site with the provided username and password
    def login_in(self, user_name_data, password_data):
        try:
            # Locate username field and enter the username
            user_name = self.driver.find_element(By.CSS_SELECTOR, "#user-name")
            user_name.send_keys(user_name_data)
            user_name.screenshot(os.path.join(self.screenshot_folder, 'user_name.png'))

            # Locate password field and enter the password
            password = self.driver.find_element(By.CSS_SELECTOR, "#password")
            password.send_keys(password_data)
            password.screenshot(os.path.join(self.screenshot_folder, 'password.png'))
            time.sleep(2)

            # Click the login button#
            login_button = self.driver.find_element(By.CSS_SELECTOR, "#login-button")
            login_button.click()
        except NoSuchElementException as e:
            print(f"No such element: {e}")

    # Method to add a product to the cart, go to the cart, and remove the product
    def add_goods(self):
        try:
            # Add a T-shirt to the cart
            add_t_shirt = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
            add_t_shirt.click()

            # Go to the cart
            cart = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#shopping_cart_container > a"))
            )
            cart.click()

            # Remove the item from the cart
            time.sleep(2)  # Can be replaced with an explicit wait
            remove_goods = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#remove-sauce-labs-bolt-t-shirt"))
            )
            remove_goods.click()

            # Save a screenshot of the cart after removing the item
            self.driver.get_screenshot_as_png()
            self.driver.save_screenshot(os.path.join(self.screenshot_folder, 'remove.png'))

            # Go back to the product page
            self.driver.back()
        except NoSuchElementException as e:
            print(f"No such element: {e}")
    
    # Method to close the browser page
    def close_page(self):
        self.driver.quit()

# Main execution
if __name__ == "__main__":
    driver = webdriver.Chrome()
    demo = SauceDemo(driver)
    demo.open_page()
    demo.login_in("standard_user", "secret_sauce")
    demo.add_goods()
    input("Press Enter to close the page...")
    demo.close_page()