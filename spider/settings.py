# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'
COOKIES_ENABLES=False
ITEM_PIPELINES = {
    'spider.pipelines.SpiderPipeline': 300,
}

# ES configuration
ES_HOST = "localhost:9200"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=2

LOG_LEVEL = 'INFO'

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=10
TIME_DELTA =20 

SCHEDULER_IDLE_BEFORE_CLOSE = 10
# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=2
CONCURRENT_REQUESTS_PER_IP=2

