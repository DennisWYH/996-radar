# -*- coding: utf-8 -*-

import scrapy
from scrapy import cmdline

class BlogSpider(scrapy.Spider):
    """ 
    	Provide Urls, so that the default start_requests() method
    	will be called upon this urls.
    """
    name = 'blogspider'
    start_urls = [
    'https://sou.zhaopin.com/?p=2&jl=489&sf=0&st=0&kw=python%20开发&kt=3',
    ]
    """
    	Parse method is the default callback method in scrapy
    	After parsing through each of the urls,
    	A response object will be returned,
    	Then you can take the element you want from the reponse object
    """
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        print('body of the response is...',response.body)
"""
	智联招聘网站分析：
		入口网页：
			python 开发 page 1 page 2
		    https://sou.zhaopin.com/?p=1&jl=489&sf=0&st=0&kw=python%20开发&kt=3
		    https://sou.zhaopin.com/?p=2&jl=489&sf=0&st=0&kw=python%20开发&kt=3
		每一页上面的职业信息元素
			<a href="https://jobs.zhaopin.com/413479081250103.htm">
			in element a, find href.
		点击下一页可以翻页，ajax更新页面，url不变
			<button class="btn soupager__btn">下一页</button>

		Problem: 
			scrapy shell 'https://sou.zhaopin.com/?jl=489&kw=python软件工程师&kt=3'
			return a response object.
			view(response) object. the job postitions session is not captured.

			scrapy shell 'https://jobs.zhaopin.com/413479081250103.htm'
			return a response object.
			view(response) object can give me the content I need. however I can't find next page from here.
		Action:
		    1. 继续读Scrapy的文档，看看有没有解决方案
		Solution:
			1. 问题定义：智联招聘使用ajax加载页面，需要使用Chrome development tool 来检测，
				在打开了开发者模式之后，刷新页面。可以在网络模块检测到ajax的请求。
			2. 找到这个请求，然后通过scrapy进行模拟。

		请求长这样：
			https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=489&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python+%E5%BC%80%E5%8F%91&kt=3&=0&at=40d70a1d8be042649b2d0eeda857481d&rt=a3ec336a52b7495fa377b7652c341982&_v=0.71722478&userCode=628987727&x-zp-page-request-id=7fb13fd6b13b42bb84236683878111e2-1554277091018-226942
			注意到page-request-id=7这个字段，如果修改ID的话，发现所得到的response不多。
			"positionURL":"https://jobs.zhaopin.com/CC552061080J00208094805.htm"
			"positionURL":"https://jobs.zhaopin.com/CC636483920J00126022112.htm"
			"positionURL":"https://jobs.zhaopin.com/CC603465980J00277521607.htm"
		页面是jason格式。上面的positionURL是职位的具体连接。一个页面有90个职位链接。

		接下里的任务就是：
			抓取page-request-id=1 - 100的页面, 就可以得到100*90 = 9000个职位链接。

"""

    # cmdline.execute('scrapy crawl')