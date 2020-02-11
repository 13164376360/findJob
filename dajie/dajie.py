# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib
import random
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time


# 网络数据爬虫
# chrome driver下载目录
# http://chromedriver.storage.googleapis.com/index.html?path=73.0.3683.20/
class DataParser():
    def __init__(self):
        self.url = 'https://so.dajie.com/job'

        self.searchContent = "Java"
        # 谷歌浏览器驱动位置
        driverPath = 'E:\\SoftInstall\\Python3.8\\install\\chromedriver.exe'
        self.browser = webdriver.Chrome(executable_path=driverPath)

    def excute(self):
        browser = self.browser
        # 打开浏览器
        browser.get(self.url)
        # 关掉弹出页面
        register_close_btn = browser.find_element_by_class_name('xxxxxx')
        register_close_btn.click()
        # 进入搜索页面并且搜索词条
        search_input_btn = browser.find_element_by_id('xxxx')
        search_input_btn.send_keys(self.searchContent)
        browser.find_element_by_id('xxxx').click()

        # jquery获取查询到的内容
        # script = 'return document.getElementById("xxxxxxx")'
        # doc = browser.execute_script(script).page_source()
        # print(doc)
        time.sleep(5)

        # xxxxx是容器div，ul是子标签
        # 通过浏览器XPATH获取每个标签
        data = browser.find_elements_by_xpath('xxxxxxxx')

        print(len(data))
        # 每条元素在li标签中
        for i in range(len(data)):
            print(i)
            job_content = data[i].find_element_by_xpath('xxxxxx')
            # 招聘网址链接
            job_href = job_content.get_attribute('xxx')
            print(job_href)
            # 岗位名称
            job_name = job_content.text
            print(job_name)
            browser.implicitly_wait(10)
            # 薪水
            # salary = data[i].find_element_by_class_name('xxx').text
            # print(salary)
            # 地区
            # ads = data[i].find_element_by_class_name('xxx').text
            # print(ads)
            # 经验
            # suffer = data[i].find_element_by_class_name('xxx').text
            # print(suffer)
            # 学历
            # edu = data[i].find_element_by_class_name('xxx').text
            # print(edu)
            print('***********************************')


if __name__ == '__main__':
    parser = DataParser()
    parser.excute()