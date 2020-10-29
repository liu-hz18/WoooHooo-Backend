import pymongo

if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost/")
    mydb = myclient["StaticNews"]
    newsSet = mydb["news"]
    allNews=newsSet.find()
    categoryList=[]
    for news in allNews:
        category=news['category']
        if category not in categoryList:
            categoryList.append(category)
    print(categoryList)
    categoryList.remove('')
    print(categoryList)
    print(mydb.list_collection_names())
    for news in newsSet.find():
        category=news['category']
        if category in categoryList:
            myCol=mydb[category]
            myCol.insert_one(news)
        else:
            continue
    print(mydb.list_collection_names())