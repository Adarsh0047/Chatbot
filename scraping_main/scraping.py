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

# # Enter Location and Job Role
# driver.get('https://in.indeed.com/')
# what = driver.find_element("id", "text-input-what")
# where = driver.find_element("id", "text-input-where")
# what.send_keys("AI/ML")
# where.send_keys("Coimbatore")
# time.sleep(10)
# l = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
# driver.execute_script("arguments[0].click();", l)
# loc_url = driver.current_url


# # Get Links and Job titles
# driver.get(loc_url)
# job_title_xp = """//div[@id="mosaic-jobResults"]//h2//span"""
# job_titles = driver.find_elements(By.XPATH, job_title_xp)
# job_titles = [job_title.text for job_title in job_titles]

# with open("links.txt", "r", encoding="utf-8") as f:
#     links = f.readlines()



# def extract_data(url, id, title):
#     driver.get(url)
#     soup=bs4.BeautifulSoup(driver.page_source, 'html.parser')
#     names=soup.findAll('title')
#     with open("jobs.txt", "a", encoding="utf-8") as f:
#        f.writelines("###ID")
#        f.writelines(id)
#        f.writelines("\n")
#        f.writelines("###TITLE")
#        f.writelines(title)
#        f.writelines("\n")
#     for i in names:
#        print(i.text)
#        # print(names.text)
#        with open("jobs.txt", "a", encoding="utf-8") as f:
#            f.writelines(i.text )
#        with open("jobs.txt", "a", encoding="utf-8") as f:
#            f.writelines("\n" )
#     div_bs4 = soup.find('div', id = "jobDescriptionText")
#     for div in div_bs4:
#         print(div.text)
#         with open("jobs.txt", "a", encoding="utf-8") as f:
#            f.writelines(div.text)
#         with open("jobs.txt", "a", encoding="utf-8") as f:
#            f.writelines("\n" )
#     with open("jobs.txt", "a", encoding="utf-8") as f:
#            f.writelines("\n\n\n\n\n\n" )
        
         

# with open("links.txt", "r") as f:
#     links = f.readlines()
# print(links[0][:-2])
# cleaned_links = [link[:-2] for link in links]
# # print(cleaned_links)
# id = 0
# for link,title in zip(cleaned_links, job_titles):  
#     # print(link)
#     extract_data(link, str(id), title)
#     id+=1
# for link in links:
#     driver.get("link")
#     soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
#     div_bs4 = soup.find('div', id = "jobDescriptionText")
#     print(div_bs4.text)

with open("links.txt", "r") as f:
    links = f.readlines()
cleaned_links = [link[:-2] for link in links]
for link in cleaned_links:
    driver.get(link)