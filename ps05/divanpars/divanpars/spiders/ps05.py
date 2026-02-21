import scrapy

class SvetSpider(scrapy.Spider):
    name = "svet"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    custom_settings = {
        'FEEDS': {
            'divan_lights.csv': {
                'format': 'csv',
                'encoding': 'utf-8-sig',      
                'store_empty': False,
                'fields': ['Название', 'Цена', 'Ссылка'],
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        products = response.css('div[class*="ProductCardMain_container"]')

        for product in products:
            name = product.css('[itemprop="name"]::text').get()
            if not name:
                name = product.css('a[href*="/product/"]::text').get()

            relative_link = product.css('a[href*="/product/"]::attr(href)').get()
            link = response.urljoin(relative_link) if relative_link else None

            price = product.css('span[data-testid="price"]::text').get()
            if price:
                price = price.replace('\xa0', ' ').strip()

            if name and link and price:
                yield {
                    'Название': name.strip(),
                    'Цена': price,
                    'Ссылка': link,
                }

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)