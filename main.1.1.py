import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException ,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class LoginPage:###
    def __init__(self,driver):
        self.driver=driver
        self.url="https://www.saucedemo.com/"

        self.username_input=(By.CSS_SELECTOR,"#user-name")
        self.password_input=(By.CSS_SELECTOR,"#password")

        self.button_login=(By.CSS_SELECTOR,"#login-button")

    #Opne login page##
    def open_page(self):  
        self.driver.get(self.url)
        self.driver.maximize_window()
     # login 
    def login(self,username_data,password_data):
        try:
            self.driver.find_element(*self.username_input).send_keys(username_data)
            self.driver.find_element(*self.password_input).send_keys(password_data)
            time.sleep(2)
            self.driver.find_element(*self.button_login).click()
        except NoSuchElementException as e:
            print(f"Error:Element not found during login :{e}")
        except Exception as e:
            print(f"Unexpected error  during login:{e}")


class MainFunction:
    def __init__(self,driver):
        self.driver=driver
        self.screenshot_folder="screenshots"
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
    
    def filter_and_goods(self):
        try:
            self.filter_on=(By.XPATH,"/html/body/div/div/div/div[1]/div[2]/div/span/select")
            self.add_goods_bike=(By.CSS_SELECTOR,"#add-to-cart-sauce-labs-bike-light")
            self.cart=(By.CSS_SELECTOR,"#shopping_cart_container > a")

            self.dropdow_filter=Select(driver.find_element(*self.filter_on))
            self.dropdow_filter.select_by_value("lohi")
            self.driver.find_element(*self.add_goods_bike).click()
            self.driver.find_element(*self.cart).click()
            time.sleep(2)
            #take scrinshot
        
            self.driver.save_screenshot(os.path.join(self.screenshot_folder,'gooods_in_cart.png'))
            self.driver.back()
        except NoSuchElementException as e:
            print(f"Error:element not found during adding to cart :{e}")
        except TimeoutException as e:
            print(f"ERROR : while closing the page :{e}")
        except Exception as e:
            print(f"Unexpected error:{e}")

    def close_page(self):
        self.driver.quit()




if __name__ == "__main__":
    driver=webdriver.Chrome()
    login_page=LoginPage(driver)
    main=MainFunction(driver)



    login_page.open_page()
    login_page.login("standard_user","secret_sauce")

    main.filter_and_goods()
    input("type here for close the page")

    main.close_page()






        



    




       


    