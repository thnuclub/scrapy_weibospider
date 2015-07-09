from pkg_resources import load_entry_point

if __name__ == '__main__':
    argv = ["scrapy", "crawl", "weibo", "-a", "name=15557106533", "-a", "password=wenghaiqin"]
    load_entry_point('Scrapy==0.24.4', 'console_scripts', 'scrapy')(argv)

