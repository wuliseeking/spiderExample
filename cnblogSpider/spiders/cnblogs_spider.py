import  scrapy
from scrapy.crawler import CrawlerPrpcess,CrawlerRunner
from twisted.internet import reactor,defer
from scrapy.utils.log import configure_logging
from cnblogSpider.items import CnblogspiderItem
from scrapy.selector import Selector
class CnblogsSpider(scrapy.Spider):
    name="cnblogs"
    allowed_domains=["cnblogs.com"]
    start_urls=["http://www.cnblogs.com/qiyeboy/default.html?page=1"]
    def parse(self,response):
        papers=response.xpath('//*[@id="mainContent"]/div/div[@class="day"]')
        print('*'*15,len(papers),'-'*30)
        mm=0
        for paper in papers :
            mm =mm + 1
            print(mm)
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title=paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time=paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content=paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url,title=title,time=time,content=content)
            yield item
        next_page=Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0],callback=self.parse)

if __name__=='__main__':
    process=CrawlerProcess({
        'USER_AGENT':'Mozilla/4.0 (compatible;MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(CnblogsSpider)
    process.start()
'''
if __name__=='__main__':
    configure_logging({'LOG_FORMAT':'%(levelname)s:%(message)s'})
    runner=CrawlerRunner()
    d=runner.crawl(CnblogsSpider)
    d.addBoth(lambda _:reactor.stop())
    reactor.run()
'''
'''
class MySpider1(scrapy.Spider):
    #your first spider definition
    ...
class MySpider2(scrapy.Spider):
    #Your second spider definition
    ...
#在一个进程中启动多个爬虫
#第一种方法
process=CrawlerProcess()
process.crawl(MySpider1)
process.crawl(MySpider2)
process.start()

#第二种方法
configure_logging()
runner=CrawlerRunner()
runner.crawl(MySpider1)
runner.crawl(MySpider2)
d=runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()

#第三种方法
configure_logging()
runner=CrawlerRunner()
@defer.inlineCallbacks
def crawl()：
    yield runner.crawl(MySpider1)
    yield runner.crawl(MySpider2)
    reactor.stop()
crawl()
reactor.run()

'''
