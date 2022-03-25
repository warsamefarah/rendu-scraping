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

    def get_table(self, titles):
        tables = self.get_html_page().find_all(class_="table_wrapper")
        selected = []
        for table in tables:
            for title in titles:
                if title in table.get_text():
                    selected.append(table)
        return selected

    def get_titles_over_header(self, trs):
        over_headers = trs[0].find_all('th')
        headers = trs[1].find_all('th')
        res = [] # [[joueur, [Pos, age]], [Tps de jeu, [min, ...]]]
        for i, over_header in enumerate(over_headers):
            if over_header.get_text() == '':
                res.append([headers[0].get_text(), []])
                tmp = headers[1:]
                headers = tmp
            else:
                res.append([over_header.get_text(), []])
            for header in headers:
                res[i][1].append(header.get_text())
                tmp = headers[1:]
                headers = tmp
                if 'group_start' in headers[0]['class']:
                    break
        print(res)
        return res

    def get_titles(self, table):
        thead = table.find('thead')
        trs = thead.find_all('tr')
        if len(trs) > 1:
            res = self.get_titles_over_header(trs)
            return res
        
        ths = trs[0].find_all('th')
        res = []
        for th in ths:
            res.append(th.get_text())
        return res

    def parse_table(self, table):
        headers = table.find(class_="over_header")
        header = headers.find_all('th') # Vide / tps de jeu ...
        next_headers = headers.findNext('tr')
        next_header = next_headers.find_all('th')
        
            




        



if __name__ == "__main__":
    get_links = SiteScraper(r'https://fbref.com/fr/equipes/361ca564/Statistiques-Tottenham-Hotspur')
    tables = get_links.get_table([
        'Statistiques basiques 2021-2022 Tottenham Hotspur: Premier League',
        'Calendrier et résultats 2021-2022 Tottenham Hotspur: Toutes les compétitions',
        'Tirs 2021-2022 Tottenham Hotspur: Premier League'
    ])
    get_links.get_titles(tables[0])
    # print(len(get_links))