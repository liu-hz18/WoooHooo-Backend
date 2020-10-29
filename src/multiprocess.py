import threading
from Scratchtest import *
import pymongo
#url 形似https://new.qq.com/omn/date/dateA0+四位随机大写字母与数字序列+00.html
def loadDateNews(date,newsSet):
    baseUrl='https://new.qq.com/omn/'+date+'/'+date+'A0'
    tailUrl='00.html'
    count=0
    #with open(f"newsData/{date}.json", 'r', encoding='utf-8') as load_f:
        #strF = load_f.read()
        #if len(strF) > 0:
            #dateNews = json.loads(strF)
        #else:
            #dateNews = []
    #print(len(dateNews))
    elementList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in elementList:
        for j in elementList:
            dateNews = []
            for k in elementList:
                for l in elementList:
                    temp = i + j + k + l
                    url=baseUrl+temp+tailUrl
                    try:
                        dateNews.append(loadWithTime(url))
                        #print(dateNews[-1])
                        count=count+1
                    except:
                        continue
            print(date+":"+str(count))
            x = newsSet.insert_many(dateNews)
            #with open(f"newsData/{date}.json", 'w', encoding='utf-8') as json_file:
                #json.dump(dateNews, json_file, ensure_ascii=False)

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, date,newsSet):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.date = date
        self.newsSet=newsSet

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        loadDateNews(self.date,self.newsSet)


if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost/")
    mydb = myclient["StaticNews"]
    newsSet=mydb["news"]

    monthday=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
          '17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']

    # 创建新线程
    threads=[]
    for i in range(0,30):
        tempThread=myThread(i,f"202008{monthday[i]}",newsSet)
        tempThread.start()
        threads.append(tempThread)

    for tempThread in threads:
        tempThread.join()

