import os
import re
import csv
import pandas as pd
import pymysql
from tkinter import messagebox

# 系统打开pskSpider文件夹运行爬虫
os.system("cd pksSpider && scrapy crawl pks")
# 爬虫.txt 存入
with open('D:\研究生\课程\网络内容信息安全\爬虫\pksSpider\pksSpider\爬虫.txt')as f:
    item = f.read()

print(item)
# 通过正则匹配找到title author poc信息
ptitle = re.compile(r'Title": (.*?), "author"')
pauthor = re.compile(r'"Author": "(.*?)", "date"')
ppoc = re.compile(r'"Poc":(.*?)"author"')

title = ptitle.findall(item)
author = pauthor.findall(item)
poc = ppoc.findall(item)

r = zip(title, author, poc)
header = ['title', 'author', 'poc']
# 写入csv文件中
with open('Result.csv', 'w', encoding='utf-8', newline='') as file_obj:
    writer = csv.writer(file_obj)
    writer.writerow(header)
    for i in r:
        writer.writerow(i)
# 连接数据库
connection = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='spider')
cursor = connection.cursor()

try:
    cursor.execute("CREATE TABLE spider_result"
                   "( title CHAR(255) ,"
                   "  author CHAR(255) , "
                   "  poc CHAR(255)"
                   ");")
    # 创建表
    connection.commit()
except:
    messagebox.showinfo("提示", "数据库已创建")


# 获取当前文件地址
myAddress = os.getcwd()
csvFilePath = '' + myAddress + '\\Result.csv'

# 读取csv文件并插入数据库
df = pd.read_csv(csvFilePath)
for index, row in df.iterrows():
    date_str = row['title']
    avg = row['author']
    poc = row['poc']
    sql = f"INSERT INTO spider_result (title,author,poc) VALUES ('{date_str}', '{avg}','{poc}')"
    cursor.execute(sql)
connection.commit()
