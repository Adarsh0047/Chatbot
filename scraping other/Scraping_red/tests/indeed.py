from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"  
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://in.indeed.com/')
what = driver.find_element("id", "text-input-what")
where = driver.find_element("id", "text-input-where")
# text_area = driver.find_element_by_id('textarea')
what.send_keys("AI/ML")
where.send_keys("Coimbatore")
time.sleep(10)
l = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
driver.execute_script("arguments[0].click();", l)
print("Page title is: ")
print(driver.current_url)
time.sleep(10)
