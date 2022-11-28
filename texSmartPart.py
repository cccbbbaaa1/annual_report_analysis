# 进行分词+词频统计，得到json/csv结果
import json
import re
import time
import requests
import csv
from collections import defaultdict
word_list_count = defaultdict(lambda: 0)


def separate_sentence(txt_path):  #用中文句号、分号进行断句并用defaultdict计数
    counts = defaultdict(lambda: 0)
    with open(txt_path,'r',encoding="utf-8") as txt:
        content=txt.read()
        separate_contents=re.split(r'([。;；]|  |   )',content)
        for sentence in separate_contents:
            if not sentence.isdigit() and not len(sentence) <= 3:
                if len(sentence) > 8190:
                    pieces=re.split(r'( )',sentence)
                    for piece in pieces:
                        counts[piece] += 1
                else:
                    counts[sentence] += 1
    txt.close()
    return counts

def upload(upload_str,i):  #上传短句至API接口并得到返回结果
    obj = {"str": upload_str,
           "options":{
               "input_spec": {"lang": "auto"},  # 语言类型自动识别
               "syntactic_parsing":{"enable":False},  #句法分析
               "text_cat": {"enable": True},   # 文本分类工具
               "srl":{"enable":False}  # 语义角色标注
           }}
    req_str = json.dumps(obj).encode()
    url = "https://texsmart.qq.com/api"
    r = requests.post(url, data=req_str)
    time.sleep(2)
    print(i)
    # r.encoding = "utf-8"
    # print(r.text)
    if r.json():
        js=open('./json_result/'+ str(i)+ '.json','w',encoding='utf-8')   # 将每次的结果都存入一个单独的json文件
        js.write(r.text)
        print("写入json文件完成！")
        js.close()
        r = r.json()
        return r
    else:
        print("返回结果为空!")
        return ''


def store_res(json_res):  # 对得到的分词结果进行存储
    res_list=json.loads(json_res)

    return

def wordlist_analysis(freq,word_list):  # 对"word_list"内容进行分析与计数,freq为该短句出现的次数，word_list为基础粒度分词结果
    for word in word_list:
        if not word['str'].isdigit() and not len(word['str']) <= 1:  # 纯数字不计数，字符长度小于1不计数
            word_list_count[word['str']] += freq
    #print(word_list_count)
    return

def store_res_CSV(path,model):  # 将结果存入csv
    f_csv=open(path,model,encoding='utf8',newline='')
    f_writer=csv.writer(f_csv)
    if model == 'w':
        f_writer.writerow(['词语','频数'])
    for word in word_list_count:
        f_writer.writerow([word]+[word_list_count[word]])
    f_csv.close()
    print('写入成功！')
    return

if __name__=="__main__":
    upload_path="./report_sample _after250.txt" # 上传文本文件路径
    download_path="./" #结果储存路径
    # print(separate_sentence(upload_path))
    sentences=separate_sentence(upload_path)
    # for sentence in sentences:  #单句上传时
    #     #print(sentence)
    #     result = upload(sentence)
    #     wordlist_analysis(sentences[sentence],result["word_list"])
    #     time.sleep(1)
    sentences_key=list(sentences.keys())  #len(sentences_key)=712895
    count=0
    j=25
    for index in range(142000,len(sentences_key),100):  # 每次上传100句
        #print(sentences_key[index:index + 100])
        results = upload((sentences_key[index:index+100]),index)
        #print(results)
        i = 0
        count += 1
        if results:
            for result in results['res_list']:
                #print(sentences[result['norm_str']])
                wordlist_analysis(sentences[sentences_key[index+i]], result["word_list"])
                i += 1
            print("前", index + 100, "句完成统计!")
        else:
            print(index,"句出现问题！")
        if count == 10:
            j += 1
            count = 0
            store_res_CSV('./xls_result/'+'word_freq'+str(j)+'.csv','w')
            store_res_CSV(download_path + 'word_freq.csv', 'a')
            word_list_count = defaultdict(lambda: 0)
    # for index in range(0,len(texts),100):  #每100
    #     print(index)
    #     obj = {"str": texts[index:index+100]}
    #store_res_CSV(download_path+'word_freq.csv','w')