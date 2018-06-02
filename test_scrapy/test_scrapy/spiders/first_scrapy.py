import os
import scrapy
import requests
import urllib
import threading
import gevent
from scrapy.selector import HtmlXPathSelector
class FirstScrapySpiders(scrapy.Spider):
    name = 'first'
    allowed_domains=['http://www.521609.com/']
    start_urls=[
            'http://www.521609.com/meinvxiaohua/',
        ]

    def parse(self, response):
        # print(response.text)
        url = response.url
        print(url)

        body = response.body
        # print(body)
        unicode_body = response.body_as_unicode()
        # print(unicode_body)

        response_xpath = HtmlXPathSelector(response)
        items = response_xpath.select('//div[@class="index_img list_center"]//li/a/img').extract()
        names = response_xpath.select('//div[@class="index_img list_center"]//li/a/img/@alt').extract()
        images_url = response_xpath.select('//div[@class="index_img list_center"]//li/a/img/@src').extract()
        # items = response_xpath.select("//div[@class='body']/div[@class='up']/div[@class='yaowen']")

        # items = response.xpath('/html/body/div[3]/div[2]/div[7]/div[1]').extract()
        gevent_list =[]
        for item in range(len(items)):
            def scrapy_job(item):
                image_url  = FirstScrapySpiders.allowed_domains[0]+images_url[item]
                images_positon = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images/')
                filename = images_positon+names[item]+'.jpg'
                response_image = requests.get(image_url)
                with open(filename,'wb') as image:
                    image.write(response_image.content)
            gevent_list.append(gevent.spawn(scrapy_job,item))
        print(gevent_list)
        gevent.joinall(gevent_list)

class SecondScrapySpiders(scrapy.Spider):
    name = 'second'
    allowed_domains=['http://www.521609.com/']
    start_urls=[
            'http://www.521609.com/meinvxiaohua/',
        ]

    def parse(self, response):
        # print(response.text)
        url = response.url
        print(url)

        body = response.body
        # print(body)
        unicode_body = response.body_as_unicode()
        # print(unicode_body)

        response_xpath = HtmlXPathSelector(response)
        items = response_xpath.select('//div[@class="index_img list_center"]//li/a/img').extract()
        names = response_xpath.select('//div[@class="index_img list_center"]//li/a/img/@alt').extract()
        images_url = response_xpath.select('//div[@class="index_img list_center"]//li/a/img/@src').extract()
        # items = response_xpath.select("//div[@class='body']/div[@class='up']/div[@class='yaowen']")

        # items = response.xpath('/html/body/div[3]/div[2]/div[7]/div[1]').extract()

        for item in range(len(items)):
            def scrapy_job(item):
                image_url  = FirstScrapySpiders.allowed_domains[0]+images_url[item]
                images_positon = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images/')
                filename = images_positon+names[item]+'.jpg'
                response_image = requests.get(image_url)
                with open(filename,'wb') as image:
                    image.write(response_image.content)
            thr = threading.Thread(target=scrapy_job,args=(item,))
            thr.start()
