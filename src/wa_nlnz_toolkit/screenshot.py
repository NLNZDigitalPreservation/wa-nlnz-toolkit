import time
import os
import validators
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from wa_nlnz_toolkit._config import header


def screenshot_webpage(url, output_path="/content/screenshot.png", delay=2):
    """
    Takes a screenshot of the given webpage and saves it to output_path.

    Parameters:
        url (str): The webpage URL.
        output_path (str): File path to save the screenshot.
        delay (int): Seconds to wait for page loading before capturing.
    """
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    if not validators.url(url):
        raise ValueError(f"Invalid URL: {url}")

    if os.path.isdir(output_path):
        output_path = os.path.join(output_path, "screenshot.png")

    if not output_path.lower().endswith(".png"):
        output_path = f"{output_path}.png"

    # Automatically install the matching ChromeDriver version
    chromedriver_path = chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,4000")

    # ✅ Add custom User-Agent here
    chrome_options.add_argument(f"--user-agent={header['User-Agent']}")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(delay)  # wait for page to load
        driver.save_screenshot(output_path)
        print(f"✅ Screenshot saved to: {output_path}")
    finally:
        driver.quit()
