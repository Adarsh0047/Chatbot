import requests
from bs4 import BeautifulSoup

def extract(page):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0"}
    url = f"https://in.indeed.com/jobs?q=AI%2FML&l=Tamil+Nadu&start={page}"
    r = requests.get(url, headers)
    return r.status_code
print(extract(0))

