# Judgements: High Court Order/Judgement Fetcher

Easily automate the retrieval of the latest high court orders or judgements and save them in PDF format with this script.

1. **Open the URL**: The script initiates a Chrome browser session using Selenium WebDriver.
2. **Select High Court**: Focuses on retrieving documents from the "High Court" section.
3. **Captcha Resolution**: Utilizes OCR to decipher captchas, with retries if necessary.
4. **Extract Case Information**: Details of cases are extracted for further actions.
5. **PDF Retrieval**: Waits for the PDF link, captures a screenshot, and then downloads the PDF.
6. **Save PDF**: The document is saved in the current directory with an appropriate name.
7. **Cleanup**: Closes the browser to conclude the session.


## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Script](#running-the-script)
- [Working Example](#working-example)
- [PREVIOUS ATTEMPT OF SIDE FILE](#previous-attempt-of-selenium-ide-file)
- [Future Improvements](#future-improvements-that-can-be-done)

## Prerequisites
Ensure Python is installed on your system. If not, you can install it from [Python's official website](https://www.python.org/downloads/) or via the command line:
```bash
sudo apt-get install python3
```

## Installation
1. **Install Required Python Packages**: To install the necessary dependencies, execute the following command in your terminal:
```bash
pip install -r requirements.txt
```

## Running the Script
To execute the script, use the command below in your terminal:
```bash
python3 main.py
```

**Important:** 
1. The first run of the script might take a little longer due to the initial setup of the Chrome WebDriver. Subsequent runs will be faster.
2. There might be instances where script execution is interrupted due to downtime of the OCR API, as its free version is being used. If you encounter any issues, such as script stalling or delays, please wait for some time and try running the script again. I appreciate your understanding and patience.
3. It is highly suggested to run the code in a virtual environment to avoid any conflicts with the existing packages in your system. To learn more about virtual environments, please visit the [official Python documentation](https://docs.python.org/3/library/venv.html).

## Working Example:

*Below are examples of successful execution for Ubuntu as well as Windows. Each stage is logged in the terminal.*

https://github.com/HistoriFy/Judgements/assets/67834542/aa039b0c-44f1-4e93-a1f4-ee94be59d996




https://github.com/HistoriFy/Judgements/assets/67834542/568bcd36-5682-4da0-b3c7-4a50e1a6cc42




---


## Previous Attempt of Selenium IDE File

Several attempts were made to directly fetch the PDF using Selenium IDE. Unfortunately, these attempts were unsuccessful due to the captcha challenges on the targeted website.


1. **Captcha Source URL**: The initial strategy to copy the source URL of the captcha image was unsuccessful because the captcha is dynamically regenerated with each request. This regeneration occurs whether the request is made independently or alongside the website's own requests. You can witness this behavior by visiting the [captcha URL](https://judgments.ecourts.gov.in/pdfsearch/vendor/securimage/securimage_show.php) and just refreshing it.

   
2. **Storing captcha image**: The approach of using the `execute_script` function to copy the captcha into the clipboard or storage was also unsuccessful.

3. **Google Lens Parsing**: Trying to parse the captcha with Google Lens did not work as controlling the newly opened window was problematic. The process consistently failed despite attempts to use the `title` or `window handle` of the tab.

![Selenium IDE Attempt](https://github.com/HistoriFy/SCR-Judgements/assets/67834542/a96368e3-205f-45f6-85ac-f638e8014260)

4. **HTML2Canvas, Axios/Fetch Attempt:** External libraries such as `html2canvas` and `axios/fetch` were necessary to capture a screenshot of the captcha and solve it through the OCR API. However, importing these libraries into the console of the tab controlled by Selenium IDE required the use of `<script>` tags. These scripts needed to be either hosted on a CDN or locally, and attention also had to be given to the CORS security of the page. This entire process proved to be challenging with just the `execute_script` support of Selenium IDE.


Ultimately, I transitioned to using the WebDriver approach. Suggestions for making the Selenium SIDE file work are greatly welcomed.

## Future Improvements That Can Be Done:

1. **Better and Faster OCR**: Leveraging advanced OCR solutions like GPT-4 or GPT-4-vision API could reduce downtime and improve accuracy.

2. **Dockerization**: Implementing Docker would ensure the script runs smoothly across different systems and can be easily scaled in the cloud.

3. **Class-Based Refactoring**: Improving the script structure through class-based refactoring would enhance maintainability and readability.

Additional improvement suggestions are always appreciated.


