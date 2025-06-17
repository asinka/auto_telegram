from datetime import date
from typing import List

from bs4 import BeautifulSoup

from news_sources.base_news_source import BaseNewsSource
from news_sources.types import N1News


class N1NewsSource(BaseNewsSource):
    SOURCE_MAIN_URL = 'https://n1info.rs/'
    SOURCE = 'N1'

    def __init__(self):
        super().__init__(url = 'https://n1info.rs/vesti/')

    def _get_raw_today_news(self) -> List[BeautifulSoup]:
        return self.parsed_source.find_all(name='article')

    def _map_raw_news(self, raw_news: List[BeautifulSoup]) -> List[N1News]:
        result = []
        for raw_one_news in raw_news:
            article_soup = self._get_article_soup(raw_news=raw_one_news)
            try:
                result.append(
                    N1News(
                        title=self._get_title(article_soup).strip(),
                        summary=self._get_summary(article_soup).strip(),
                        img_url=self._get_image_url(article_soup)
                    )
                )
            except Exception:
                pass
        return result

    def _get_article_url(self, raw_news: BeautifulSoup) -> str:
        url = raw_news.find(name='a').attrs['href'].lstrip()
        return f'{self.SOURCE_MAIN_URL}{url}'

    def _get_title(self, article_soup: BeautifulSoup) -> str:
        return article_soup.find(name='h1').text

    def _get_summary(self, article_soup: BeautifulSoup) -> str:
        return article_soup.find(
            name='p',
            attrs={'data-testid' : 'article-lead-text'}
        ).text

    def _get_image_url(self, article_soup: BeautifulSoup) -> str:
        image_url = article_soup.find(
            name='img',
            attrs={'data-selector':'image-with-caption'}
        ).attrs['srcset'].split(',')[-1].split()[0]
        return f'{self.SOURCE_MAIN_URL}{image_url}'
