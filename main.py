#entry point for the script

# Required libraries
# 1. selenium
# 2. requests
# 3. python-dotenv

##NOTE: The script assumes that the Chrome browser is pre-installed on the system.
##      If not, Please download and install the Chrome browser from https://www.google.com/chrome/

##NOTE: Sometimes script execution stucks due to downtime of OCR api (Free version moment)
##      In that case, please try again after some time.


# Flow of main.py
# 1. Open the URL in a Chrome browser using Selenium WebDriver.
# 2. Select the "High Court" option from the dropdown due to constant updates
# 3. Try to solve the captcha by saving its screenshot and running OCR on it.
# 4. If the captcha is not solved, try to solve it again. Exit at the end if the captcha is not solved.
# 6. Extract the case information from the table and click on the first case to view the details.
# 7. Wait for the PDF link to be accessible and capture a screenshot of the page.
# 8. Extract the PDF link and save the PDF file to the current working directory.
# 9. Close the browser.


from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import sys
import os

from captcha_solver import  attempt_to_solve_captcha, handle_captcha_validation
from utils import sanitize_filename
from config import configure_chrome_options



def main():
    
    website = 'https://judgments.ecourts.gov.in/pdfsearch/index.php'
    
    driver = webdriver.Chrome(options=configure_chrome_options())
    driver.get(website)
    driver.implicitly_wait(10)
    
    #Selecting High Court Cases due to large number of cases and constant updates
    
    high_court_option = driver.find_element(By.XPATH, '//select[@id="fcourt_type"]//option[contains(text(),"High Court")]')
    high_court_option.click()
    print("High Court option selected")
    
    captcha_text = attempt_to_solve_captcha(driver)
    if not captcha_text:
        driver.quit()
        return

    if not handle_captcha_validation(driver):
        driver.quit()
        return
    
    # Wait for the page to load
    driver.implicitly_wait(5)
    try:
        
        # Select the last week from the decision date dropdown
        
        decision_date_drop_down_element = driver.find_element(By.XPATH, '//i[contains(@class,"calendar")]/parent::a')
        decision_date_drop_down_element.click()
        
        time.sleep(2)
        
        last_week_option_element = driver.find_element(By.XPATH, '//input[@value="WEEK"]')
        last_week_option_element.click()
        
        time.sleep(2)
        
        search_button_element = driver.find_element(By.XPATH, '//i[contains(@class,"search")]/parent::button')
        search_button_element.click()
        
        #wait for page to load again after updating the list with LATEST UPDATED case
        time.sleep(5)     
        
        # Extract case information
        cases_table = driver.find_element(By.XPATH, '//tbody[@id="report_body"]')
        first_case = cases_table.find_element(By.XPATH, './/tr[1]/td[not(contains(@class, "sorting"))]')
        first_case_heading_element = first_case.find_element(By.XPATH, './/button[@role="link"]')
        first_case_heading = first_case_heading_element.get_attribute('aria-label')
        first_case_decision_date = first_case.find_element(By.XPATH, './/span[contains(text(),"Decision Date")]/following-sibling::font[1]').text
        
        if first_case.is_displayed():
            print(f"First Case: {first_case_heading}")
            print(f"Decision Date: {first_case_decision_date}")

        first_case_heading_element.click()
        
        time.sleep(5)  # Wait for the PDF link to be accessible
        
        first_case_pdf_link = driver.find_element(By.XPATH, '//div[@id="viewFiles-body"]/object').get_attribute('data')
        print("PDF link: ", first_case_pdf_link)
        
        pdf_name = sanitize_filename(first_case_heading) + ".pdf"
        pdf_path = os.path.join(os.getcwd(), pdf_name)
        
        
        pdf_response = requests.get(first_case_pdf_link)
        
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"PDF saved as {pdf_name}")
        print(f"PDF Path: {pdf_path}")
        
    except Exception as e:
        print(f"An error occurred: \n")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error File: {fname}")
        print(f"Error Type: {exc_type}")
        print(f"Error Object: {exc_obj}")
        print(f"Error Line: {exc_tb.tb_lineno}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()


