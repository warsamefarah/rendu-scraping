from cgitb import text
import requests
from bs4 import BeautifulSoup

class SiteScraper:
    url: str = ''

    def __init__(self, url) -> None:
        self.url = url


    def get_html_page(self):
        page = requests.get(self.url).text
        return BeautifulSoup(page, 'html.parser')

    def get_table(self):
        table = self.get_html_page().find_all(class_="table_wrapper")
        return table

if __name__ == "__main__":
    get_links = SiteScraper(r'https://fbref.com/fr/equipes/361ca564/Statistiques-Tottenham-Hotspur').get_table()
    print(get_links)