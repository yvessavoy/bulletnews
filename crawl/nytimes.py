from base import Crawler


class NyTimes(Crawler):
    def __init__(self):
        super().__init__()
        self.urls = [
            'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'
        ]
        self.story_class = 'css-exrw3m evys1bk0'
        self.base_url_cnt = len(urls)

    def crawl(self):
        for url in self.urls:
            article_rss = self.get_xml_page(url)
            for item in article_rss[0]:
                if item.tag == 'item':
                    self.article_urls += 1
                    title = item[0].text
                    original_url = item[2].text
                    story_text, publish_tsd = self.get_details(self.get_page(original_url))
                    self.store_tfidf(title, 'nytimes', original_url, story_text, 5, 'english', publish_tsd)

    def get_details(self, soup):
        story_text = ""
        publish_tsd = soup.find('meta', property='article:published')
        publish_tsd = publish_tsd['content'] if publish_tsd else '1990-01-01T00:00:00.000Z'
        story_p = soup.find_all('p', class_=self.story_class)
        for p in story_p:
            if len(p.text) > 0:
                story_text += p.text
                if p.text.endswith('.'):
                    story_text += ' '
        return story_text, publish_tsd
