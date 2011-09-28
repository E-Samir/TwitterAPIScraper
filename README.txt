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

Interactive Shell
-----------------

[source,bash]
scrapy shell https://dev.twitter.com/docs/api  
scrapy shell https://dev.twitter.com/docs/api/1/get/statuses/home_timeline
