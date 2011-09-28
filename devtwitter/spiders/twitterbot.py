#!/usr/bin/env python
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import re
import json

class DmozSpider(BaseSpider):
   currentUrl = ""
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
       #"https://dev.twitter.com/docs/api"
   ]

   #def make_requests_from_url(self,url):
   #    self.currentUrl = url
   #    return BaseSpider.make_requests_from_url(url)

   def __init__(self):
       print "initializing"
       f = open('/tmp/currentapi.json')
       data = f.read()
       self.raw = json.loads(data)

       #self.raw = {} 
       #self.raw["TwitterAPI"] = {} 
       #self.raw["TwitterAPI"]["API"] = [] 

   def flush(self):
       f = open('final.json','w')
       f.write(json.dumps(self.raw, sort_keys=True, indent=4))
       f.close()
       print "goodbye cruel world"

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
       for item in alist:
           if item.strip() == "required":
               required_list.append(alist.index(item))

       return required_list

   def findParent(self, data, parent_name):
       for item in data:
           if item["name"] == parent_name:
               return item
       return None
       #print "searching for: %s"%(parent_name)


   def parse(self, response):
       print "processing : %s" %(self.currentUrl)
       hxs = HtmlXPathSelector(response)

       parent_names = hxs.select("//div[@class='breadcrumb']/a/text()").extract()
       parent = parent_names[len(parent_names)-1]
       method_names = hxs.select("//h1[@id='title']/text()").extract()
       base_urls = hxs.select("//div[@class='odd']/text()").re("http.*")
       parameters = hxs.select("//div[@class='parameter']/span/text()").extract()
       required_list = hxs.select("//div[@class='parameter']/span[@class='param']/span/text()").extract() 
       descriptions = hxs.select("//div[@class='parameter']/p/text()").extract()

       self.sanitize(parameters)
       res = self.processRequired(required_list)
       updated_required_list = []
       if(len(res) > 0):
           for i in res:
               updated_required_list.append(parameters[i]) 

       obj = {} 
       names = method_names[0].split(' ')
       obj["name"] = names[1].replace("/", "_");
       if(names[0] == "POST"):
           obj["require_post"] = True
       else:
           obj["require_post"] = False

       obj["description"] = descriptions[0].strip()
       obj["parameters"] = parameters
       obj["base_url"] = base_urls[0].strip()
       obj["required"] = updated_required_list
       print "parent: %s" %(parent)
       #print json.dumps(obj, sort_keys=True, indent=4)
       data = self.raw["TwitterAPI"]["API"]
       container = self.findParent(data, parent)
       container["methods"].append(obj)
       print "# of objects inside methods is: %s" %(str(len(container["methods"])))

       self.flush();

       

   #def oldparse(self, response):
   #    hxs = HtmlXPathSelector(response)

   #    sites = hxs.select("//td[@class='views-field views-field-title']/a").re("href=\".*?\"")
   #    descriptions = hxs.select("//caption/p/text()").extract()
   #    self.sanitize(descriptions)
   #    api_names = hxs.select("//caption/strong/text()").extract()
   #    for i in range(0,len(descriptions)):
   #        obj = {}
   #        obj["name"]  = api_names[i]
   #        obj["methods"] = []
   #        obj["description"] =  descriptions[i]

   #        self.raw["TwitterAPI"]["API"].append(obj)
   #        #print obj
   #    f = open('currentapi.json','w')
   #    f.write(json.dumps(self.raw, sort_keys=True, indent=4))
   #    f.close()

   #    print "write new list of URLS to parse to urls.txt"
   #    print "length of sites is: %s"%(str(len(sites)))
   #    f = open('urls.txt','w')
   #    for site in sites:
   #        ndx = sites.index(site)
   #        match = re.search("\".*\"", site)
   #        if match == None:
   #            sites.remove(site)
   #        site = re.search("\".*\"", site).group().replace("\"","")
   #        site = "https://dev.twitter.com%s"%(site)
   #        #sites[ndx] = site
   #        f.write(site + "\r\n")

   #    f.close()


