#!/usr/bin/env python
# encoding:utf-8

import scrapy
from rwhois_registrant.items import RwhoisRegistrantItem
import re
import MySQLdb as mdb
import os
from tool import get_cookie, delete_cookie
import time
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class DmozSpider(scrapy.Spider):
    name = "rwhois_email"
    allowed_domains = ["benmi.com"]
    handle_httpstatus_list = [503]

    # start_urls = ["https://www.benmi.com/whoishistory/baidu.com.html"]

    def __init__(self):
        self.head = {
            "authority": "www.benmi.com",
            "method": "GET",
            "path": "/",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch",
            "accept-language": "en-US,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "__cfduid=df6bf2ef2f039c7b52004f1280b9b9ab31471399390; cf_clearance=ce09e2bfeed7280c3f62b6920f8fdd23b4e6ebcf-1471399395-900; ASP.NET_SessionId=lcfdeach44nhqgwfosnyb2fx; CNZZDATA4814012=cnzz_eid%3D218222633-1471395729-https%253A%252F%252Fwww.benmi.com%252F%26ntime%3D1471395729upgrade-insecure-requests:1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36"
        }

    def start_requests(self):
        registrant = self.get_registrant()
        if (registrant != None):
            cookie = get_cookie()
            # url = "https://www.benmi.com/whoishistory/" + domain + ".html"
            url = "https://www.benmi.com/rwhois?q=" + registrant + "&t=em"
            return [scrapy.Request(url, headers=self.head, meta={'registrant': registrant, 'cookie': cookie},
                                   cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2],
                                            "BenmiUserInfo2": "Benmi-UN=hahaha321",
                                            "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "})]

    def parse(self, response):
        request_state = self.if_too_many_request(response.body, 'parse')
        registrant = response.meta['registrant']
        if (request_state == False):
            all_page_num = self.get_page_num(response.body)
            num = 1
            while num <= all_page_num:
                url = "https://www.benmi.com/rwhois?p=" + \
                      str(num) + "&q=" + registrant + "&t=em"
                print url
                cookie = get_cookie()
                num = num + 1
                yield scrapy.Request(url, headers=self.head, meta={'cookie': cookie, 'registrant': registrant},
                                     cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2],
                                              "BenmiUserInfo2": "Benmi-UN=hahaha321",
                                              "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "},
                                     callback=self.get_first_page, dont_filter=True)
            self.finish_registrant(registrant)
            registrant = self.get_registrant()
            if (registrant != None):
                cookie = get_cookie()
                # url = "https://www.benmi.com/whoishistory/" + domain + ".html"
                url = "https://www.benmi.com/rwhois?q=" + registrant + "&t=em"
                yield scrapy.Request(url, headers=self.head, meta={'registrant': registrant, 'cookie': cookie},
                                     cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2],
                                              "BenmiUserInfo2": "Benmi-UN=hahaha321",
                                              "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "},
                                     callback=self.parse, dont_filter=True)
        else:
            url = response.request.url
            cookie = get_cookie()
            yield scrapy.Request(url, headers=self.head, meta={'registrant': registrant, 'cookie': cookie},
                                 cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2],
                                          "BenmiUserInfo2": "Benmi-UN=hahaha321",
                                          "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "},
                                 callback=self.parse, dont_filter=True)

    # def get_first_page(self, response):
    #     request_state = self.if_too_many_request(response.body, 'first_page')
    #     registrant = response.meta['registrant']
    #     if(request_state == False):
    #         content = u'//table[@class="sf-grid" and @id = "sf-grid"]/tr/td[@class = "lf"]/a/img[@alt="..."]/../@href'
    #         domain_url_list = response.xpath(content).extract()
    #         index = 0
    #         domain_url_list2 = []
    #         while(index < len(domain_url_list)):
    #             domain_url_list2.append(domain_url_list[index]) 
    #             index = index + 2
    #         for url in domain_url_list2:
    #             cookie = get_cookie()
    #             url = "https://www.benmi.com" + url
    #             item = RwhoisRegistrantItem()
    #             item['registrant'] = registrant 
    #             yield scrapy.Request(url, headers=self.head, meta={'cookie': cookie,'item':item}, cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2], "BenmiUserInfo2": "Benmi-UN=hahaha321", "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "}, callback=self.get_domain_name, dont_filter=True)
    #     else:
    #         url = response.request.url
    #         cookie = get_cookie()
    #         yield scrapy.Request(url, headers=self.head, meta={'cookie': cookie,'registrant':registrant}, cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2], "BenmiUserInfo2": "Benmi-UN=hahaha321", "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "}, callback=self.get_first_page, dont_filter=True)

    def get_first_page(self, response):
        request_state = self.if_too_many_request(response.body, 'first_page')
        registrant = response.meta['registrant']
        if (request_state == False):
            s = Selector(text=response.body)
            content = u'//table[@class="sf-grid" and @id = "sf-grid"]/tr/td[@class = "lf"]/a/img[@alt="..."]/../@href'
            domain_url_list = s.xpath(content).extract()
            content2 = u'//table[@class="sf-grid" and @id = "sf-grid"]/tr'
            s_list = s.xpath(content2)
            domain_url_list2 = []
            for s in s_list:
                url2 = s.xpath('td[@class = "lf"]/a/img[@alt="..."]/../@href').extract()[0]
                domain_url_list2.append(url2)
            for url in domain_url_list2:
                cookie = get_cookie()
                url = "https://www.benmi.com" + url
                item = RwhoisRegistrantItem()
                item['registrant'] = registrant
                yield scrapy.Request(url, headers=self.head, meta={'cookie': cookie, 'item': item},
                                     cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2],
                                              "BenmiUserInfo2": "Benmi-UN=hahaha321",
                                              "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "},
                                     callback=self.get_domain_name, dont_filter=True)

    def get_domain_name(self, response):
        request_state = self.if_too_many_request(response.body, 'name')
        item = response.meta['item']
        if (request_state == False):
            domain = response.xpath("//head/title/text()").extract()[0]
            domain = domain.encode('utf8')[:-105]
            item['domain'] = domain
            yield item
        else:
            url = response.request.url
            cookie = get_cookie()
            yield scrapy.Request(url, headers=self.head, meta={'cookie': cookie, 'item': item},
                                 cookies={"__cfduid": cookie[1], "cf_clearance": cookie[2],
                                          "BenmiUserInfo2": "Benmi-UN=hahaha321",
                                          "SITEINFO": "66b/UN0Nvf1MujwHhivXoluFewMFC48CdOZ9YpNXKEg=; "},
                                 callback=self.get_domain_name, dont_filter=True)

    def get_page_num(self, source):
        content = '<span class="Page">(.*)'
        pattern = re.compile(content)
        result = pattern.findall(source)
        content = '共(\d*?)页'
        pattern = re.compile(content)
        if (result != []):
            result = pattern.findall(result[0])
            if (int(result[0]) > 10):
                return 10
            return int(result[0])
        else:
            content = "暂无域名(.)*相关历史记录数据，或移步查看(.)*相关信息："
            pattern = re.compile(content)
            result = pattern.findall(source)
            if (result != []):
                return 0
            else:
                return 1

    def if_too_many_request(self, source, msg):
        content = '访问太频繁,请稍候再访问!'
        pattern = re.compile(content)
        result = pattern.findall(source)
        if (result != []):
            print msg + '   too many request'
            return True
        else:
            return False

    def get_registrant(self):
        try:
            con = mdb.connect('172.26.253.3',
                              'root',
                              'platform',
                              'malicious_domain_sys',
                              charset='utf8')
            cur = con.cursor()
            n = cur.execute(
                """SELECT * FROM malicious_domain_sys.info_reverse_search WHERE done != 1 AND info_type = 3 LIMIT 1 """)
            if n == 0:
                return None
            element = cur.fetchall()
            con.close()
        except Exception as e:
            domain = self.get_registrant()
            return domain
        domain = element[0][1]
        if domain is None:
            domain = ''
        return domain.replace('+', '%2B')

    def finish_registrant(self, registrant):
        con = mdb.connect('172.26.253.3',
                          'root',
                          'platform',
                          'malicious_domain_sys',
                          charset='utf8')
        cur = con.cursor()
        registrant = registrant.replace('%2B', '+')
        SQL = """UPDATE malicious_domain_sys.info_reverse_search SET done = 1 WHERE info = "{r}" """.format(
            r=registrant)
        cur.execute(SQL)
        con.commit()
        con.close()
