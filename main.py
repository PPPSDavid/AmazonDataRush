# Attempt 1: 从亚马逊搜索列表中抓取商品名称，价格，url，并存入csv
from lxml import etree
import requests
import csv
import random
import time

# from itertools import cycle

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

# test_url = "https://www.amazon.com/Apple-Watch-GPS-44mm-Aluminum/dp/B07XR5T85R/ref=sr_1_5?keywords=apple&qid
# =1583891902&sr=8-5"

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

# 以上全部为对于亚马逊反机器人指令的对应，因并未被过多侦测故未实际采用

# 数据来源：亚马逊美国版
BASE_URL = "https://www.amazon.com/s?k="

# 浏览器头部数据：根据真实浏览器模仿得来
HEADER = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                  'Safari/537.36',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
}


# 给定一个物品名称（String）与搜索页面数（int），返回一个text格式的html回复
def get_search_page(item_name, pg):
    target = BASE_URL + item_name + "&page=" + str(pg)
    print(target)
    for i in range(100):
        try:
            print("Request #%d" % i)
            time.sleep(random.randint(1, 3))
            # proxy = next(proxy_pool)
            response = requests.get(
                target, headers=HEADER)
            if response.status_code != 200:
                # print("Error!")
                # Request is not successfully handled
                print('Request is not successfully handled')
                continue
            elif response.status_code == 200:
                # print(response.text)
                html = etree.HTML(response.text)
                items_with_all_data = './/div[@class="sg-col-inner"]/div[2]//span[' \
                                      '@class="a-price-whole"]/../../../../../../../../../../div[@class="sg-row"][' \
                                      '1]//span[@aria-label][1]/../../../../../../../../.. '
                item_titles = html.xpath(
                    items_with_all_data + '//span[@class="a-size-medium a-color-base a-text-normal"]/node()')
                no_result = html.xpath(
                    '//span[contains(string(),"No results")]'
                )
                if len(item_titles) == 0:
                    # Request is blocked by bot detection
                    print('Request is blocked by bot detection')
                    continue
                elif len(no_result) > 0:
                    print("Invalid search page, returning")
                    return None
                else:
                    print("HTML is normal, proceeding to next stage")
                    return response.text
            return None
        except:
            print("Exception,skipping")
            continue
    return None


# 给定一个string格式的html，通过Xpath提取搜索中需要的特征
def parse_and_select(res):
    html = etree.HTML(res)
    items_with_all_data = './/div[@class="sg-col-inner"]/div[2]//span[' \
                          '@class="a-price-whole"]/../../../../../../../../../../div[@class="sg-row"][1]//span[' \
                          '@aria-label][1]/../../../../../../../../.. '
    item_titles = html.xpath(
        items_with_all_data + '//span[@class="a-size-medium a-color-base a-text-normal"]/node()')
    item_prices = html.xpath(
        items_with_all_data + '//span[@class="a-price"]/span[@class="a-offscreen"]/node()')
    item_url = html.xpath(
        items_with_all_data + "//a[@class='a-link-normal a-text-normal']/@href")
    item_review = html.xpath(
        items_with_all_data + '//div[@class="sg-row"][1]//span[@aria-label!="Amazon\'s Choice"][1]/@aria-label'
    )
    item_review_count = html.xpath(
        items_with_all_data + '//div[@class="sg-row"][1]//span[@aria-label][2]/@aria-label'
    )
    # print(len(item_titles))
    # print(len(item_prices))
    # print(len(item_url))
    # print(len(item_review))
    # print(len(item_review_count))
    url_processed = []
    for i in item_url:
        url_processed.append("https://www.amazon.com" + i)

    review_processed = []
    for i in item_review:
        try:
            number = i[0:3]
            review_processed.append(float(number))
        except ValueError:
            continue

    review_count_processed = []
    for i in item_review_count:
        review_count_processed.append(int(i.replace(',', '')))

    data = []
    for i in range(len(item_titles)):
        item = [item_titles[i], item_prices[i], url_processed[i], review_processed[i], review_count_processed[i]]
        data.append(item)
    return data


# Attempt two: loop through item pages for specific information.
# 给定一个特定商品的url，返回一个text格式的服务器返回html
def get_item_page(url):
    for i in range(100):
        try:
            print("Request #%d" % i)
            time.sleep(random.randint(1, 3))
            response = requests.get(
                url, headers=HEADER)
            if response.status_code != 200:
                # print("Error!")
                # Request is not successfully handled
                print('Request is not successfully handled')
                continue
            elif response.status_code == 200:
                # print(response.text)
                html = etree.HTML(response.text)
                item_titles = html.xpath(
                    '// div[ @ id = "centerCol"]'
                )
                if len(item_titles) == 0:
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


