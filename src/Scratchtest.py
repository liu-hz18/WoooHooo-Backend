import requests
import demjson
from bs4 import BeautifulSoup
import json

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30,allow_redirects=False)
        r.raise_for_status()
        return r.text
    except:
        return ""

# for links like https://news.qq.com/a/time/newsID.htm
def getContentwithA(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("div.hd > h1")
    time = soup.select("div.a_Info > span.a_time")
    paras = soup.select("div.Cnt-Main-Article-QQ > p.text")
    textcontent=""
    for para in paras:
        if len(para) > 0:
            textcontent+=para.get_text()
    temp = soup.find('script', {'type': 'text/javascript'}).contents[0].replace("\n", "").split("||")[-1]
    keywords=demjson.decode(temp.replace("\'", "\""))["tags"]
    #将爬取到的文章用字典格式来存
    article = {
        'Title' : title[0].get_text(),
        'Time' : time[0].get_text(),
        'Paragraph' : textcontent,
        'keywords':keywords,
        'catalog1':"unknown",
        'catalog2':"unknown"
    }
    print(article)

#for links like http://new.qq.com/omn/time/newsID.html
def getContentWithTime(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    paras = soup.select("div.content-article > p.one-p")
    images=soup.select("div.content-article >p.one-p> img.content-picture")
    imagesurl=[]
    for index in images:
        imagesurl.append(index.get('src'))
    textcontent = ""

    for para in paras:
        if len(para) > 0:
            textcontent += para.get_text().replace('\n',"")
    return textcontent,imagesurl

#for links like http://new.qq.com/omn/time/newsID.html
def loadWithTime(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("div.LEFT > h1")
    paras = soup.select("div.content-article > p.one-p")
    textcontent = ""
    for para in paras:
        if len(para) > 0:
            textcontent += para.get_text().replace('\n'," ")
    # 将爬取到的文章用字典格式来存
    temp = json.loads((soup.findAll('script')[5]).contents[0].split("=")[-1])
    time=temp["pubtime"]
    catalog=temp["catalog1"]
    source=temp['media']
    images = soup.select("div.content-article >p.one-p> img.content-picture")
    imagesurl = []
    for index in images:
        imagesurl.append(index.get('src'))
    top_image=""
    if len(images)!=0:
        top_image=images[0].get('src')
    article = {
        'url':url,
        'title': title[0].get_text(),
        'publish_time': time,
        'content': textcontent,
        'category': catalog,
        'source':source,
        'imageurl':imagesurl,
        'top_img':top_image
    }
    return article

#得到四位随机数序列的所有组合形式
def getRandomUrl():
    elementList=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J',
                 'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    randomList=[]
    for i in elementList:
        for j in elementList:
            for k in elementList:
                for l in elementList:
                    temp=i+j+k+l
                    randomList.append(temp)
    return randomList


