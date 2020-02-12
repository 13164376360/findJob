import requests
from lxml import etree
from urllib.parse import urlencode
import ssl
import csv
import time

"""搜索的职业名称"""
position_type = '幼教培训师'

"""输出文件名"""
csv_name = "zhaopin3" + '.csv'
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 写入文件表头的字段
with open(csv_name, 'a', newline='', encoding='utf-8') as fp:
    writer = csv.writer(fp)
    writer.writerow(['职业名称', '公司简介', '薪资', '要求', '福利', '岗位职责及要求', '地址', '网址', '获取时间'])

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'referer': 'https://www.zhipin.com/c100010000/?query=hrbp&ka=sel-city-100010000',
    'cookie' : '_uab_collina=158133362979252410346994; lastCity=101010100; __c=1581476493; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1581391502,1581417868,1581472777,1581476493; __l=l=https%3A%2F%2Fwww.zhipin.com%2Fbeijing%2F&r=&friend_source=0&friend_source=0; __a=16861044.1581388836.1581472775.1581476493.25.4.4.15; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1581476531; __zp_stoken__=ff57uAOoO2oYSklcgvBgzRRgMycO5dtYszxbWJoT%2Brf7ApaUyky6G2q%2Bmj%2B4oFtXmAeTaY%2FXMJX46R%2F5LxRk%2F8V4K87%2FC%2BQHQM1o6Kn%2F8U%2F%2BWsRpR89eAjSv9f8OVDrXjexJ'
}

# 先用固定的url获取总页数
# 1、构建固定的参数

Base_url = 'https://www.zhipin.com/c100010000/?query=hrbp&page='
for i in range(10):
    url = Base_url+str(i+1)
    print(url)

# 2、发送请求骗取页数
resp = requests.get(url, headers=HEADERS)
resp.encoding = 'utf-8'
text = resp.text
# print(text)
html = etree.HTML(text)
'''total_page页数在此，需要加入如果没有第二页的判断'''
try:
    total_page = html.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    print("总页数一共为：" + str(total_page) + "!")
except:
    total_page = None
    print("没有第二页！！！！！")
# 3、获取列表页下面的每个详情页的url
href = html.xpath("//div[@class='info-primary']//a/@href")
for h in href:
    detail_url = 'https://www.zhipin.com' + h
    print(detail_url)
    print("\n当前时间为：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    time.sleep(5)

    # 4、通过详情页去获取内容,是详情页，而不是上面的列表页url
    resp = requests.get(detail_url, headers=HEADERS)
    resp.encoding = 'utf-8'
    text = resp.text
    html = etree.HTML(text)
    title = html.xpath("//h1/text()")[0]
    try:
        company_profile = html.xpath("//div[@class='job-sec company-info']/div[@class='text']/text()")[
                              0].strip() + "..."
    except:
        company_profile = '没有公司简介！！！！！！！！'
    print(company_profile)
    salary = html.xpath("//span[@class='salary']/text()")[0]
    req = html.xpath("//div[@class='info-primary']//p/text()")[:3]
    job_tag = html.xpath("//div[@class='tag-container']//div[@class='tag-all job-tags']//span/text()")
    positions = html.xpath("//div[@class='job-sec']/div[@class='text']/text()")
    position_description = []
    for posi in positions:
        position_description.append(posi.strip())
    address = html.xpath("//div[@class='job-location']/div[@class='location-address']/text()")[0].strip()
    with open(csv_name, 'a', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(
            [title, company_profile, salary, req, job_tag, position_description, address, detail_url, current_time])


def get_detail_urls(url):
    resp = requests.get(url, headers=HEADERS)
    resp.encoding = 'utf-8'
    text = resp.text
    html = etree.HTML(text)
    href = html.xpath("//div[@class='info-primary']//a/@href")
    for h in href:
        detail_url = 'https://www.zhipin.com' + h
        print(detail_url)
        print("\n当前时间为：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        time.sleep(5)
        get_detail_content(detail_url)


# 获取详情页的内容
def get_detail_content(url):
    resp = requests.get(url, headers=HEADERS)
    resp.encoding = 'utf-8'
    text = resp.text
    html = etree.HTML(text)
    title = html.xpath("//h1/text()")[0]
    try:
        company_profile = html.xpath("//div[@class='job-sec company-info']/div[@class='text']/text()")[
                              0].strip() + "..."
    except:
        company_profile = '没有公司简介！！！！！！！！'
    salary = html.xpath("//span[@class='salary']/text()")[0]
    req = html.xpath("//div[@class='info-primary']//p/text()")[:3]
    job_tag = html.xpath("//div[@class='tag-container']//div[@class='tag-all job-tags']//span/text()")
    positions = html.xpath("//div[@class='job-sec']/div[@class='text']/text()")
    position_description = []
    for posi in positions:
        position_description.append(posi.strip())
    address = html.xpath("//div[@class='job-location']/div[@class='location-address']/text()")[0].strip()
    with open(csv_name, 'a', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(
            [title, company_profile, salary, req, job_tag, position_description, address, detail_url, current_time])


# 定义主方法获取所有列表页
def spider():
    if total_page is not None:
        for i in range(2, int(total_page) + 1):
            print("当前在第" + str(i) + "页！")
            ka = 'page-' + str(i)
            params = {
                'query': position_type,
                'page': i,
                'ka': ka
            }
        Base_url = 'https://www.zhipin.com/c101200100/?'
        url = Base_url + urlencode(params)
        get_detail_urls(url)


if __name__ == '__main__':
    spider()