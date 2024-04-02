import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin
from boss_zhipin.items import BossZhipinItem

class ZhipinSpider(scrapy.Spider):
    name = "zhipin"
    allowed_domains = ["zhipin.com"]
    start_urls = ["https://www.zhipin.com/web/geek/job?city=100010000&position=100514,100407&page=2"]

    #base url
    base_url = "https://www.zhipin.com"

    #分页爬取
    page = 2

    #实例化一个浏览器对象
    def __init__(self):
        service = Service(executable_path='/usr/local/bin/chromedriver')
        self.bro = webdriver.Chrome(service=service)


    def parse(self, response):
        print(response)
        #li_list = response.xpath('//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li | //*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li')
        li_list = response.xpath('//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li')
        for li in li_list:
            job_company = li.xpath('./div[1]/div/div[2]//a/text()').extract_first()
            #直接跳转详情页
            job_detials = li.xpath('.//a/@href').extract_first()
            #new_urls = 'https://www.zhipin.com' + job_detials
            new_url = urljoin(self.base_url, job_detials)
            item = BossZhipinItem()
            item['company'] = job_company

            if new_url:
                yield scrapy.Request(url=new_url, callback=self.parse_detials,meta={'item':item})

        # 实现分页
        current_page = response.url.split("page=")[-1]
        next_page = int(current_page) + 1
        if next_page <= 4:  # 限制爬取的页数为10页，根据需求调整
            next_page_url = f"https://www.zhipin.com/web/geek/job?city=100010000&position=100514,100407&page={next_page}"
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    #详情页数据爬取
    def parse_detials(self,response):
        item = response.meta['item']
        job_name = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[2]/h1/text()').extract_first()
        job_location = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/a/text()').extract_first()
        job_salary = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/div[2]/span/text()').extract_first()
        job_edu = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/span[2]/text()').extract_first()
        job_experience = response.xpath('//*[@id="main"]/div[1]/div/div/div[1]/p/span[1]/text()').extract_first()
        job_skills = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[1]/ul/li/text()').extract()
        job_skills = ' '.join(job_skills)
        job_demand = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[1]/div[2]/text()').extract()
        job_demand = ''.join(job_demand)
        item['name'] = job_name
        item['location'] = job_location
        item['salary'] = job_salary
        item['edu'] = job_edu
        item['experience'] = job_experience
        item['skills'] = job_skills
        item['demand'] = job_demand
        yield item

    def closed(self, spider):
        self.bro.quit()



