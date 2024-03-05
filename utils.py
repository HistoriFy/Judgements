# some utility functions that will be used in the main script.
# 
# 1. The `select_high_court` function selects the "High Court" option from the main page where captcha is displayed.
# 2. The `capture_captcha_image` function captures the captcha image and saves it to the current working directory.
#       It uses the `screenshot_as_png` method of the WebElement to capture the image and save it as `captcha.png`.
# 3. The `image_to_base64` function converts the image to a base64 encoded string.
#       It reads the image file and returns the base64 encoded string.
# 4. The `sanitize_filename` function sanitizes the filename to avoid any filename with special characters.

from selenium.webdriver.common.by import By
import base64
import os
import re

def select_high_court(driver):
    """Select the "High Court" option from the dropdown.
    
    Args:
        driver (Webdriver): Selenium WebDriver instance.
    """
    high_court_option = driver.find_element(By.XPATH, '//select[@id="fcourt_type"]//option[contains(text(),"High Court")]')
    high_court_option.click()
    print("High Court option selected")

def capture_captcha_image(driver, selector='img[id*="captcha_image"]'):
    """Capture the captcha image and save it to the current working directory.
        
        Args:
            driver (Webdriver): Selenium WebDriver instance.
            selector (str): CSS selector for the captcha image.
            
        Returns:
            str: Path to the saved captcha image.
    """
    image_binary = driver.find_element(By.CSS_SELECTOR, selector).screenshot_as_png
    image_path = os.path.join(os.getcwd(), "captcha.png")
    with open(image_path, "wb") as image_file:
        image_file.write(image_binary)
    return image_path

def image_to_base64(image_path):
    """Convert the image to base64 encoded string.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        str: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def sanitize_filename(filename):
    """Sanitize the filename to avoid any issues.
    
    Args:
        filename (str): Original filename.
        
    Returns:
        str: Sanitized filename.
    """
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Optionally, truncate the file name to avoid length issues
    max_length = 240  # Arbitrary limit, considering the path might add to the length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized