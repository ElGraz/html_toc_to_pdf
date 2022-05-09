from urllib import parse, request, response, error
from bs4 import BeautifulSoup

from page import Page


class Spider:
    """Spider to crawl pages from TOC"""
    __home_url = None

    def __init__(self, home: str):
        self.__home_url = home
        try:
            parsed = parse.urlparse(home)
            print(f"> Running spider via [{parsed.scheme}] at [{parsed.netloc}] with path [{parsed.path}]")
        except Exception as ex:
            print("Invalid URL inserted")
            print(ex)

    def get_pages(self) -> list[Page]:
        pages = list()
        print(f"= Getting homepage from {self.__home_url}")
        try:
            html = None
            with request.urlopen(self.__home_url) as home:
                data = home.read()
                print(f"= Got {len(data)} bytes of data")
                html = BeautifulSoup(data, 'html.parser')

            id = 0
            pages.append(Page(num=id, desc='TOC', url=self.__home_url))

            for link in html.find_all('a'):
                id += 1
                href = link.get('href')
                if not href or not link.text:
                    print(f"? Link {link} has no href")
                    continue
                page = Page(num=id, desc=link.text, url=self.__complete_url(href, self.__home_url))

                print(f"= found link to '{page.url}' with desc '{page.desc}' num '{page.num}'")
                pages.append(page)

        except error.URLError or error.HTTPError as ex:
            print(f"Invalid url: {ex}")

        return pages

    @staticmethod
    def __complete_url(url: str, baseurl: str):
        parsed = parse.urlparse(url)
        if len(parsed.scheme) == 0:
            return parse.urljoin(baseurl, url)
        return url


    @staticmethod
    def get_data(page) -> str:
        print(f"= getting data of page {page.num}: '{page.desc}'")
        with request.urlopen(page.url) as home:
            data = home.read()
        return data



