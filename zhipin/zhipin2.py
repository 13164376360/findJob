import requests
from bs4 import BeautifulSoup
import time
import xlwt  # 用来创建excel文档并写入数据
from selenium import webdriver
import time

#
# driver = webdriver.Chrome()
# driver.get('https://www.zhipin.com/c100010000/?query=hrbp&period=3&page=1')
# print("初始化浏览器")

def initRequest():
    global url_pattern, headers
    url_pattern = 'https://www.zhipin.com/{}/?query={}&period={}&page='.format(city, key, period)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
        "cookie" : "_uab_collina=158138884277552994676298; lastCity=101010100; sid=sem_pz_bdpc_dasou_title; __c=1581382946; __g=sem_pz_bdpc_dasou_title; __l=l=https%253A%252F%252Fwww.zhipin.com%252Fbeijing%252F%253Fsid%253Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fwww.zhipin.com%2Fbeijing%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0&g=%2Fwww.zhipin.com%2Fbeijing%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0; __zp_stoken__=96e92soKXIjFTith5N6PPFAmsrYQVKFfPwmUZTJ%2FYwyQifNKMrDQ21kYH%2B%2BrinwLNgk2as%2BKyXee1kVvBSxFXY3FHtqOJRzZvG2fuY%2FP0JsIH13xWoV6hNTRn9GwrWBxvTa1; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1581382949,1581388841,1581390943,1581391502; __zp_seo_uuid__=7e0b6c61-0bf2-4d1d-af8d-b3361b5a6f8f; __a=16861044.1581388836..1581382946.9.1.9.5; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1581391973"
    }


def initExcel():
    global newTable, wb, ws, headData
    hud = ['职位名', '薪资1', '薪资2', '职位名', '地点', '经验', '学历', '公司行业', '融资阶段', '公司人数', '发布日期', '发布人']
    print('\t'.join(hud))

    import datetime
    nowTime = datetime.datetime.now().strftime('%Y%m%d-%H%M')  # 现在
    newTable = "boss-" + city + "-" + nowTime + "-" + key + "-" + period + ".xls"  # 表格名称

    print(newTable)

    wb = xlwt.Workbook(encoding='utf-8')  # 创建excel文件，声明编码
    ws = wb.add_sheet('sheet1')  # 创建表格
    headData = ['公司名', '职位名', '薪资1', '薪资2', '职位名', '经验要求', '学历要求', '公司行业', '融资阶段', '公司人数', '发布日期', '发布人']  # 表头部信息
    for colnum in range(0, len(headData) - 1):
        ws.write(0, colnum, headData[colnum], xlwt.easyxf('font: bold on'))  # 行，列


def excel_write(items, index):
    # 爬取到的内容写入excel表格
    for item in items:  # 职位信息
        for i in range(0, len(headData) - 1):
            # print item[i]
            ws.write(index, i, item[i])  # 行，列，数据
            print(str(index) + "\t" + str(i) + "\t" + item[i])
        index += 1


def start():
    try:
        page = 1
        pageSize = 0
        for n in range(1, 11): #页数
            url = url_pattern + str(page)
            print(url)
            # html = driver.get(url, headers=headers)
            html = requests.get(url)
            print(html.text)
            page += 1
            soup = BeautifulSoup(html.text, 'html.parser')
            items = []
            jobPrimarys = soup.find_all('div', 'job-primary')
            if pageSize == 0:
                pageSize = len(jobPrimarys)
                print("页面总数：" + str(pageSize))
            for jobPrimary in jobPrimarys:
                item = []
                # print(gongsi)
                gongsi = jobPrimary.find('div', 'company-text').find('a').string
                item.append(gongsi)  # 公司名

                item.append(jobPrimary.find('div', 'job-title').string)  # 职位名

                xinzi = jobPrimary.find('span', 'red').string
                xinzi = xinzi.replace('k', '')
                xinzi = xinzi.split('-')
                item.append(xinzi[0])  # 薪资起始数
                item.append(xinzi[1])  # 薪资起始数

                yaoqiu = jobPrimary.find('p').contents
                item.append(yaoqiu[0].string if len(yaoqiu) > 0 else 'None')  # 地点
                item.append(yaoqiu[2].string if len(yaoqiu) > 2 else 'None')  # 经验
                item.append(yaoqiu[4].string if len(yaoqiu) > 4 else 'None')  # 学历

                gongsi = jobPrimary.find('div', 'info-company').find('p').contents
                item.append(gongsi[0].string if len(gongsi) > 0 else 'None')  # 公司行业
                item.append(gongsi[2].string if len(gongsi) > 2 else 'None')  # 融资阶段
                item.append(gongsi[4].string if len(gongsi) > 4 else 'None')  # 公司人数

                item.append(jobPrimary.find('div', 'info-publis').find('p').string.replace('发布于', ''))  # 发布日期
                item.append(jobPrimary.find('div', 'info-publis').find('h3').contents[3].string)  # 发布人

                print('\t'.join(item))

                _item = tuple(item)  # 转为元组
                items.append(_item)  # 转为数组
                time.sleep(0.3)

            # 写入excel
            index = (n - 1) * pageSize + 1
            excel_write(items, index)
    except:
        wb.save(newTable)
        pass
    # 保存
    wb.save(newTable)


print("----------初始化参数----------")
key = 'hrbp'  # 搜索关键字
period = '3'  # 1天发布，1； 3天发布，2； 7天发布，3；
city = 'c100010000'  # c101280600 深圳

print("----------初始化请求----------")
initRequest()

print("----------初始化excel----------")
initExcel()

print("----------开始----------")
start()

