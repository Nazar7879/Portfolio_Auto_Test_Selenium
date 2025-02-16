import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

#Logging settings

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="class")
def driver_init(request):
    driver=webdriver.Chrome()
    request.cls.driver=driver
    yield
    driver.quit()


@pytest.mark.usefixtures("driver_init")
class TestLogin:

    url="https://www.saucedemo.com/"
    #install locators
    locator_user_name=(By.CSS_SELECTOR,"#user-name")
    password_locator=(By.CSS_SELECTOR,"#password")
    button_locators=(By.CSS_SELECTOR,"#login-button")


    def login_in(self,user_name_data,password_data):
        
        logging.info("Start process")
        
        self.driver.get(self.url)

        WebDriverWait(self.driver,10).until(EC.presence_of_element_located(self.locator_user_name))

        self.driver.find_element(*self.locator_user_name).send_keys(user_name_data)
        self.driver.find_element(*self.password_locator).send_keys(password_data)
        self.driver.find_element(*self.button_locators).click()

        WebDriverWait(self.driver,10).until(EC.url_contains("inventory"))

        logging.info("authorization was successful")


    @pytest.mark.parametrize("user_name,password",[
        ["user_1","877979aaa"],
        ["user_2","fggmf77979"],
        ["user_3","gtuggtt989898"],
        ["user_4","fpfpfpfpf5565"],
        ["standard_user","secret_sauce"]


    ])




    def test_login(self,user_name,password):
        try:
            self.login_in(user_name,password)
            assert "inventory" in self.driver.current_url
            logging.info(f"Test for {user_name} was successful")
        except AssertionError:
            logging.error(f"Test for {user_name} wasn't  pass")
            raise
        except Exception as e:
            logging.error(f"we got a problem with test{user_name}:{str(e)}")
            raise
                          
            




    


 

