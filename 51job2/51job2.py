"""
数据清洗2
对数据进行深度清洗
"""
#coding:utf-8
import pandas as pd
import re
#除此之外还要安装xlrd包

data = pd.read_excel(r'51job.xls',sheet_name='Job')
result = pd.DataFrame(data)
# 出现有空值（NAN）得信息，直接删除整行
# a = result.dropna(axis=0,how='any')
print(pd.set_option('display.max_rows',None))   #输出全部行，不省略
# 清洗职位出错的
b = u'数据'
number = 1
li = result['职位']
lenli = len(li)
# for i in range(0,len(li)):
# for i in range(0,len(li)):
#     try:
#         if b in li[i]:
#             print(number,li[i])
#             number+=1
#         else:
#             result = result.drop(i,axis=0)
#     except:
#         pass
# 清理信息错位
b2= u'人'
li2 = result['学历要求']
for i in range(0,412):
    try:
        if b2 in li2[i]:
            #print(number,li2[i])
            number+=1
            result = result.drop(i,axis=0)
    except:
        pass
# 薪资转换单位
b3 =u'万/年'
b4 =u'千/月'
li3 = result['薪资']
#注释部分的print都是为了调试用的
for i in range(0,412):
    try:
        if b3 in li3[i]:
            x = re.findall(r'\d*\.?\d+',li3[i])
            #print(x)
            min_ = format(float(x[0])/12,'.2f')              #转换成浮点型并保留两位小数
            max_ = format(float(x[1])/12,'.2f')
            li3[i][1] = min_+'-'+max_+u'万/月'
        if b4 in li3[i]:
            x = re.findall(r'\d*\.?\d+',li3[i])
            #print(x)
            #input()
            min_ = format(float(x[0])/10,'.2f')
            max_ = format(float(x[1])/10,'.2f')
            li3[i][1] = str(min_+'-'+max_+'万/月')
        print(i,li3[i])

    except:
        pass
# 存入令一个文件中
result.to_excel('51job2.xls', sheet_name='Job', index=False)


