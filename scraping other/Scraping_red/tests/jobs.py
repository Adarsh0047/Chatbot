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
driver.get("https://in.indeed.com/jobs?q=Ai%2FML&l=Coimbatore%2C+Tamil+Nadu&from=searchOnHP&vjk=7be6085817e5e2a7")
xpath = """//div[@class="css-1m4cuuf e37uo190"]//h2/a/@href"""

elements = driver.find_elements(By.XPATH, """//div[@class="css-1m4cuuf e37uo190"]//h2/a""")
hrefs = [element.get_attribute("href") for element in elements]
# href = element.get_attribute('href')
# print(href)
print(hrefs)
with open("links.txt", "w") as f:
    for href in hrefs:
        f.write(href)
        f.write("\n")

with open("links.txt", "r") as f:
    links = f.readlines()
print(links[0][:-2])
cleaned_links = [link[:-2] for link in links]
id = 0
for link,title in zip(cleaned_links, job_titles):  
    # print(link)
    extract_data(link, str(id), title)
    id+=1

