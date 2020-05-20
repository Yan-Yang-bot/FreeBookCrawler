import scrapy
import requests
from os import path

urls = ["https://link.springer.com/search/page/{}?facet-content-type=%22Book%22&package=mat-covid19_textbooks&facet-language=%22En%22&sortOrder=newestFirst&showAll=true", "https://link.springer.com/search/page/{}?facet-content-type=%22Book%22&package=mat-covid19_textbooks&facet-language=%22En%22&sortOrder=oldestFirst&showAll=true"]

class BookSpider(scrapy.Spider):
    counter = 0
    dup = 0
    name = 'bookspider'
    start_urls = [url.format(i) for i in range(1, 22) for url in urls]
    download_page_link_css = 'ol#results-list li div.text h2 a.title'
    title_css = 'div.main-context div.page-title h1::text'
    pdf_download_css = 'div.main-container div.cta-button-container__item:first-child a::attr(href)'

    def download(self, response):
        title = response.css(self.title_css).extract_first()
        title = title.replace('/', '\\') + '.pdf'
        if path.isfile(title):
            self.dup += 1
            print('DUPLICATED:', title)
        else:
            self.counter += 1
            pdf_path = response.css(self.pdf_download_css).extract_first()
            myfile = requests.get('https://link.springer.com' + pdf_path)
            open(title, 'wb').write(myfile.content)

    def parse(self, response):
        for download_page in response.css(self.download_page_link_css):
            yield response.follow(download_page, self.download, dont_filter=True)

    def __del__(self):
        print(self.counter, 'downloaded', self.dup, 'duplication')
