import requests
from bs4 import BeautifulSoup
import json
import xlwt
import time
import random

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
]

headers = {
    "user-agent": random.choice(user_agent_list),
    'cookie': '_uab_collina=158138884277552994676298; lastCity=101010100; __c=1581476493; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1581391502,1581417868,1581472777,1581476493; __l=l=https%3A%2F%2Fwww.zhipin.com%2Fbeijing%2F&r=&friend_source=0&friend_source=0; __a=16861044.1581388836.1581472775.1581476493.35.4.14.25; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1581480500; __zp_stoken__=ff57uAOoO2oYSklcgvBgzRRgM46Sg6gb8MDDMcqWJLYev5jQWQ3uJv7bhIA4bTJxqtLuaY%2FXMJX46R%2F5LxRk%2F8V4K3nAWfscyADQ7RZndaFrz2hpR89eAjSv9f8OVDrXjexJ'
    }

excel1 = xlwt.Workbook()
# 设置单元格
sheet1 = excel1.add_sheet('Job', cell_overwrite_ok=True)
sheet1.write(0, 0, '职位名称')
sheet1.write(0, 1, '公司名称')
sheet1.write(0, 2, '行业')
sheet1.write(0, 3, '融资情况')
sheet1.write(0, 4, '公司人数')
sheet1.write(0, 5, '薪资')
sheet1.write(0, 6, '工作地点')
sheet1.write(0, 7, '工作经验')
sheet1.write(0, 8, '学历要求')
sheet1.write(0, 9, '职位描述')
# 获取指定城市的编码
def get_city_code(city_name):
    response = requests.get("https://www.zhipin.com/wapi/zpCommon/data/city.json")
    contents = json.loads(response.text)
    cities = contents["zpData"]["hotCityList"]
    city_code = contents["zpData"]["locationCity"]["code"]
    for city in cities:
        if city["name"] == city_name:
            city_code = city["code"]
    return city_code


def get_url(query="", city="", industry="", position="", page=1):
    base_url = "https://www.zhipin.com/job_detail/?query={}&city={}&industry={}&position={}&page={}"
    urls = []
    url = base_url.format(query, city, industry, position, page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    page_list = soup.find("div", "page").find_all("a")
    urls.append(url)
    while page_list[len(page_list) - 1]["href"] != "javascript:;":
        page += 1
        url = base_url.format(query, city, industry, position, page)
        urls.append(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        page_list = soup.find("div", "page").find_all("a")
    return urls


def get_html(url):
    response = requests.get(url, headers=headers)
    return response.text


def job_info(job_name, company, industry, finance, staff_number, salary, site, work_experience, education_bak, job_desc):
    return {
        "job_name": job_name,
        "company": company,
        "industry": industry,
        "finance": finance,
        "staff_number": staff_number,
        "salary": salary,
        "site": site,
        "work_experience": work_experience,
        "education_bak": education_bak,
        "job_desc": job_desc
    }


def get_job_desc(jid, lid):
    url = "https://www.zhipin.com/wapi/zpgeek/view/job/card.json?jid={}&lid={}"
    response = requests.get(url.format(jid, lid), headers=headers)
    html = json.loads(response.text)["zpData"]["html"]
    soup = BeautifulSoup(html, "lxml")
    desc = soup.find("div", "detail-bottom-text").get_text()
    return desc


def get_content(html,number):
    bs = BeautifulSoup(html, 'lxml')
    contents = []
    number2=number+1
    for info in bs.find_all("div", "job-primary"):
        job_name = info.find("span", "job-name").get_text()
        # job_name = info.find("div", "job-title").get_text()
        job_area = info.find("span", "job-area").get_text()
        company = info.find("div", "company-text").a.get_text()
        jid = info.find("div", "info-primary").a["data-jid"]
        lid = info.find("div", "info-primary").a["data-lid"]
        desc = get_job_desc(jid, lid)
        texts = [text for text in info.find("div", "info-primary").p.stripped_strings]
        site = texts[0]
        work_exp = "texts[1]"
        edu_bak = "texts[2]"
        salary = info.span.get_text()
        salary = info.find("span", "red").get_text()
        companies = [text for text in info.find("div", "company-text").p.stripped_strings]
        industry = companies[0]
        if len(companies) > 2:
            finance = companies[1]
            staff_num = companies[2]
        else:
            finance = None
            staff_num = companies[1]
        sheet1.write(number2, 0, job_name)
        sheet1.write(number2, 1, company)
        sheet1.write(number2, 2, industry)
        sheet1.write(number2, 3, finance)
        sheet1.write(number2, 4, staff_num)
        sheet1.write(number2, 5, salary)
        sheet1.write(number2, 6, job_area)
        sheet1.write(number2, 7, work_exp)
        sheet1.write(number2, 8, edu_bak)
        sheet1.write(number2, 9, desc)
        excel1.save("liepin0.xls")
        number2 += 1
        print(str(number2)+ "---",job_name, company, industry, finance, staff_num, salary, job_area, work_exp, edu_bak, desc)
        contents.append(job_info(job_name, company, industry, finance, staff_num, salary, site, work_exp, edu_bak, desc))
        time.sleep(1)
    return contents


def save_data(content, city, query):
    file = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = file.add_sheet("job_info", cell_overwrite_ok=True)
    sheet.write(0, 0, "职位名称")
    sheet.write(0, 1, "公司名称")
    sheet.write(0, 2, "行业")
    sheet.write(0, 3, "融资情况")
    sheet.write(0, 4, "公司人数")
    sheet.write(0, 5, "薪资")
    sheet.write(0, 6, "工作地点")
    sheet.write(0, 7, "工作经验")
    sheet.write(0, 8, "学历要求")
    sheet.write(0, 9, "职位描述")
    for i in range(len(content)):
        sheet.write(i+1, 0, content[i]["job_name"])
        sheet.write(i+1, 1, content[i]["company"])
        sheet.write(i+1, 2, content[i]["industry"])
        sheet.write(i+1, 3, content[i]["finance"])
        sheet.write(i+1, 4, content[i]["staff_number"])
        sheet.write(i+1, 5, content[i]["salary"])
        sheet.write(i+1, 6, content[i]["site"])
        sheet.write(i+1, 7, content[i]["work_experience"])
        sheet.write(i+1, 8, content[i]["education_bak"])
        sheet.write(i+1, 9, content[i]["job_desc"])
    file.save(r'c:\projects\{}_{}.xls'.format(city, query))


# def main():
#     city_name = "深圳"
#     city = get_city_code(city_name)
#     city = 'c100010000'
#     query = "hrbp"
#     urls = get_url(query=query, city=city)
#     contents = []
#     for url in urls:
#         html = get_html(url)
#         content = get_content(html)
#         contents += content
#         time.sleep(5)
#     save_data(contents, city_name, query)

def main():
    city_name = "深圳"
    city = get_city_code(city_name)
    city = '100010000'
    query = "hrbp"
    urls = "https://www.zhipin.com/c100010000/?query=hrbp&page="
    # contents = []
    number = 0
    for i in range(10):
        url = urls+str(i+1)
        html = get_html(url)
        content = get_content(html,number)
        number+=30
        time.sleep(2)
    excel1.save("liepin0.xls")
    # save_data(contents, '全国', 'hrbp')


if __name__ == '__main__':
    main()




