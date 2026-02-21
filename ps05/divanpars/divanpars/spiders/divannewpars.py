import scrapy

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]

    def parse(self, response):
        # Создаём переменную, в которую будет сохраняться информация
        # Находим все карточки товаров по общему классу
        divans = response.css('div._Ud0k')

        # Настраиваем работу с каждым отдельным диваном в списке
        for divan in divans:
            # Используем оператор yield, который помогает обрабатывать одно отдельное действие
            # и позволяет управлять потоком выполнения, останавливать и возобновлять работу парсера
            yield {
                # Название: ищем внутри карточки div с классом lsooF, внутри него тег span, берём текст
                'name': divan.css('div.lsooF span::text').get(),
                # Цена: ищем внутри карточки div с классом pY3d2, внутри него тег span, берём текст
                'price': divan.css('div.pY3d2 span::text').get(),
                # Ссылка: ищем тег a и извлекаем значение атрибута href
                'url': divan.css('a').attrib['href']
            }