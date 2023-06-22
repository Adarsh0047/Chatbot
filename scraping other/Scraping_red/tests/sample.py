from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"  
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('http://codepad.org')
text_area = driver.find_element("id", "textarea")
# text_area = driver.find_element_by_id('textarea')
text_area.send_keys("This text is send using Python code.")
time.sleep(10)
