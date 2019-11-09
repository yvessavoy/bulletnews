import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from tfidf import tfidf
from web import models


class Crawler:
    def get_page(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    def get_xml_page(self, url):
        r = requests.get(url)
        return ET.fromstring(r.text)

    def store_tfidf(self, title, origin, url, text, amount, lang):
        if len(text) > 0:
            sentences = tfidf(text, amount, lang)
            article = models.Article(title=title,
                                    origin=origin,
                                    insert_tsd=timezone.now(),
                                    original_url=url,
                                    bp1=sentences[0],
                                    bp2=sentences[1],
                                    bp3=sentences[2],
                                    bp4=sentences[3],
                                    bp5=sentences[4])
            article.save()