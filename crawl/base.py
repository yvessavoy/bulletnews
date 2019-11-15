import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from tfidf import tfidf
from web import models


class Crawler:
    def __init__(self):
        self.base_url_cnt = 0
        self.articles_cnt = 0
        self.article_too_short = 0

    def get_page(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    def get_xml_page(self, url):
        r = requests.get(url)
        return ET.fromstring(r.text)

    def print_stats(self):
        print('*' * 80)
        print(f'Statistics for {self.origin} *')
        print('*' + '-' * 78 + '*')
        print(f'* - Base Urls queried: {self.base_url_cnt}')
        print(f'* - Articles queried: {self.articles_cnt}')
        print(f'* -- Articles to short: {self.article_too_short}')

    def store_tfidf(self, title, origin, url, text, amount, lang, publish_tsd):
        self.origin = origin
        if len(text) > 0:
            sentences = tfidf(text, amount, lang)
            if len(sentences) == amount:
                article = models.Article(title=title,
                                        origin=origin,
                                        insert_tsd=timezone.now(),
                                        publish_tsd=publish_tsd,
                                        original_url=url,
                                        bp1=sentences[0],
                                        bp2=sentences[1],
                                        bp3=sentences[2],
                                        bp4=sentences[3],
                                        bp5=sentences[4])
                article.save()
            else:
                self.article_too_short += 1
        else:
            self.article_too_short += 1