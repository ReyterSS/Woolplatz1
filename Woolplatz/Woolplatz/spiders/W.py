import scrapy
from scrapy import Request


class WSpider(scrapy.Spider):
    name = "W"
    custom_settings = {"FEEDS": { "%(time)s.csv": {"format": "csv"}}}

    def start_requests(self):
        #Get list of search
        f = open("Titles.txt")
        for i in f.readlines():
            # Get name of brand
            brand = i.split(' ')[0]
            # Get title
            title = i.replace(f'{brand}', '').replace(' ','-')
            url = f'https://www.wollplatz.de/wolle/{brand}/{brand}{title}'
            yield Request(
                url=url,
                callback=self.parse,
            )
        # close file with list
        f.close()
    #
    def parse(self, response):
        title = response.xpath('//h1[@id="pageheadertitle"]//text()').get()
        needle_size = response.xpath(
            '//div[@id="pdetailTableSpecs"]//tr/td[contains(., "Nadelstärke")]//following-sibling::td//text()').get()
        avaliability1 = response.xpath(
            '//div[@id="ContentPlaceHolder1_upCartBuyButton"][contains(., "In den Warenkorb")]').get()
        if avaliability1 is not None:
            avaliability = 'Yes'
        else:
            avaliability = 'None'
        composition = response.xpath('//td[@class="sb-container"]//div[@class="variants-group-container"]//text()')[
                      1:].getall()
        # store data in dict
        data = {
            'Title': title,
            'Needle Size': needle_size,
            'Avaliability': avaliability,
            'Composition': composition
        }
        yield data

