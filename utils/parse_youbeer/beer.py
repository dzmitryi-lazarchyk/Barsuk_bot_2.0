import requests
from bs4 import BeautifulSoup
import re

from tgbot.models.database import Tap, Jar

page_url = "https://your.beer/place/barsuk"
page_params = {
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    },
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": None,
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
}


def fetch(url, params):
    headers = params['headers']
    body = params['body']
    if params['method'] == 'GET':
        return requests.get(url, headers=headers)
    if params['method'] == 'POST':
        return requests.get(url, headers=headers, data=body)


def parse_yourbear(product: str):
    page = fetch(page_url, page_params)
    soup = BeautifulSoup(page.text, "html.parser")
    if product == "taps":
        items = soup.find('div', class_='tab-body').find('div', class_='b-list'). \
            find('div', class_='row').find_next_sibling('div'). \
            find_all('div', class_='b-card col-xs-12 col-sm-12 col-md-12 col-lg-12 col-xl-6')
        bear = []

        for item in items:
            sort_raw = item.find('div', class_="b-characteristics").get_text().strip()
            sort = re.sub(r'\s+•\s+', ', ', sort_raw)

            price_list = ""
            prices = item.find_all('div', class_="b-skus-data d-flex justify-content-start")
            for el in prices:
                price = el.get_text().strip().translate(el.get_text().strip().maketrans('\n', ' '))
                price_list = price_list + '\n' + price
            price_list = price_list.strip()

            bear.append(Tap(
                tap=int(item.find('h2', class_="b-card-tap").get('data-tap')),
                name=item.find('h2', class_="b-card-tap").find('a').get_text(),
                brewery=item.find('h3').find('a').get_text(),
                link=item.find('h2', class_="b-card-tap").find('a').get('href'),
                image=item.find('div', class_="b-logo justify-content-start").find('a').get('data-bg'),
                sort=sort,
                price_list=price_list,
            ))
        return bear
    elif product == "jars":
        items = soup.find('div', class_='tab-body').find('div', class_='b-list mt-3'). \
            find('div', class_='row').find_next_sibling('div').find_next_sibling('div'). \
            find_all('div', class_='b-card col-xs-12 col-sm-12 col-md-12 col-lg-12 col-xl-6')

        bear = []
        for item in items:
            sort_raw = item.find('div', class_="b-characteristics").get_text().strip()
            sort = re.sub(r'\s+•\s+', ', ', sort_raw)

            price_list = item.find('div', class_="b-skus-type").get_text() + item.find('div',
                                                                                       class_="b-skus-price ml-auto").get_text()

            bear.append(Jar(
                name=item.find('h2').find('a').get_text(),
                brewery=item.find('h3').find('a').get_text(),
                link=item.find('h2').find('a').get('href'),
                image=item.find('div', class_="b-logo justify-content-start").find('a').get('data-bg'),
                sort=sort,
                price_list=price_list,
            ))

        return bear
