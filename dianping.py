#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.dom import pulldom
import requests
from lxml import etree
import codecs
from time import sleep

header = {
    "Host": "www.dianping.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    }

def getUrls():
    cityID = 1
    pageNum = 0
    for i in range(50):
        pageNum += 1
        url = "http://www.dianping.com/search/category/{}/10/p{}".format(cityID, pageNum)
        yield url

def getPage(url):
    return session.get(url)

def parse(page):
    tree = etree.HTML(page.text)
    print page.text
    restaurants = []
    for i in range(15):
        res = {}
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]//h4/text()".format(i+1))
        try:
            res['name'] = ele[0]
        except:
            res['name'] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]/div[2]/div[3]/span[@class='addr']//text()".format(i+1))
        try:
            res['address'] = ele[0]
        except:
            res['address'] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]//a[@class='mean-price']/b/text()".format(i+1))
        try:
            res["price"] = ele[0][1:]
        except:
            res["price"] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]/div[2]/span/span[1]/b/text()".format(i+1))
        try:
            res['taste'] = ele[0]
        except:
            res['taste'] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]/div[2]/span/span[2]/b/text()".format(i+1))
        try:
            res['env'] = ele[0]
        except:
            res['env'] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]/div[2]/span/span[3]/b/text()".format(i+1))
        try:
            res['service'] = ele[0]
        except:
            res['service'] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]/div[2]/div[3]/a[1]/span//text()".format(i+1))
        try:
            res['category'] = ele[0]
        except:
            res['category'] = "-1"
        ele = tree.xpath("//*[@id='shop-all-list']/ul/li[{}]//img/@data-src".format(i+1))
        try:
            res['pic']= ele[0]
        except:
            res['pic'] = "-1"
        restaurants.append(res)
    return restaurants


def xmlGenerartor(dic):
    restaurant = newdoc.createElement("restaurant")
    restaurant.setAttribute("name",dic["name"])
    restaurant.setAttribute("address",dic["address"])
    restaurant.setAttribute("price",dic["price"])
    restaurant.setAttribute("taste",dic["taste"])
    restaurant.setAttribute("env",dic["env"])
    restaurant.setAttribute("category",dic["category"])
    restaurant.setAttribute("service",dic["service"])
    restaurant.setAttribute("pic",dic["pic"])
    restaurants.appendChild(restaurant)


if __name__=="__main__":
    session = requests.session()
    session.headers.update(header)
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "shanghai", None)
    restaurants = newdoc.createElement("restaurants")
    newdoc.documentElement.appendChild(restaurants)
    counter = 0
    for url in getUrls():
        counter += 1
        print "Retrieving page {}".format(counter)
        page = getPage(url)
        rets = parse(page)
        for ret in rets:
            xmlGenerartor(ret)
        sleep(5)
    f= codecs.open("data.xml","w", "utf-8")
    f.write(newdoc.toprettyxml())
    f.close()
