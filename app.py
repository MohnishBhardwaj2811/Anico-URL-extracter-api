from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, request, jsonify, render_template
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode (without GUI)
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-images')  # Disable loading of images

# Set up the Chrome webdriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.implicitly_wait(1)  # Set implicit wait to 1 second

def main(url):
    attempt = 1
    while True:
        print("Attempted:" + str(attempt))
        attempt += 1
        driver.get(url)
        # Find elements directly without explicit waiting
        download_elements = driver.find_elements(By.CLASS_NAME, 'download')

        if download_elements:
            break

    data = {}
    for download_element in download_elements:
        download_link = download_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        download_text = download_element.find_element(By.TAG_NAME, 'a').text

        if "https://gredirect.info/download.php?" in download_link:
            # Print the extracted information
            data[download_text] = download_link

    return data

# Close the browser window
# This should be placed outside the main function to ensure it gets called
# even if an exception occurs.
try:
    app = Flask(__name__)

    # Home
    @app.route("/<user_id>")
    def get_home(user_id):
        url = 'https://embtaku.pro/download?id=' + user_id
        print(user_id)
        try:
            data = main(url)
            return jsonify(data)
        except:
            return {"data": "data not found", "data_code": 404}
    finally:
        driver.quit()
