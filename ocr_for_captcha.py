# We use OCR.space API to solve the captcha. 
# It is a paid service, but you can get a free API key for 25,000 requests per month.
# You can sign up for a free account at https://ocr.space/ocrapi


# We use the `requests` library to send a POST request to the OCR.space API endpoint.
# We pass the captcha image as a base64 encoded string in the request payload.
# The API key is passed in the request headers.
# The response is in JSON format, and we extract the text from the `ParsedResults` field.
# The extracted text is then returned to the calling function.

# We are currently using engine 2 for OCR which is better for numbers and special characters.

import requests

from utils import image_to_base64, capture_captcha_image

def solve_captcha(image_path):
    """Solve the captcha using OCR.space API.

    Args:
        image_path (str): Path to the captcha image. It is stored as `captcha.png` in the current working directory.

    Returns:
        str: Extracted text from the captcha image.
    """    
    base64_image = f'data:image/png;base64,{image_to_base64(image_path)}'
    ocr_url = "https://api.ocr.space/parse/image"
    payload = {'language': 'eng', 'filetype': 'PNG', 'OCREngine': '2'}
    files = {'base64image': (None, base64_image)}
    headers = {'apikey': 'K89610423888957'}  # Replace with your OCR.space API key

    response = requests.post(ocr_url, headers=headers, data=payload, files=files)
    result = response.json()
    
    if 'ParsedResults' in result and len(result['ParsedResults']) > 0:
        return result['ParsedResults'][0]['ParsedText'].strip()
    return None