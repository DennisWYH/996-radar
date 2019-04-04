# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
import json
import time

class JobSpider(scrapy.Spider):
	name ='babes'
	def start_request(self):
		urls=[]
		with open('positionUrl.txt','r') as f:
			read_data = f.read()
			read_data_list = read_data.split()
		for i in read_data_list:
			urls.append(i);
			print('urls added.....', i)
		for url in urls:
			time.sleep(5)
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		title = response.xpath('//*[@id="root"]/div[3]/div/div/h3').re('[>].*[<]').extract()
		title = title[1:-2]
		print(title)
