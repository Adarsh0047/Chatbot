from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_argument('headless')
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--test-type")
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"  
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://in.indeed.com/viewjob?cmp=YOROSIS-Technologies&t=Engineer&jk=dfe1c8ef9b6bbbd5&vjs=3")
title_xpath= """//h1/span"""

title = driver.find_element(By.XPATH, title_xpath).text
job_desc_xpath = """//div[@id="jobDetailsSection"]/div[2]/div[2]/div/div/div/div"""
desc_lis = driver.find_elements(By.XPATH, job_desc_xpath)
descs = []
for i in desc_lis:
    descs.append(i.text)

qualifications_xpath = """//div[@id="qualificationsSection"]/div[2]/div/ul/li/p"""
qualifications_elems = driver.find_elements(By.XPATH, qualifications_xpath)
qualifications = []
for i in qualifications_elems:
    qualifications.append(i.text)
print(title)
print(descs)
print(qualifications)
about_xpath = """//div[@id="jobDescriptionText"]/ul/li"""
about = driver.find_element(By.XPATH, about_xpath).text
print(about)
