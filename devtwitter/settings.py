# Scrapy settings for devtwitter project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'devtwitter'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['devtwitter.spiders']
NEWSPIDER_MODULE = 'devtwitter.spiders'
DEFAULT_ITEM_CLASS = 'devtwitter.items.DevtwitterItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

