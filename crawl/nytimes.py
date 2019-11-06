from base import Crawler


class NyTimesWorld(Crawler):
    def __init__(self):
        super().__init__(origin='nytimes'
                       , base_url='https://www.nytimes.com'
                       , list_url='section/world'
                       , article_url_class=None
                       , article_url_tle='div'
                       , article_url_tle_class='css-10wtrbd'
                       , article_title_in_head=True
                       , article_detail_text_tag='p'
                       , article_detail_text_class='css-exrw3m evys1bk0')
