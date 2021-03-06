import xlsxwriter
import re
import time
import requests

workbook = xlsxwriter.Workbook('英才网_shenzhen.xlsx')
worksheet = workbook.add_worksheet()

url = 'https://search.chinahr.com/bj/job/?key=hrbp'
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}

# 主页html
html_all = requests.get(url, headers=header)
html_all = html_all.text

find_mainsection = re.compile(r'href=\"(http://m\.chinahr\.com/shenzhen/jobs/\d{5}/)">\s*?<li>(.*?)</li>')
html_name_list = find_mainsection.findall(html_all)

name_H = 1
for html_name in html_name_list:
    worksheet.write(name_H, 0, html_name[1])
    name_H = name_H + 1
    print(html_name[1])
    # 已经写入职业名称

    # 每项工作抓取的页数
    for job_page in range(1, 4):
        url_job = html_name[0] + '%s/' % job_page
        # print(url_job)
        # time.sleep(30)

        html_job = requests.get(html_name[0], headers=header)
        html_job = html_job.text
        # print(html_job)
        # time.sleep(3000)
        find_wages = re.compile(r'<div class=\"list_price\">(\d{3,5})-(\d{3,5})</div>')
        wages = find_wages.findall(html_job)
        wages_L = 2

        wages_all = 0

        for wage_wage in wages:
            wage_start = int(wage_wage[0])
            wage_end = int(wage_wage[1])
            # print('这是工资匹配结果',wage_wage,'平均',wage_start/2.0+wage_end/2.0)
            wage_mean = wage_start / 2.0 + wage_end / 2.0
            worksheet.write(name_H - 1, wages_L, wage_mean)
            wages_L = wages_L + 1

            # 新增加
            wages_all = wages_all + wage_mean
            wages_mean = wages_all / (wages_L - 2)
            worksheet.write(name_H - 1, 1, wages_mean)

    # time.sleep(1)
workbook.close()
print('写入成功')
# exit()