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
        data=response.xpath('//select/option/text()')[5:].getall()
        colony_list=[]
        for colony in data:
            colony_list.append(colony)
            yield Request('http://nwcmc.gov.in/ptsearch_data.php?colony={colony}&houseno=&name=&address=&serno=',
                meta={'cookiejar':str(uuid4)},
                callback=self.get_colonies)

            def get_colonies(self,response):
                table=response.xpath('/html/body/table')
                with open('colony_data.csv','w') as f:
                    wr=csv.writer(f)
                    for tr in table.xpath('.//tr'):
                        _tdata=[]
                    
                        for td in tr.xpath('.//td'):
                            _text=''.join([a for a in td.xpath('.//text()').extract()])
                            _tdata.append(_text)
                        wr.writerow(_tdata)
    
    