# Setup

from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import requests
import bs4
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--test-type")
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"  
driver = webdriver.Chrome(ChromeDriverManager().install())

# Enter Location and Job Role
driver.get('https://in.indeed.com/')
what = driver.find_element("id", "text-input-what")
where = driver.find_element("id", "text-input-where")
job_name = "software developer"
what.send_keys(job_name)
where.send_keys("Coimbatore")
time.sleep(10)

# Get Links and Job titles
driver.get("https://in.indeed.com/jobs?q=ai%2Fml&l=Coimbatore%2C+Tamil+Nadu&vjk=dfe1c8ef9b6bbbd5")
job_title_xp = """//div[@id="mosaic-jobResults"]//h2//span"""
job_titles = driver.find_elements(By.XPATH, job_title_xp)
job_titles = [job_title.text for job_title in job_titles]

job_href_xp = """//div[@id="mosaic-jobResults"]//h2//a"""
job_hrefs = driver.find_elements(By.XPATH, job_href_xp)
job_hrefs = [element.get_attribute("href") for element in job_hrefs]
# with open("links.txt", "w") as f:
#     for href in job_hrefs:
#         f.write(href)
#         f.write("\n")
# Extract and Print data

# def extract_source(url):
#      agent = {"User-Agent":"Mozilla/5.0"}
#      source=requests.get(url, headers=agent).text
#      print(source)
#      return source
def extract_data(url, id, title):
    driver.get(url)
    soup=bs4.BeautifulSoup(driver.page_source, 'html.parser')
    names=soup.findAll('title')
    with open(f"{job_name}.txt", "a", encoding="utf-8") as f:
       f.writelines("###ID")
       f.writelines(id)
       f.writelines("\n")
       f.writelines("###TITLE")
       f.writelines(title)
       f.writelines("\n")
    for i in names:
       print(i.text)
       # print(names.text)
       with open(f"{job_name}.txt", "a", encoding="utf-8") as f:
           f.writelines(i.text )
       with open(f"{job_name}.txt", "a", encoding="utf-8") as f:
           f.writelines("\n\n" )
    div_bs4 = soup.find('div', id = "jobDescriptionText")
    for div in div_bs4:
        
        print(div.text)
        with open(f"{job_name}.txt", "a", encoding="utf-8") as f:
           f.writelines(div.text)
        with open(f"{job_name}.txt", "a", encoding="utf-8") as f:
           f.writelines("\n\n" )
    with open(f"{job_name}.txt", "a", encoding="utf-8") as f:
           f.writelines("\n\n\n\n\n\n" )
        
         

# with open("links.txt", "r") as f:
#     links = f.readlines()
# print(links[0][:-2])
# cleaned_links = [link[:-2] for link in links]
# print(cleaned_links)
id = 0
for link,title in zip(job_hrefs, job_titles):  
    # print(link)
    extract_data(link, str(id), title)
    id+=1
# extract_data("https://in.indeed.com/company/YOROSIS-Technologies/jobs/Engineer-dfe1c8ef9b6bbbd5?fccid=849cd718a80914e4&vjs=")