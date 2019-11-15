import logging
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from tfidf import tfidf
from web import models


class Crawler:
    def __init__(self):
        self.max_articles = 0
        self.processed_articles = 0

    def get_logger(self, mod_name):
        logger = logging.getLogger(mod_name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def get_page(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    def get_xml_page(self, url):
        r = requests.get(url)
        return ET.fromstring(r.text)

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
        self.processed_articles += 1
        self.logger.info(f'{self.processed_articles:03d} / {self.max_articles:03d}')
