# scrapy_weibospider
scrapy weibo spider(基于scrapy-redis的分布式,由于抓取是带状态的，所以目前多机会有问题，目前猜测scrapy-redis不适合抓取需登录的网站)

## Usage

```
scrapy crawl weibospider -a name=username -a password=pwd

scrapy runspider weibospider_redis.py -a name=username -a password=pwd (client)

```

## SETUP

```
(ubuntu) apt-get install python2.7-dev libssl-dev libffi-dev libxml2-dev libxslt1-dev

pip install -r requirements.txt

```


## Mark

```
virtual memory exhausted: Cannot allocate memory

dd if=/dev/zero of=/swap bs=1024 count=1M
mkswap /swap
swapon /swap
echo “/swap  swap  swap  sw  0  0″ >> /etc/fstab
```
