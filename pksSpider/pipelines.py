# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
def write_to_file(content):
    with open('D:\研究生\课程\网络内容信息安全\爬虫\pksSpider\pksSpider\爬虫.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=True))

class PksspiderPipeline:
    def process_item(self, item, spider):
        print(item)
        return item
