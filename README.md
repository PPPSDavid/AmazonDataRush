# AmazonDataRush: Data-fetch script for tech products
## By David Yu

## 项目简述：
通过模拟用户的亚马逊搜索获得相关产品搜索结果列表，并整合存储为.csv格式。
## 项目存储数据类型：
1. 商品名称
2. 商户名称
3. 商品价格
3. 商品原价（如有优惠）
3. 用户打分（五分制）
4. 用户打分数量
5. 商品详情页链接
6. 商品是否为亚马逊优选
1. 商品可选配置（电子产品等）
1. 商品简介
1. 商品快递类型
1. 商品退货类型
1. 商品库存情况
1. 商品是否带有意外险

    - 如果有亚马逊标准2年/4年保险，记录其价格
## 项目设计思路
1. 通过两层信息爬取兼顾信息的完整性与信息的详细程度

        因为亚马逊搜索页面中各个商品包含的信息不同（如有商品为非亚马逊自营，其包含的信息相对于自营Prime产品更少），故只
        通过搜索页获得的信息存在较大局限性。
        
        在本项目中，在标准的搜索页信息摘取后还会对各个商品详情页访问并抓取信息，因此页面更为详细，故可以包含如邮寄，退货，
        商品库存等等。
1. 可用于多种不同商品搜索

        本项目中采用的XPayth指令均具有广泛实用性，可被用于各种商品的搜索与整理。
       （由于亚马逊有些商品搜索列表格式不同，故本项目目前仅可匹配两种网页格式中的一种：单行一个商品，常见于科技产品搜索中）
        经测试，大多数科技产品均可完全适配。
        
1. 较高可用性的用户IO

        项目中自带可以方便使用的 main函数，可以通过终端简单调用，并在data文件夹中找到程序自动存储在对应名称的数据。

## 附带数据集
- 搜索内容： "Gaming Laptop"
- 搜索页面数量： "5"

测试过的其他搜索："phone"，"Apple"， "graphics card"
## 所用库列表
1. lxml
2. requests
3. csv
4. random
5. time
        
## 待完成部分
1. 反反爬虫

        亚马逊自带反爬虫程序目前版本通过模仿真实浏览器的头部数据达到绕开的目的。
        此方法可保证在测试运行中不出现被侦测的情况，但可能会在大规模抓取时出现问题。
    
        项目代码中包含了用proxy代理随机的进一步伪装访问的代码，但由于公共proxy过于不稳定
        且在小规模使用时没有帮助，故没有运用。未来可以进一步优化此功能。
2. 支持全部亚马逊搜索页面
        
        未来可以通过设计单独的抓取逻辑适配目前未被适配的页面。