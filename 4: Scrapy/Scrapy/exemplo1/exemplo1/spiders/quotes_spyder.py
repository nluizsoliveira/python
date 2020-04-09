import scrapy
import datetime

def start_url_generator():
    base_url = 'http://www.economia.gov.br/agendas/gabinete-do-ministro/ministro-da-economia/paulo-guedes/'
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date.today()
    one_day = datetime.timedelta(days=1)

    start_urls = []
    while start_date < end_date:
        year  = str(start_date.year).zfill(4)
        month = str(start_date.month).zfill(2)
        day   = str(start_date.day).zfill(2)

        url_path = f'{year}-{month}-{day}?month:int={month}&year:int={year}'

        start_urls.append(f'{base_url}{url_path}')
        start_date += one_day

    return start_urls

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = start_url_generator()

    def parse(self, response):
        for compromisso in response.css('.item-compromisso'):  # Lista de Selectors

            yield {
                "MinistryName": response.css('.agenda-orgao::text').get(),
                "MinisterName": response.css('.agenda-autoridade::text').get(),
                "EventDate": compromisso.css('.horario.comprimisso-inicio').attrib['datetime'],
                "EventTitle": compromisso.css('.comprimisso-titulo::text').get(),
                "EventLocation": compromisso.css('.comprimisso-local ::text').getall()[2][1:], #Remove \n, Local: e espaço vazio
                "EventParticipants" : [nome[:-1] for nome in compromisso.css('.comprimisso-participantes::text').getall()[1:]] 
            }

    