# 与上一函数相似，通过Xpath选择商品页面上的重要信息。
def parse_and_select_item(res):
    html = etree.HTML(res)
    item_seller = html.xpath(
        '//div[@id = "centerCol"]/div[@id="bylineInfo_feature_div"]//a/node()'
    )
    item_specs = html.xpath(
        '//div[@id="twister_feature_div"]//ul/li/@title'
    )
    item_description = html.xpath(
        '//div[@id = "centerCol"]//div[@id="featurebullets_feature_div"]//ul/li[position()>1]/span/node()'
    )
    # Should be non-zero for prime supported shipping
    item_shipping = html.xpath(
        '//span[@id = "price-shipping-message"]/b/text()'
    )
    item_return = html.xpath(
        '//div[@id="buybox"]//span[@id = "creturns-return-policy-content"]//a/text()'
    )
    item_stock_level = html.xpath(
        '//div[@id="availability"]/span/node()'
    )
    item_protection_plan = html.xpath(
        '//span[contains(string(),"Add a Protection Plan")]'
    )
    item_protection_plan_price4 = html.xpath(
        '//span/a[contains(string(),"4-Year")]/../span/text()'
    )
    item_protection_plan_price2 = html.xpath(
        '//span/a[contains(string(),"2-Year")]/../span/text()'
    )
    item_listing_price = html.xpath(
        '//td[contains(string(),"List Price:")]/../td[position()=2]/span[contains(string(),"$")]/text()'
    )
    item_is_amazon_choice = html.xpath(
        '//span[contains(string(),"Amazon\'s Choice")]'
    )
    # print(item_specs)
    # print(item_description)
    # print(item_shipping)
    # print(item_return)
    # print(item_stock_level)
    print(item_is_amazon_choice)
    print(item_listing_price)
    NA = "N/A"
    if len(item_seller) == 0:
        item_seller = NA
    else:
        item_seller = item_seller[0]

    if len(item_specs) == 0:
        item_specs = NA
    else:
        item_specs_c = []
        for i in item_specs:
            item_specs_c.append(i[16:])
        item_specs = " / ".join(item_specs_c)

    if len(item_description) == 0:
        item_description = NA
    else:
        item_description_c = []
        for i in item_description:
            item_description_c.append(i.replace("\n", ""))
        item_description = " \n ".join(item_description_c)
    if len(item_shipping) == 0:
        item_shipping = NA
    else:
        item_shipping = item_shipping[0]
    if len(item_return) == 0:
        item_return = NA
    else:
        item_return = item_return[0].replace("\n", "")
    if len(item_stock_level) == 0:
        item_stock_level = NA
    else:
        item_stock_level = item_stock_level[0].replace("\n", "")
    if len(item_protection_plan) > 0:
        item_protection_plan = True
    else:
        item_protection_plan = False
    if len(item_protection_plan_price2) == 0:
        item_protection_plan_price2 = NA
    else:
        item_protection_plan_price2 = item_protection_plan_price2[0]
    if len(item_protection_plan_price4) == 0:
        item_protection_plan_price4 = NA
    else:
        item_protection_plan_price4 = item_protection_plan_price4[0]
    if len(item_listing_price) == 0:
        item_listing_price = NA
    else:
        item_listing_price = item_listing_price[0]
    if len(item_is_amazon_choice) == 0:
        item_is_amazon_choice = False
    else:
        item_is_amazon_choice = True
    data = [item_is_amazon_choice, item_seller, item_listing_price, item_specs, item_description, item_shipping,
            item_return, item_stock_level, item_protection_plan, item_protection_plan_price2,
            item_protection_plan_price4]
    # print(data)
    return data


def to_csv(fina_data, search_item_name):
    headers = ["Name", "Price", "Link", "Customer Review", "Review Count", "Is Amazon's Choice (Recommendation)",
               "Seller", "Original Listing Price (If Applicable)", "Specs List(If Applicable)",
               "Item Description", "Shipping Option", "Returning Option", "Item Stock Level", "Protection Plan Offered",
               "Protection Plan Price (2 year)", "Protection Plan Price (4 year)"]
    csv_file = open("./data/ListSearch_" + search_item_name + ".csv", "w")
    writer = csv.writer(csv_file)
    writer.writerow(headers)
    for i in fina_data:
        writer.writerow(i)
    csv_file.close()
    return


def main(item, page_count):
    html = get_search_page(item, page_count)
    query_data = parse_and_select(html)
    # Start individual Search
    data_s = []
    # j = 0
    for i in query_data:
        # if j > 1:
        #    break
        # j += 1
        url = i[2]
        print(url)
        html_i = get_item_page(url)
        data_i = parse_and_select_item(html_i)
        data_s.append(i + data_i)

    # print(data_s[0])
    return data_s
    print("finished one search page")


if __name__ == "__main__":
    # url = "https://www.amazon.com/Gaming-GeForce-i7-9750H-Windows-G531GV-DB76/dp/B07S3L9LPT/ref=sr_1_2_sspa?crid
    # =1O5WSBCSPMOBF&keywords=gaming+laptop&qid=1583961076&sprefix=gaming+lap%2Caps%2C159&sr=8-2-spons&psc=1&spLa
    # =ZW5jcnlwdGVkUXVhbGlmaWVyPUExOFpTOTM5MDZHNlM4JmVuY3J5cHRlZElkPUEwOTYzOTcyMzFWTDE3S0VKQ0dLUiZlbmNyeXB0ZWRBZElkPUEw
    # NTQ0OTExWEkyQ1Q4N0Y2NTJQJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
    # html = get_item_page(url) parse_and_select_item(html)
    name = input("Please Input the Item You Want To Search")
    name = name.replace(" ", "+")
    page = input("Please indecate how many pages of data is needed")
    try:
        page_c = int(page)
        if page_c >= 20:
            print("TooLarge page number input")
    except:
        print("invalid page number input")
        raise KeyboardInterrupt
    print("Your search subject is " + name)
    print("You want to search for " + page + " times")
    input("Press enter to start the search")
    print("Search started")
    i = 1
    data = []
    while page_c > 0:
        print("Working on " + str(i) + "'s search, " + str(page) + " search left.")
        data_si = main(name, i)
        data = data + data_si
        page_c -= 1
        i += 1
    to_csv(data, name)
    print("All search finished and stored")
