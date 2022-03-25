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
        over_headers = trs[0].find_all(class_='over_header')
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
        res.append([headers[0].get_text(), []])
        return res

    def get_titles(self, table):
        thead = table.find('thead')
        trs = thead.find_all('tr')
        if len(trs) > 1:
            res = self.get_titles_over_header(trs)
            return (res, True)
        
        ths = trs[0].find_all('th')
        res = []
        for th in ths:
            res.append(th.get_text())
        return (res, False)


    def get_items_over_header(self, table, titles):
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        t_res = []
        for tr in trs:
            res = {}
            tr_items = [x.get_text() for x in tr.find_all('th') + tr.find_all('td')]
            for title in titles:
                res[title[0]] = {}
                if title == titles[0]:
                    res[title[0]]["Nom"] = tr_items[0]
                    tmp = tr_items[1:]
                    tr_items = tmp
                for sub_title in title[1]:
                    res[sub_title] = tr_items[0]
                    tmp = tr_items[1:]
                    tr_items = tmp
            t_res.append(res)
        print(t_res)
        return t_res

    def get_items(self, table, titles):
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        t_res = []
        for tr in trs:
            res = {}
            tr_items = [x.get_text() for x in tr.find_all('th') + tr.find_all('td')]
            for i,title in enumerate(titles):
                res[title] = tr_items[i]
            t_res.append(res)
        print(t_res)
        return t_res

    def parse_table(self, table):
        titles, has_over_header = self.get_titles(table)

        if has_over_header:
            return self.get_items_over_header(table, titles)
        return self.get_items(table, titles)



if __name__ == "__main__":
    get_links = SiteScraper(r'https://fbref.com/fr/equipes/361ca564/Statistiques-Tottenham-Hotspur')
    tables = get_links.get_table([
        'Statistiques basiques 2021-2022 Tottenham Hotspur: Premier League',
        'Calendrier et résultats 2021-2022 Tottenham Hotspur: Toutes les compétitions',
        'Tirs 2021-2022 Tottenham Hotspur: Premier League'
    ])
    get_links.parse_table(tables[0])
    # print(len(get_links))