#!/usr/bin/env python
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import re
import json
from HTMLParser import HTMLParser
import os,sys



class DmozSpider(BaseSpider):
   raw = {}  
   name = "dev.twitter.com"
   allowed_domains = ["dev.twitter.com"]
   start_urls =[ 
       "https://dev.twitter.com/docs/api"
       ]


   def __init__(self):
       print "initializing"

       self.raw = {} 
       self.raw["TwitterAPI"] = {} 
       self.raw["TwitterAPI"]["API"] = [] 

   def flush(self):
       f = open('final.json','w')
       f.write(json.dumps(self.raw, sort_keys=True, indent=4))
       f.close()

   def sanitize(self, desc):
       
       for w  in desc:
           ndx = desc.index(w)
           desc[ndx] = w.strip()
           obj = re.search("\w", desc[ndx])
           if obj == None:
               desc.remove(w.strip())
               continue

   def processRequired(self, alist):
       required_list = [] 
       ndx = 0
       for item in alist:
           if item.strip() == "required":
               required_list.append(ndx)
           ndx = ndx + 1

       return required_list

   def findParent(self, data, parent_name):
       for item in data:
           if item["name"] == parent_name:
               return item
       return None
       #print "searching for: %s"%(parent_name)
   def html_cleanup(self,value):
       value = HTMLParser.unescape.__func__(HTMLParser, value.lower())
       value = value.replace("&", "and").replace(" ", "_")
       return value


   def fixURL(self, value):
       value = value.replace(":user", "USER").replace(":list_id","LIST_ID").replace(":id", "ID").replace("format","json")
       return value

   def fixName(self, value):
       value = value.replace(":user", "user").replace(":list_id","list_id").replace(":id", "id")
       return value


   def parse(self, response):
       hxs = HtmlXPathSelector(response)

       sites = hxs.select("//td[@class='views-field views-field-title']/a").re("href=\".*?\"")
       descriptions = hxs.select("//caption/p/text()").extract()
       self.sanitize(descriptions)
       api_names = hxs.select("//caption/strong/text()").extract()

       for i in range(0,len(descriptions)):
           obj = {}
           obj["name"] =  self.html_cleanup(api_names[i])
           obj["methods"] = []
           obj["description"] = HTMLParser.unescape.__func__(HTMLParser, descriptions[i].lower()) 

           self.raw["TwitterAPI"]["API"].insert(i, obj)


       f = open('currentapi.json','w')
       f.write(json.dumps(self.raw, sort_keys=True, indent=4))
       f.close()

       print "write new list of URLS to parse to urls.txt"
       print "length of sites is: %s"%(str(len(sites)))
       f = open('urls.txt','w')
       for site in sites:
           ndx = sites.index(site)
           match = re.search("\".*\"", site)
           if match == None:
               sites.remove(site)
           site = re.search("\".*\"", site).group().replace("\"","")
           site = "https://dev.twitter.com%s"%(site)
           #sites[ndx] = site
           f.write(site + "\r\n")

       f.close()


