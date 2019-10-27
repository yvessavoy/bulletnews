from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from tfidf import tfidf
import web.models as models


class Crawler:
    def __init__(self):
        self.base_url = 'https://bbc.com'
        self.article_list_url = self.base_url + '/news/world/'
        self.article_link_class = 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'
        self.title_tag = 'story-body__h1'
        self.story_tag = 'story-body__inner'
        self.classes_to_ignore = ['Tweet-text']

    def crawl(self):
        r = requests.get(self.article_list_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        article_urls = []
        for article in soup.find_all('a', class_=self.article_link_class):
            url = urljoin(self.base_url, article.get('href'))
            if url not in article_urls:
                article_urls.append(url)

        for url in article_urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            title = soup.find('h1', class_=self.title_tag)
            if title:
                story = soup.find('div', class_=self.story_tag)
                if story:
                    story_text = ""
                    for p in story.find_all('p'):
                        if len(p.text) > 0:
                            if (p.has_attr('class') and p['class'][0] != 'Tweet-text') or not p.has_attr('class'):
                                story_text += p.text
                                if p.text[-1] == '.':
                                    story_text += ' '
                    top_sents = tfidf(story_text, 5, 'english')

                    article = models.Article(title=title.text,
                                             origin='bbc',
                                             insert_tsd=timezone.now(),
                                             original_url=url,
                                             bp1=top_sents[0]['sentence'],
                                             bp2=top_sents[1]['sentence'],
                                             bp3=top_sents[2]['sentence'],
                                             bp4=top_sents[3]['sentence'],
                                             bp5=top_sents[4]['sentence'])
                    article.save()
