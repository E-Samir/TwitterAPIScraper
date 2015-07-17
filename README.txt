# DEPRECATED.

This project was used to scrape dev.twiter.com for API definition.  The page changed singificantly and this project is highly unlikely to work.  The code is left it for legacy purposes.



TwitterAPIScraper
================

Generate Documentation
----------------------

[source,bash]
asciidoc README.txt


Dependencies
------------

 * http://scrapy.org/

Run
---
[source,bash]
scrapy crawl dev.twitter.com 
or
scrapy runspider devtwitter/spiders/twitterbot.py 

Interactive Shell
-----------------

[source,bash]
scrapy shell https://dev.twitter.com/docs/api  
scrapy shell https://dev.twitter.com/docs/api/1/get/statuses/home_timeline
echo "booh"




