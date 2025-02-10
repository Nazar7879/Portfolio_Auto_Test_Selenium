import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        self.username_locator = (By.CSS_SELECTOR, "#user-name")
        self.password_locator = (By.CSS_SELECTOR, "#password")
        self.button_login_locator = (By.CSS_SELECTOR, "#login-button")

    def open_page(self):
        self.driver.get(self.url)

    def login(self, username, password):
        self.driver.find_element(*self.username_locator).send_keys(username)
        time.sleep(2)
        self.driver.find_element(*self.password_locator).send_keys(password)
        time.sleep(2)
        self.driver.find_element(*self.button_login_locator).click()

class FilterPage:
    def __init__(self, driver):
        self.driver = driver
        self.filter_locator = (By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/span/select")

    def apply_filter(self, option):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.filter_locator))
        dropdown = self.driver.find_element(*self.filter_locator)
        select = Select(dropdown)
        select.select_by_visible_text(option)
        time.sleep(2)

    def get_product_names(self):
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [product.text for product in products]

    def get_product_prices(self):
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [float(price.text.strip("$")) for price in products]

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def login(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("standard_user", "secret_sauce")

@pytest.fixture
def filter_actions(driver):
    filter_page = FilterPage(driver)
    filter_page.apply_filter("Name (A to Z)")
    names_a_to_z = filter_page.get_product_names()
    filter_page.apply_filter("Name (Z to A)")
    names_z_to_a = filter_page.get_product_names()
    filter_page.apply_filter("Price (low to high)")
    prices_low_to_high = filter_page.get_product_prices()
    filter_page.apply_filter("Price (high to low)")
    prices_high_to_low = filter_page.get_product_prices()

    return {
        "names_a_to_z": names_a_to_z,
        "names_z_to_a": names_z_to_a,
        "prices_low_to_high": prices_low_to_high,
        "prices_high_to_low": prices_high_to_low
    }

def test_login_success(driver, login):
    current_url = driver.current_url
    assert "inventory" in current_url, f"Login failed, current URL: {current_url}"

def test_filters(driver, login, filter_actions):
    assert filter_actions["names_a_to_z"] == sorted(filter_actions["names_a_to_z"]), "Names are not sorted A to Z"
    assert filter_actions["names_z_to_a"] == sorted(filter_actions["names_z_to_a"], reverse=True), "Names are not sorted Z to A"
    assert filter_actions["prices_low_to_high"] == sorted(filter_actions["prices_low_to_high"]), "Prices are not sorted low to high"
    assert filter_actions["prices_high_to_low"] == sorted(filter_actions["prices_high_to_low"], reverse=True), "Prices are not sorted high to low"

if __name__ == "__main__":
    pytest.main([__file__])