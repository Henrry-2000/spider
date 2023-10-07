import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class PksSpider(CrawlSpider):
    name = "pks"
    # 设置爬取的域名和start_urls
    allowed_domains = ["packetstormsecurity.com"]
    start_urls = ["https://packetstormsecurity.com/files/tags/exploit/page1/"]
    rules = (Rule(LinkExtractor(allow=r"Items/"),callback="parse_item",follow=True),)

    def parse_item(self,response):
        item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return item

    rules = (Rule(LinkExtractor(allow=r'files/tags/exploit/page(.*?)'), callback='parse_vul_list', follow=True),)
    def parse_vul_list(self, response):
        vul_list = response.xpath('//a[@class="ico text-plain"]/@href').extract()
        for vul in vul_list:
           vul_url ='https://packetstormsecurity.com'+vul
           request = scrapy.Request(url=vul_url,callback=self.parse_vul_inf,dont_filter=True)
           yield request

    def parse_vul_inf(self,response) :
        item={}
        item['title']=response.xpath('//strong/text()').extract_first() if response.xpath('//strong/text()').extract_first() else ''
        authors=response.xpath('//a[@class="person"]/text()').extract() if response.xpath ('//a[@class="person"]/text()').extract() else ''
        item['author']=','.join(authors)
        date =response.xpath(".//pre/code").extract_first() if response.xpath (".//pre/code").extract_first() else ''
        pattern = re.compile(r'//Discover date : (.*?)/')
        item['date']=pattern.findall(date)
        item['des'] = response.xpath('//dd[@class="detail"]/p/text()').extract()
        item['vul_type']=''
        test = response.xpath(".//pre/code").extract_first()
        s_replace = test.replace('<br>',"\n")
        s_replace = s_replace.replace('<code>','')
        s_replace = s_replace.replace('</code>','')
        item['poc'] =s_replace
        yield item

