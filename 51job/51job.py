# -*- coding:utf-8 -*-
import urllib.request
import xlwt
import re
import urllib.parse
import time


"""
re方法爬取
url="https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html"
a = urllib.request.urlopen(url)
html = a.read().decode('gbk')   
reg = re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)" href="(.*?)".*? <span class="t2"><a target="_blank" title="(.*?)" href="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*?<span class="t5">(.*?)</span>.*?',re.S)#匹配换行符
items=re.findall(reg,html)
"""


"""
url="https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html"
res = requests.get(url).text
s = etree.HTML(res)  # 将源码转化为能被 XPath 匹配的格式
#然后
requir = s.xpath('                此处输从网页中复制的xpath或者自己写的索引                     /text()')

"""
#模拟浏览器
header={
    'Host':'search.51job.com',
    'Referer':'https://mkt.51job.com/tg/sem/pz_2018.html?from=baidupz',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) 37abc/2.0.6.16 Chrome/60.0.3112.113 Safari/537.36'
}

def getfront(page,item):

     result = urllib.parse.quote(item)
     ur1 = result+',2,'+ str(page)+'.html'
     ur2 = 'http://search.51job.com/list/000000,000000,0000,00,9,99,'
     res = ur2+ur1
     a = urllib.request.urlopen(res)
     html = a.read().decode('gbk')          # 读取源代码并转为unicode
     return html

def getInformation(html):
    reg = re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)" href="(.*?)".*? <span class="t2"><a target="_blank" title="(.*?)" href="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*?<span class="t5">(.*?)</span>.*?',re.S)#匹配换行符
    items=re.findall(reg,html)
    return items


excel1 = xlwt.Workbook()
# 设置单元格
sheet1 = excel1.add_sheet('Job', cell_overwrite_ok=True)
sheet1.write(0, 0, '序号')
sheet1.write(0, 1, '职位')
sheet1.write(0, 2, '公司名称')
sheet1.write(0, 3, '公司地点')
sheet1.write(0, 4, '公司性质')
sheet1.write(0, 5, '薪资')
sheet1.write(0, 6, '学历要求')
sheet1.write(0, 7, '工作经验')
sheet1.write(0, 8, '公司规模')
sheet1.write(0, 9, '公司类型')
sheet1.write(0, 10,'公司福利')
sheet1.write(0, 11,'发布时间')
sheet1.write(0, 12,'任职要求')

# hrbp
number = 1
item = input()
for j in range(1,2000):   #页数自己随便改
    try:
        print("正在爬取第"+str(j)+"页数据...")
        html = getfront(j,item)      #调用获取网页原码
        for i in getInformation(html):
            try:
                url1 = i[1]          #职位网址
                res1 = urllib.request.urlopen(url1).read().decode('gbk')
                company = re.findall(re.compile(r'<div class="com_tag">.*?<p class="at" title="(.*?)"><span class="i_flag">.*?<p class="at" title="(.*?)">.*?<p class="at" title="(.*?)">.*?',re.S),res1)
                job_need = re.findall(re.compile(r'<p class="msg ltype".*?>.*?&nbsp;&nbsp;<span>|</span>&nbsp;&nbsp;(.*?)&nbsp;&nbsp;<span>|</span>&nbsp;&nbsp;(.*?)&nbsp;&nbsp;<span>|</span>&nbsp;&nbsp;.*?</p>',re.S),res1)
                welfare = re.findall(re.compile(r'<span class="sp4">(.*?)</span>',re.S),res1)
                print(i[0],i[2],i[4],i[5],company[0][0],job_need[2][0],job_need[1][0],company[0][1],company[0][2],welfare,i[6])
                sheet1.write(number,0,number)
                sheet1.write(number,1,i[0])
                sheet1.write(number,2,i[2])
                sheet1.write(number,3,i[4])
                sheet1.write(number,4,company[0][0])
                sheet1.write(number,5,i[5])
                sheet1.write(number,6,job_need[1][0])
                sheet1.write(number,7,job_need[2][0])
                sheet1.write(number,8,company[0][1])
                sheet1.write(number,9,company[0][2])
                sheet1.write(number,10,("  ".join(str(i) for i in welfare)))
                sheet1.write(number,11,i[6])
                number+=1
                excel1.save("51job.xls")
                time.sleep(0.3) #休息间隔，避免爬取海量数据时被误判为攻击，IP遭到封禁
            except:
                pass
    except:
        pass

excel1.save("51job.xls")
