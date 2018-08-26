# -*- coding: utf-8 -*-

# Scrapy settings for qidian project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qidian'

SPIDER_MODULES = ['qidian.spiders']
NEWSPIDER_MODULE = 'qidian.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'qidian.middlewares.QidianSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'qidian.middlewares.RandomIPMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'qidian.pipelines.QidianPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

PROXIES =[
{"ip_port": "183.48.89.42 : 8118"},
{"ip_port": "117.86.167.2 : 18118"},
{"ip_port": "125.118.145.161 : 6666"},
{"ip_port": "1.198.192.182 : 8010"},
{"ip_port": "221.10.159.234 : 1337"},
{"ip_port": "27.40.146.251 : 61234"},
{"ip_port": "123.180.69.17 : 8010"},
{"ip_port": "180.125.6.174 : 25733"},
{"ip_port": "114.104.173.17 : 26521"},
{"ip_port": "115.213.203.194 : 3128"},
{"ip_port": "110.73.42.122 : 8123"},
{"ip_port": "114.223.161.97 : 8118"},
{"ip_port": "115.223.89.109 : 8010"},
{"ip_port": "125.121.115.215 : 808"},
{"ip_port": "125.122.171.210 : 808"},
{"ip_port": "180.118.243.84 : 808"},
{"ip_port": "114.225.169.215 : 53128"},
{"ip_port": "106.56.102.192 : 8070"},
{"ip_port": "111.155.116.238 : 8123"},
{"ip_port": "117.86.207.149 : 18118"},
{"ip_port": "1.197.58.226 : 61234"},
{"ip_port": "171.39.2.221 : 8123"},
{"ip_port": "122.246.49.73 : 8010"},
{"ip_port": "115.219.107.197 : 8010"},
{"ip_port": "220.191.100.82 : 6666"},
{"ip_port": "121.31.159.129 :8123"},
{"ip_port": "121.31.176.165 : 8123"},
{"ip_port": "121.31.100.80 : 8123"},
{"ip_port": "42.248.200.234 : 23513"},
{"ip_port": "49.89.75.235 : 53128"},
{"ip_port": "115.46.75.1 : 8123"},
{"ip_port": "111.226.188.18 : 808"},
{"ip_port": "61.178.238.122 : 63000"},
{"ip_port": "117.86.166.6 : 8118"},
{"ip_port": "223.241.117.84 : 8010"},
{"ip_port": "180.118.241.201 : 61234"},
{"ip_port": "125.118.146.235 : 6666"},
{"ip_port": "60.3.89.20 : 80"},
{"ip_port": "180.121.135.151 : 808"},
{"ip_port": "180.118.243.164 : 808"},
{"ip_port": "110.73.4.138 : 8123"},
{"ip_port": "110.73.42.79 : 8123"},
{"ip_port": "114.231.71.224 : 18118"},
{"ip_port": "125.121.115.140 : 808"},
{"ip_port": "121.31.192.12 : 8123"},
{"ip_port": "110.73.42.11 : 8123"},
{"ip_port": "114.99.28.49 : 48433"},
{"ip_port": "182.45.178.113 : 6666"},
{"ip_port": "171.11.79.120 : 30581"},
{"ip_port": "106.8.17.10 : 60443"},
{"ip_port": "117.86.16.18 : 18118"},
{"ip_port": "121.225.26.59 : 3128"},
{"ip_port": "111.155.116.200 : 8123"},
{"ip_port": "180.118.242.201 : 808"},
{"ip_port": "125.118.151.238 : 6666"},
{"ip_port": "117.86.22.213 : 18118"},
{"ip_port": "125.118.240.242 : 6666"},
{"ip_port": "119.5.1.26 : 808"},
{"ip_port": "183.164.239.157 : 47284"},
{"ip_port": "183.158.20.113 : 808"},
{"ip_port": "180.121.130.167 : 18118"},
{"ip_port": "111.155.116.249 : 8123"},
{"ip_port": "114.237.59.6 : 40081"},
{"ip_port": "117.86.9.40 : 18118"},
{"ip_port": "171.38.34.235 : 8123"},
{"ip_port": "106.56.102.228 : 8070"},
{"ip_port": "218.72.75.80 : 37701"},
{"ip_port": "171.12.85.102 : 26568"},
{"ip_port": "117.31.149.116 : 28968"},
{"ip_port": "115.226.145.78 : 29692"},
{"ip_port": "121.225.24.82 : 3128"},
{"ip_port": "183.128.242.161 : 6666"},
{"ip_port": "111.155.116.232 : 8123"},
{"ip_port": "115.208.67.121 : 61234"},
{"ip_port": "110.73.7.147 : 8123"},
{"ip_port": "113.121.240.131 : 808"},
{"ip_port": "222.85.22.85 : 8010"},
{"ip_port": "144.255.163.218 : 808"},
{"ip_port": "110.72.37.143 : 8123"},
{"ip_port": "221.227.250.85 : 18118"},
{"ip_port": "117.86.16.105 : 18118"},
{"ip_port": "110.73.4.130 : 8123"},
{"ip_port": "114.139.101.237 :6666"},
{"ip_port": "114.232.170.224 : 24718"},
{"ip_port": "117.64.234.125 : 18118"},
{"ip_port": "220.191.102.94 : 6666"},
{"ip_port": "106.56.102.250 : 8070"},
{"ip_port": "180.118.243.131 : 61234"},
{"ip_port": "180.122.147.131 : 31495"},
{"ip_port": "125.120.86.70 : 8118"},
{"ip_port": "118.122.92.252 : 37901"},
{"ip_port": "110.73.1.4 : 8123"},
{"ip_port": "223.241.117.107 :8010"},
{"ip_port": "117.85.86.86 : 53128"},
{"ip_port": "220.184.213.173 : 6666"},
{"ip_port": "117.69.66.210 : 6668"},
{"ip_port": "114.104.97.133 : 6668"},
{"ip_port": "222.211.235.20 : 6675"},
{"ip_port": "114.231.69.23 : 18118"},
        ]