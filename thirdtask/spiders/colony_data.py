from scrapy import Request
from uuid import uuid4
import csv
import scrapy

class colony_data(scrapy.Spider):
    name="colony_data"
    
    def start_requests(self):
        yield Request('http://nwcmc.gov.in/ptsearch_nanded.php',
            meta={'cookiejar':str(uuid4)},
            callback=self.parse) 
   
    def parse(self,response):
        data=response.xpath('//*[@id="colony"]/option/@value')[1:11].getall()
        for colony_no in data:
            print(colony_no,'***************************************************************')
            yield Request('http://nwcmc.gov.in/ptsearch_data.php?colony={}&houseno=&name=&address=&serno='.format(colony_no),
                meta={'cookiejar':str(uuid4),'colony':colony_no},
                callback=self.get_colonies)

    def get_colonies(self,response):
        table=response.xpath('/html/body/table')
        with open('colony_data_{}.csv'.format(response.meta['colony']),'a') as f:
            wr=csv.writer(f)
            for tr in table.xpath('.//tr'):
                _tdata=[]
                        
                for td in tr.xpath('.//td'):
                    _text=''.join([a for a in td.xpath('.//text()').extract()])
                    _tdata.append(_text)
                wr.writerow(_tdata)
