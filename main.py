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
# 3. Attempt to solve the captcha by capturing the image and using OCR to extract the text.
# 4. If the captcha is not solved, attempt to solve it again.
# 5. If the captcha is still not solved, exit the script.
# 6. Extract the case information from the table and click on the first case to view the details.
# 7. Wait for the PDF link to be accessible and capture a screenshot of the page.
# 8. Extract the PDF link and save the PDF file to the current working directory.
# 9. Close the browser.


from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import os

from captcha_solver import  attempt_to_solve_captcha, handle_captcha_validation
from utils import sanitize_filename
from config import configure_chrome_options



def main():
    driver = webdriver.Chrome(options=configure_chrome_options())
    driver.get('https://judgments.ecourts.gov.in/pdfsearch/index.php')
    driver.implicitly_wait(10)
    
    #Selecting High Court Cases due to large number of cases and constant update
    
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
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()


