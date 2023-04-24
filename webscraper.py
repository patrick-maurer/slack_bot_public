from bs4 import BeautifulSoup
import requests


def status(code, author):
    """
    get status of a given article

    :param code: article code
    :param author: author last name
    :return: status of the article
    """

    URL = f"https://authors.aps.org/Submissions/status?&accode={code}&author={author}"
    page_to_scrape = requests.get(URL)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    return soup.findAll("td")[0].text.strip("\n")
