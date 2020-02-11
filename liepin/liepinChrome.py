import csv
from time import sleep
from bs4 import BeautifulSoup
import xlwt
import lxml
import requests
from lxml import etree
from selenium import webdriver


driver = webdriver.Chrome()
driver.get('https://www.liepin.com/zhaopin/?init=-1&headckid=181a371f3583bfee&fromSearchBtn=2&pubTime=30&ckid=27fda43c09cfd22a&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=hrbp&siTag=wpx05sEHOAKOTToVOh4zJw~UoKQA1_uiNxxEb8RglVcHg&d_sfrom=search_fp&d_ckId=72cb43ffd77e25f190635f45f4400ce0&d_curPage=0&d_pageSize=40&d_headId=8551d000d99330889491c8d91023137d&curPage=')
print("初始化浏览器")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"}

url = 'https://www.liepin.com/zhaopin/?init=-1&headckid=181a371f3583bfee&fromSearchBtn=2&pubTime=30&ckid=27fda43c09cfd22a&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=hrbp&siTag=wpx05sEHOAKOTToVOh4zJw~UoKQA1_uiNxxEb8RglVcHg&d_sfrom=search_fp&d_ckId=72cb43ffd77e25f190635f45f4400ce0&d_curPage=0&d_pageSize=40&d_headId=8551d000d99330889491c8d91023137d&curPage='

excel1 = xlwt.Workbook()
# 设置单元格
sheet1 = excel1.add_sheet('Job', cell_overwrite_ok=True)
sheet1.write(0, 0, '序号')
sheet1.write(0, 1, '招聘岗位')
sheet1.write(0, 2, '薪酬')
sheet1.write(0, 3, '公司地址')
sheet1.write(0, 4, '所需学历')
sheet1.write(0, 5, '工作经验')
sheet1.write(0, 6, '公司名称')
sheet1.write(0, 7, '公司性质')
sheet1.write(0, 8, '公司福利')
sheet1.write(0, 9, '公司类型')
sheet1.write(0, 10, '公司规模')
def toexcel():
    print()


def getPerPageInfo(url,number):
    html = requests.get(url, headers=headers).text
    driver.get(url)
    html = driver.execute_script("return document.documentElement.outerHTML")
    mytree = lxml.etree.HTML(html)
    if mytree.xpath('//ul[@class="sojob-list"]/li') is None:
        print('又被限制ip了1')
        sleep(60)
        driver.get(url)
        html = driver.execute_script("return document.documentElement.outerHTML")
    postList = mytree.xpath('//ul[@class="sojob-list"]/li')
    number2 = number+1
    print("抓取下面这一页数据")
    print(number)
    for post in postList:
        postTitle = post.xpath('.//div[@class="job-info"]/h3/a/text()')[0]
        postInfo = post.xpath('.//div[@class="job-info"]/p/span//text()')
        postadd = post.xpath('.//div[@class="job-info"]/p/a//text()')
        postSalary = postInfo[0]
        postEDU = postInfo[1]
        postExperience = postInfo[2]
        postName = post.xpath('.//p[@class="company-name"]/a/text()')
        posturl = post.xpath('.//div[@class="job-info"]/h3/a/@href')[0]
        posturllen = len(posturl)
        if posturllen < 27:
            continue
         # gongsiguimo = requests.get(posturl,headers=headers).text
        driver.get(posturl)
        gongsiguimo = driver.execute_script("return document.documentElement.outerHTML")
        mytree2 = lxml.etree.HTML(gongsiguimo)
        postList2 = mytree2.xpath('.//ul[@class="new-compintro"]/li//text()')
        lengthpost = len(postList2)
        if len(postList2) <= 3 &len(postList2) >=1 :
            print(number2)
            print("数据不全！！！")
            continue
        if len(postList2) <= 4 :
            print('又被限制ip了2')
            sleep(60)
            continue
            driver.get(posturl)
            gongsiguimo = driver.execute_script("return document.documentElement.outerHTML")
            mytree2 = lxml.etree.HTML(gongsiguimo)
        postList2 = mytree2.xpath('.//ul[@class="new-compintro"]/li//text()')
        guimo1 = postList2[1]
        guimo2 = postList2[3]
        guimo2 = guimo2.strip('公司规模：')
        guimo3 = postList2[4]
        guimo3 = guimo2.strip('公司地址：')
        postxingzhi = post.xpath('.//p[@class="field-financing"]/span/text()')
        postfuli = post.xpath('.//p[@class="temptation clearfix"]/span//text()')
        postfuli1 = ''
        for fuli in postfuli:
            postfuli1 = postfuli1 + " "+fuli
        infoList = [postTitle, postSalary,postadd, postEDU, postExperience,postName,postxingzhi,postfuli1,guimo1,guimo2]
        print(number2,postTitle, postSalary, postEDU, postExperience,postName,postxingzhi,guimo1,guimo2)
        sheet1.write(number2, 0, number2)
        sheet1.write(number2, 1, infoList[0])
        sheet1.write(number2, 2, infoList[1])
        sheet1.write(number2, 3, infoList[2])
        sheet1.write(number2, 4, infoList[3])
        sheet1.write(number2, 5, infoList[4])
        sheet1.write(number2, 6, infoList[5])
        sheet1.write(number2, 7, infoList[6])
        sheet1.write(number2, 8, infoList[7])
        sheet1.write(number2, 9, infoList[8])
        sheet1.write(number2, 10, infoList[9])
        excel1.save("liepin2.xls")
        number2+=1
        # 将得到的数据用csv格式存储
        writer.writerow(infoList)  # writerows()会把单个字符写入到一个单元格中，而writerow()会把一个字符串写入一个单元格中
        sleep(0.3)


if __name__ == '__main__':

    csvHeader = ['招聘岗位', '薪酬', '地点', '所需学历', '工作经验','公司名称','公司性质','公司福利']

    with open('./猎聘网hrbp相关岗位信息.csv', 'a+', encoding='utf-8', errors='ignore', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(csvHeader)
        number = 0
        for i in range(1000):
            url = url + str(i)
            print("爬取第  页数据")
            print(i)
            getPerPageInfo(url,number)
            number=number+40
            sleep(0.5)  # 每一页爬取时延迟一会，防止对别人服务器造成太大压力

excel1.save("liepin2.xls")