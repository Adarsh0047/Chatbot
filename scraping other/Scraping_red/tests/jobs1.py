from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://in.indeed.com/jobs?q=ai%2Fml&l=Coimbatore%2C+Tamil+Nadu&vjk=dfe1c8ef9b6bbbd5")
job_title_xp = """//div[@id="mosaic-jobResults"]//h2//span"""
job_titles = driver.find_elements(By.XPATH, job_title_xp)
job_titles = [job_title.text for job_title in job_titles]

job_href_xp = """//div[@id="mosaic-jobResults"]//h2//a"""
job_hrefs = driver.find_elements(By.XPATH, job_href_xp)
job_hrefs = [element.get_attribute("href") for element in job_hrefs]
with open("links.txt", "w") as f:
    for href in job_hrefs:
        f.write(href)
        f.write("\n")
