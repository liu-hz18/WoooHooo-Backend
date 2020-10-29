import json
import pymongo

count=0
date=[]
monthday=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
for i in range(0,30):
    date.append(f"202008{monthday[i]}")
totalNews=[]
myclient = pymongo.MongoClient("mongodb://localhost/")
mydb = myclient["StaticNews"]
newsSet=mydb["news"]
for index in date:
    try:
        dateNews=[]
        with open(f"newsData/{index}.json", 'r', encoding='utf-8') as load_f:
            strF = load_f.read()
            if len(strF) > 0:
                dateNews = json.loads(strF)
            else:
                dateNews = []
        count=count+len(dateNews)
        totalNews=totalNews+dateNews
        x = newsSet.insert_many(dateNews)
    except:
        continue

print(count)
