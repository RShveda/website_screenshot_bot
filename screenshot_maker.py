from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import uuid

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080


def resize_image(img_name: str):
    basewidth = 1024
    img = Image.open(img_name)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(img_name)


def make_image(web_url):
    DRIVER = 'chromedriver'
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Chrome(DRIVER, options=driver_options)
    driver.get(web_url)
    height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.body.clientHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
    driver.set_window_size(DEFAULT_WIDTH, height, windowHandle='current')
    time.sleep(7)
    screenshot_name = str(uuid.uuid4()) + ".png"
    driver.save_screenshot(screenshot_name)
    resize_image(screenshot_name)
    driver.quit()
    return screenshot_name


def test_driver(web_url):
    DRIVER = 'chromedriver'
    driver_options = Options()
    driver_options.add_argument("--headless")
    # driver_options.add_argument("--user-agent = Chrome/86.0.4240.183")
    driver = webdriver.Chrome(DRIVER, options=driver_options)
    driver.get(web_url)
    time.sleep(30)
    driver.quit()


if __name__ == '__main__':
    test_driver("https://www.amazon.com/")