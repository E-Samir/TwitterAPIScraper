#!/usr/bin/env python
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import re
import json
from HTMLParser import HTMLParser
import os,sys


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)



class DmozSpider(BaseSpider):
   raw = {}  
   name = "dev.twitter.com"
   allowed_domains = ["dev.twitter.com"]
   start_urls = [
       "https://dev.twitter.com/docs/api/1/get/statuses/home_timeline",
       "https://dev.twitter.com/docs/api/1/get/statuses/mentions",
       "https://dev.twitter.com/docs/api/1/get/statuses/public_timeline",
       "https://dev.twitter.com/docs/api/1/get/statuses/retweeted_by_me",
       "https://dev.twitter.com/docs/api/1/get/statuses/retweeted_to_me",
       "https://dev.twitter.com/docs/api/1/get/statuses/retweets_of_me",
       "https://dev.twitter.com/docs/api/1/get/statuses/user_timeline",
       "https://dev.twitter.com/docs/api/1/get/statuses/retweeted_to_user",
       "https://dev.twitter.com/docs/get/statuses/retweeted_by_user",
       "https://dev.twitter.com/docs/api/1/get/statuses/%3Aid/retweeted_by",
       "https://dev.twitter.com/docs/api/1/get/statuses/%3Aid/retweeted_by/ids",
       "https://dev.twitter.com/docs/api/1/get/statuses/retweets/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/statuses/show/%3Aid",
       "https://dev.twitter.com/docs/api/1/post/statuses/destroy/%3Aid",
       "https://dev.twitter.com/docs/api/1/post/statuses/retweet/%3Aid",
       "https://dev.twitter.com/docs/api/1/post/statuses/update",
       "https://dev.twitter.com/docs/api/1/post/statuses/update_with_media",
       "https://dev.twitter.com/docs/api/1/get/search",
       "https://dev.twitter.com/docs/api/1/get/direct_messages",
       "https://dev.twitter.com/docs/api/1/get/direct_messages/sent",
       "https://dev.twitter.com/docs/api/1/post/direct_messages/destroy/%3Aid",
       "https://dev.twitter.com/docs/api/1/post/direct_messages/new",
       "https://dev.twitter.com/docs/api/1/get/direct_messages/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/followers/ids",
       "https://dev.twitter.com/docs/api/1/get/friends/ids",
       "https://dev.twitter.com/docs/api/1/get/friendships/exists",
       "https://dev.twitter.com/docs/api/1/get/friendships/incoming",
       "https://dev.twitter.com/docs/api/1/get/friendships/outgoing",
       "https://dev.twitter.com/docs/api/1/get/friendships/show",
       "https://dev.twitter.com/docs/api/1/post/friendships/create",
       "https://dev.twitter.com/docs/api/1/post/friendships/destroy",
       "https://dev.twitter.com/docs/api/1/get/friendships/lookup",
       "https://dev.twitter.com/docs/api/1/post/friendships/update",
       "https://dev.twitter.com/docs/api/get-friendshipsno_retweet_ids",
       "https://dev.twitter.com/docs/api/1/get/users/lookup",
       "https://dev.twitter.com/docs/api/1/get/users/profile_image/%3Ascreen_name",
       "https://dev.twitter.com/docs/api/1/get/users/search",
       "https://dev.twitter.com/docs/api/1/get/users/show",
       "https://dev.twitter.com/docs/api/1/get/users/contributees",
       "https://dev.twitter.com/docs/api/1/get/users/contributors",
       "https://dev.twitter.com/docs/api/1/get/users/suggestions",
       "https://dev.twitter.com/docs/api/1/get/users/suggestions/%3Aslug",
       "https://dev.twitter.com/docs/api/1/get/users/suggestions/%3Aslug/members",
       "https://dev.twitter.com/docs/api/1/get/favorites",
       "https://dev.twitter.com/docs/api/1/post/favorites/create/%3Aid",
       "https://dev.twitter.com/docs/api/1/post/favorites/destroy/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/lists/all",
       "https://dev.twitter.com/docs/api/1/get/lists/statuses",
       "https://dev.twitter.com/docs/api/1/post/lists/members/destroy",
       "https://dev.twitter.com/docs/api/1/get/lists/memberships",
       "https://dev.twitter.com/docs/api/1/get/lists/subscriptions",
       "https://dev.twitter.com/docs/api/1/post/lists/subscribers/create",
       "https://dev.twitter.com/docs/api/1/get/lists/subscribers/show",
       "https://dev.twitter.com/docs/api/1/post/lists/subscribers/destroy",
       "https://dev.twitter.com/docs/api/1/post/lists/members/create_all",
       "https://dev.twitter.com/docs/api/1/get/lists/members/show",
       "https://dev.twitter.com/docs/api/1/get/lists/members",
       "https://dev.twitter.com/docs/api/1/post/lists/members/create",
       "https://dev.twitter.com/docs/api/1/post/lists/destroy",
       "https://dev.twitter.com/docs/api/1/post/lists/update",
       "https://dev.twitter.com/docs/api/1/post/lists/create",
       "https://dev.twitter.com/docs/api/1/get/lists",
       "https://dev.twitter.com/docs/api/1/get/lists/show",
       #"https://dev.twitter.com/docs/api/1/get/account/rate_limit_status",
       "https://dev.twitter.com/docs/api/1/get/account/verify_credentials",
       #"https://dev.twitter.com/docs/api/1/post/account/end_session",
       "https://dev.twitter.com/docs/api/1/post/account/update_delivery_device",
       "https://dev.twitter.com/docs/api/1/post/account/update_profile",
       "https://dev.twitter.com/docs/api/1/post/account/update_profile_background_image",
       "https://dev.twitter.com/docs/api/1/post/account/update_profile_colors",
       "https://dev.twitter.com/docs/api/1/post/account/update_profile_image",
       #"https://dev.twitter.com/docs/api/1/get/account/totals",
       #"https://dev.twitter.com/docs/api/1/get/account/settings",
       "https://dev.twitter.com/docs/api/1/post/account/settings",
       "https://dev.twitter.com/docs/api/1/post/notifications/follow",
       "https://dev.twitter.com/docs/api/1/post/notifications/leave",
       #"https://dev.twitter.com/docs/api/1/get/saved_searches",
       "https://dev.twitter.com/docs/api/1/get/saved_searches/show/%3Aid",
       "https://dev.twitter.com/docs/api/1/post/saved_searches/create",
       "https://dev.twitter.com/docs/api/1/post/saved_searches/destroy/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/trends/%3Awoeid",
       "https://dev.twitter.com/docs/api/1/get/trends/available",
       "https://dev.twitter.com/docs/api/1/get/geo/id/%3Aplace_id",
       #"https://dev.twitter.com/docs/api/1/get/geo/nearby_places",
       "https://dev.twitter.com/docs/api/1/get/geo/reverse_geocode",
       "https://dev.twitter.com/docs/api/1/get/geo/search",
       "https://dev.twitter.com/docs/api/1/get/geo/similar_places",
       "https://dev.twitter.com/docs/api/1/post/geo/place",
       #"https://dev.twitter.com/docs/api/1/get/trends",
       "https://dev.twitter.com/docs/api/1/get/trends/current",
       "https://dev.twitter.com/docs/api/1/get/trends/daily",
       "https://dev.twitter.com/docs/api/1/get/trends/weekly",
       "https://dev.twitter.com/docs/api/1/get/blocks/blocking",
       "https://dev.twitter.com/docs/api/1/get/blocks/blocking/ids",
       "https://dev.twitter.com/docs/api/1/get/blocks/exists",
       "https://dev.twitter.com/docs/api/1/post/blocks/create",
       "https://dev.twitter.com/docs/api/1/post/blocks/destroy",
       "https://dev.twitter.com/docs/api/1/post/report_spam",
       "https://dev.twitter.com/docs/api/1/get/oauth/authenticate",
       "https://dev.twitter.com/docs/api/1/get/oauth/authorize",
       "https://dev.twitter.com/docs/api/1/post/oauth/access_token",
       "https://dev.twitter.com/docs/api/1/post/oauth/request_token",
       #"https://dev.twitter.com/docs/api/1/get/help/test",
       "https://dev.twitter.com/docs/api/1/delete/%3Auser/%3Alist_id/members",
       "https://dev.twitter.com/docs/api/1/delete/%3Auser/%3Alist_id/subscribers",
       "https://dev.twitter.com/docs/api/1/delete/%3Auser/lists/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/%3Alist_id/members",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/%3Alist_id/members/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/%3Alist_id/subscribers",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/%3Alist_id/subscribers/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/lists",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/lists/%3Aid",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/lists/%3Aid/statuses",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/lists/memberships",
       "https://dev.twitter.com/docs/api/1/get/%3Auser/lists/subscriptions",
       "https://dev.twitter.com/docs/api/1/get/statuses/followers",
       "https://dev.twitter.com/docs/api/1/get/statuses/friends",
       "https://dev.twitter.com/docs/api/1/get/statuses/friends_timeline",
       "https://dev.twitter.com/docs/api/1/post/%3Auser/%3Alist_id/create_all",
       "https://dev.twitter.com/docs/api/1/post/%3Auser/%3Alist_id/members",
       "https://dev.twitter.com/docs/api/1/post/%3Auser/%3Alist_id/subscribers",
       "https://dev.twitter.com/docs/api/1/post/%3Auser/lists",
       "https://dev.twitter.com/docs/api/1/post/%3Auser/lists/%3Aid",
       "https://dev.twitter.com/docs/api/post-accountupdate_location"
   ]

   def strip_tags(self,html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

   def __init__(self):
       print "initializing"
       f = open('currentapi.json')
       data = f.read()
       self.raw = json.loads(data)

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
       value = value.replace(":user", "USER").replace(":list_id","LIST_ID").replace(":id", "ID").replace("format","FORMAT")
       return value

   def fixName(self, value):
       value = value.replace(":user", "user").replace(":list_id","list_id").replace(":id", "id")
       return value


   def process_resource(self, raw):
       key=""
       data = {} 
       for item in raw:
           i = self.strip_tags(item)
           if(key == "auth"):
               data["auth"] = i
               key=""
               continue
           if(key == "formats"):
               data["formats"] = i
               key=""
               continue
           if(key == "http"):
               data["http"] = i
               key=""
               continue
           if(key == "rate"):
               data["rate"] = i
               key=""
               continue
           if(i.lower().find("authentication") != -1):
               key="auth"
           if(i.lower().find("formats") != -1):
               key="formats"
           if(i.lower().find("http methods") != -1):
               key="http"
           if(i.lower().find("rate") != -1):
               key="rate"

       if(data.has_key("formats")):
           v= data["formats"]
           if(v == ""):
               data["formats"] = []
           else:
               v= v.lower().replace("json","json,").replace("xml","xml,").replace("rss","rss,").replace("atom","atom,")
               if(v[len(v)-1] == ','):
                   v= v[:len(v)-1]
               ar= v.split(",")
               data["formats"] = ar

       return data


   def parse(self, response):
       hxs = HtmlXPathSelector(response)

       parent_names = hxs.select("//div[@class='breadcrumb']/a/text()").extract()
       resource_info = hxs.select("//div[@class='block api-doc-block']/table/tbody/tr/td").extract()
       data = self.process_resource(resource_info)

       parent = parent_names[len(parent_names)-1]
       parent = self.html_cleanup(parent)

       method_names = hxs.select("//h1[@id='title']/text()").extract()
       base_urls = hxs.select("//div[@class='odd']/text()").re("http.*")
       
       parameters = hxs.select("//div[@class='parameter']/span/text()").extract()
       required_list = hxs.select("//div[@class='parameter']/span[@class='param']/span/text()").extract() 
       descriptions = hxs.select("//div[@class='parameter']/p/text()").extract()
       #param_descriptions = hxs.select("//div[@class='parameter']/p/text()").extract()

       self.sanitize(parameters)
       #self.sanitize(param_descriptions)
       res = self.processRequired(required_list)
       updated_required_list = []
       if(len(res) > 0):
           for i in res:
               updated_required_list.append(parameters[i]) 

       obj = {} 
       names = method_names[0].split(' ')
       obj["name"] = self.fixName(names[1].replace("/", "_"));
       if(names[0] == "POST"):
           obj["require_post"] = True
       else:
           obj["require_post"] = False

       obj["description"] = descriptions[0].strip()
       obj["parameters"] = parameters
       obj["base_url"] = self.fixURL(base_urls[0].strip())
       obj["required"] = updated_required_list
       obj["doc_url"] = response.url
       obj["formats"] = data["formats"]
       obj["require_auth"] = data["auth"]
       obj["rate_limited"] = data["rate"]
       
       #print "parent: %s" %(parent)
       #print json.dumps(obj, sort_keys=True, indent=4)
       data = self.raw["TwitterAPI"]["API"]
       container = self.findParent(data, parent)
       container["methods"].append(obj)

       self.flush()


       
   def close_spider(self, spider):
      self.flush();

