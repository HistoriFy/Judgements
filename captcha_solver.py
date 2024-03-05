## This file contains the functions to solve the captcha and handle the captcha validation error.
## The functions are used in the main.py file.

## The functions are:
## 1. enter_captcha_and_search
## 2. attempt_to_solve_captcha
## 3. handle_captcha_validation

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


from utils import capture_captcha_image, select_high_court
from ocr_for_captcha import solve_captcha


def enter_captcha_and_search(driver, captcha_text):
    """Enter the obtained captcha text and click on search finally.

    Args:
        driver (Webdriver): Selenium WebDriver instance.
        captcha_text (str): Extracted text from the captcha image.
    """    
    captcha_text_box = driver.find_element(By.XPATH, '//input[@id="captcha"]')
    captcha_text_box.click()
    captcha_text_box.send_keys(captcha_text)
    
    time.sleep(3)
    
    search_button = driver.find_element(By.XPATH, '//button[contains(@id,"search")]')
    search_button.click()

def attempt_to_solve_captcha(driver):
    """Attempt to solve the captcha again if the initial attempt fails.
    By default it tries twice.

    Args:
        driver (Webdriver): Selenium WebDriver instance.

    Returns:
        str: Extracted text from the captcha image.
    """    
    for attempt in range(2):
        captcha_path = capture_captcha_image(driver)
        captcha_text = solve_captcha(captcha_path)
        print(f"Captcha image solved to {captcha_text} using OCR")
        if captcha_text:
            enter_captcha_and_search(driver, captcha_text)
            return captcha_text
        print("OCR processing failed or no text extracted. Trying again..")
        driver.refresh()
    print("OCR processing failed twice... Exiting")
    return None

def handle_captcha_validation(driver):
    """Handle the captcha validation error.
    
    Args:
        driver (Webdriver): Selenium WebDriver instance.
        
    Returns:
        bool: True if the captcha is valid, False otherwise.
    """
    try:
        captcha_error_box = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//div[contains(@class,"alert-danger") and contains(text(),"Invalid Captcha")]'))
        )
        print("Captcha is invalid. Retrying....")
        
        driver.refresh()
        time.sleep(5)
        
        #Selecting the High Court option again
        select_high_court(driver)
        
        return attempt_to_solve_captcha(driver)
    except:
        print("Captcha is valid.")
        return True
