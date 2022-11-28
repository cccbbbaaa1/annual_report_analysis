# 用于抽样，
import csv
import os
import random
import pandas as pd
csv.field_size_limit(500 * 1024 * 1024) # 增大CSV加载内存
    # indust1 = 43
    # indust2 = 2876
    # indust3 = 1231

def rand_num_list(population,ratio):  # 给定size，返回占size ratio%个数的随机数序列
    num=int(population*ratio/100)
    #print(random.sample(range(population),num))
    return random.sample(range(population),num)

def indust_list():              #确定三大产业的各自的年报数量并返回数组
    csv_path = '../txt2excel/annual_reports.csv'  # 包含所有年报的csv，列名为stockid,name,year,industry,content
    fp = open(csv_path, encoding='utf8')
    reader = csv.DictReader(fp)
    indust_l=[0,0,0,0]
    for row in reader:
        # print(row['industry'])
        if row['industry']=='1':
            indust_l[1]+=1
        elif row['industry']=='2':
            indust_l[2]+=1
        elif row['industry']=='3':
            indust_l[3]+=1
    print(indust_l)
    fp.close()
    return indust_l

if __name__=="__main__":
    csv_path='../txt2excel/annual_reports.csv' # 包含所有年报的csv，列名为stockid,name,year,industry,content
    fp = open(csv_path,encoding='utf8')
    reader = csv.DictReader(fp)
    #industry_num_list=indust_list()  #各产业年报总数
    industry_num_list=[0, 43, 2876, 1231]      # 分层抽样比例
    randomlist=[0,rand_num_list(industry_num_list[1],5),rand_num_list(industry_num_list[2],5),rand_num_list(industry_num_list[3],5)] #得到抽样5%的随机数数组
    count_list=[0,0,0,0]
    with open('./report_sample.txt','w',encoding='utf-8') as txt:
        for row in reader:  #遍历每一行年报
            for i in range(1,4):   #查找对应产业
                if row['industry'] == str(i):
                    count_list[i]+=1
                    #print(count_list[i])
                    if count_list[i] in [randomlist[i][j] for j in range(0,len(randomlist[i]))]:
                        txt.write(row['content'])
                        print(row['name'],row['year'])
    txt.close()





    # rand_num1 = rand_num_list(indust1,5)
    # rand_num2 = rand_num_list(indust2,5)
    # rand_num3 = rand_num_list(indust3,5)


    #for row in reader:


