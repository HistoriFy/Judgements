## This file contains the configuration for the WebDriver.
## The function is used in the main.py file.
## The function is:
## 1. configure_chrome_options

##NOTE: The `--disable-blink-features=AutomationControlled` option is used to bypass the bot detection by the website.
##      The `--headless` option is commented out to see the browser interaction.
##      The pdf won't be downloaded if the browser is in headless mode.

from selenium.webdriver.chrome.options import Options


def configure_chrome_options():
    """Configure Chrome options for the WebDriver.
    Returns:
        Options: Chrome options with required settings.
    """
    
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disable default selenium logging
    options.add_argument('--incognito')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument('--headless')  # Disable this if you want to see the browser interaction
    
    
    return options