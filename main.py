#!/usr/bin/python

import os
import requests
import json
from bs4 import BeautifulSoup as bf

def get_table_header(soup):
    ret = {}
    theads = soup.find_all('thead', {'class': 'table-header'})
    for t in theads:
        ret[t.th.get_text().strip()] = []
    return ret


def get_data(soup):
    l_td = []
    trow = soup.find_all('tr', {'data-id': True})
    for tr in trow:
        l_data = []
        if tr.name != 'tr':
            print('con')
            continue

        tid = 1
        data = {
            'time': '',
            'title': '',
            'metadata': {
                'actual': '',
                'previous': '',
                'consensus': '',
                'forecast': ''
            }
        }
        for td in tr.find_all('td'):
            if tid == 1:
                data['time'] = td.get_text().strip()
            elif tid == 2:
                data['metadata']['country'] = td.table.tr.td.div['title']
            elif tid == 3:
                tid += 1
                continue
            elif tid == 4:
                tid += 1
                continue
            elif tid == 5:
                data['title'] = td.a and td.a.get_text() or ''
            elif tid == 6:
                data['metadata']['actual'] = td.a and td.a.get_text() or ''
            elif tid == 7:
                data['metadata']['previous'] = td.span and td.span.get_text() or ''
            elif tid == 8:
                data['metadata']['consensus'] = td.span and td.span.get_text() or ''
            elif tid == 9:
                data['metadata']['forecast'] = td.a and td.a.get_text() or ''
            tid += 1
        l_td.append(data)
    return l_td

def get_result(soup):
    result = json.dumps(get_data(soup))
    return result

if __name__ == '__main__':
    header = {"User-Agent" :"Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    r = requests.get('https://tradingeconomics.com/calendar', headers=header)
    soup = bf(r.text, 'html.parser')

    print(get_result(soup))
