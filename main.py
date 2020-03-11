# Attempt 1: 从亚马逊搜索列表中抓取商品名称，价格，url，并存入csv
import lxml
from lxml import etree
import requests
import csv
import random
import time
from itertools import cycle

# Not Used
# def get_proxies():
#     url = 'https://free-proxy-list.net/'
#     response = requests.get(url)
#     parser = etree.HTML(response.text)
#     proxies = set()
#     for i in parser.xpath('//tbody/tr')[:100]:
#         if i.xpath('.//td[7][contains(text(),"yes")]'):
#             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#             proxies.add(proxy)
#     return proxies

# test_url = "https://www.amazon.com/Apple-Watch-GPS-44mm-Aluminum/dp/B07XR5T85R/ref=sr_1_5?keywords=apple&qid=1583891902&sr=8-5"

# Note Used
# user_agent_list = [
#    #Chrome
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
#     #Firefox
#     'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
#     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
#     'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
#     'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
#     'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
#     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
#     'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
#     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
#     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
#     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
#     'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
# ]

# Not used
# proxy_pool = cycle(get_proxies())

BASE_URL = "https://www.amazon.com/s?k="


def get_search_page(item_name, pg):
    target = BASE_URL + item_name + "&page=" + str(pg)
    print(target)
    for i in range(100):
        try:
            print("Request #%d" % i)
            time.sleep(random.randint(1, 3))
            # proxy = next(proxy_pool)
            response = requests.get(
                target, headers={
                    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "cache-control": "max-age=0",
                })
            if response.status_code != 200:
                # print("Error!")
                # Request is not successfully handled
                print('Request is not successfully handled')
                continue
            elif response.status_code == 200:
                # print(response.text)
                html = etree.HTML(response.text)
                item_titles = html.xpath(
                    ".//div[@class='a-section a-spacing-none']//a[@class='a-link-normal a-text-normal']/span")
                if (len(item_titles) == 0):
                    # Request is blocked by bot detection
                    print('Request is blocked by bot detection')
                    continue
                print("HTML is normal, proceeding to next stage")
                return response.text
            return None
        except:
            print("Exception,skipping")
            continue
    return None


def parse_and_select(res):
    html = etree.HTML(res)
    items_with_all_data = './/div[@class="sg-col-inner"]/div[2]//span[@class="a-price-whole"]/../../../../../../../../../..'
    title = items_with_all_data+'//span[@class="a-size-medium a-color-base a-text-normal"]/node()'
    print(title)
    item_titles = html.xpath(
        items_with_all_data+'//span[@class="a-size-medium a-color-base a-text-normal"]/node()')
    item_prices = html.xpath(
        items_with_all_data+'//span[@class="a-price"]/span[@class="a-offscreen"]/node()')
    item_url = html.xpath(
        items_with_all_data+"//a[@class='a-link-normal a-text-normal']/@href")
    print(len(item_titles))
    print(len(item_prices))
    print(len(item_url))
    data = []
    for i in range(len(item_titles)):
        item = [item_titles[i], item_prices[i], item_url[i]]
        data.append(item)
    return data


def to_csv(data,name):
    headers = ["Name", "Price", "Link"]
    csv_file = open("./data/ListSearch_"+name+".csv", "w")
    writer = csv.writer(csv_file)
    writer.writerow(headers)
    for i in data:
        writer.writerow(i)
    csv_file.close()
    return


def main(name, page):
    html = get_search_page(name, page)
    data = parse_and_select(html)
    # print(data)
    to_csv(data,name)
    print("finished!")


if __name__ == "__main__":
    main("gaming_laptop", 1)
