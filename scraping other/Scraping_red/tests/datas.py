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
links = []
with open("links.txt", "r") as f:
    links = f.readlines()
# print(links[0][:-2])
cleaned_links = [link[:-2] for link in links]
print(cleaned_links)

for link in cleaned_links:
    driver.get(link)
    try:
        title_xpath= """//h1/span"""
        title = "###TITLE:   " + driver.find_element(By.XPATH, title_xpath).text
    except:
        title_xpath = """//head/title"""
        title = "###TITLE:   " + driver.find_element(By.XPATH, title_xpath).text
    job_desc_xpath = """//div[@id="jobDetailsSection"]/div[2]/div[2]/div/div/div/div"""
    desc_lis = driver.find_elements(By.XPATH, job_desc_xpath)
    descs = []
    for i in desc_lis:
        descs.append("###DESC:   " +i.text)
    

    qualifications_xpath = """//div[@id="qualificationsSection"]/div[2]/div/ul/li/p"""
    qualifications_elems = driver.find_elements(By.XPATH, qualifications_xpath)
    qualifications = []
    for i in qualifications_elems:
        qualifications.append("###QUALIFICATIONS:   " + i.text)
    about_xpath = """//div[@id="jobDescriptionText"]/ul/li"""
    about = "###ABOUT:   " + driver.find_element(By.XPATH, about_xpath).text
    with open("jobs.txt", "a") as f:
        f.writelines(title)
        f.writelines([desc for desc in descs])
        f.writelines([qual for qual in qualifications])
        f.writelines(about)

# temp = file.read().splitlines()