from bs4 import BeautifulSoup
import requests


def url(code, author):
    URL = f"https://authors.aps.org/Submissions/status?&accode={code}&author={author}"
    page_to_scrape = requests.get(URL)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    return soup.findAll("td")[0].text.strip("\n")
