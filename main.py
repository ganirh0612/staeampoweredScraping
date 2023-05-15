import os

import pandas as pd
import requests
import bs4
import json
import pandas

url = 'https://store.steampowered.com/search/?snr=1_4_4__12&term=dota'

#Request Data from Steampowred.com
def get_data(url):
    req = requests.get(url)
    return req.text

#Processing Data
def parse(data):
    result = []
    soup = bs4.BeautifulSoup(data, 'html.parser')

    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    content = soup.find('div', attrs={'id': 'search_resultsRows'})
    games = content.find_all('a')

    for game in games:

        link = game['href']
        # Parsing Data
        title = game.find('span', {'class': 'title'}).text.strip().split('£')[0]
        price = game.find('div', {'class': 'search_price'}).text.strip().split('£')[0]
        release = game.find('div', {'class': 'search_released'}).text.strip().split('£')[0]

        if release == '':
            release = 'none'

        #Sorting Data
        data_dict = {
            'title': title,
            'price': price,
            'link': link,
            'release': release
        }

        #Append Data
        result.append(data_dict)

    return result

#Read and Write JSON
    with open('json_result.json', 'w') as outfile:
        json.dump(result, outfile)
    return

def loadData():
    with open('json_result.json') as json_file:
        data = json.load(json_file)

#Process Clean Data from Parser
def output(datas: list):
    for i in datas:
        print(i)

def generateData(result, filename):

    df = pd.DataFrame(result)
    df.to_excel(f'{filename}.xlsx', index=False)

if __name__ == '__main__':
    data = get_data(url)
    final_data = parse(data)
    nameFile = input('Insert Name File:')
    generateData(final_data, nameFile)
    output(final_data)

