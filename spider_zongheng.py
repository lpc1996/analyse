#  -*-  codeing  =  utf-8  -*-
#  @Time  :2022/1/29  12:17
#  @Author:旁观者
#  @File  :  spider_zongheng.py
#  @Software:  PyCharm
import urllib.request,urllib.error
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import db

def main():
    getData()


#小说链接
findLink = re.compile(r'<a href="(.*?)" target')
#图片链接
findImgSrc = re.compile(r'<img alt=".*" src="(.*?)"')
#小说名字
findName = re.compile(r'<img alt="(.*)" src')
#截取整个booklink块
findBookLink = re.compile(r'<div class="bookilnk">((?:.|\n)*?)</div>')
#作者
findAuthor = re.compile(r'<a href=".*" target="_blank">(.*?)</a>(?:.|\n)*?<a',re.S)
#类别
findType = re.compile(r'<a href=".*" target="_blank">(.*?)</a>')
#小说状态
findStatus = re.compile(r'<span>\\r\\n                            \\t\\r\\n                            \\t(.*?)\\r\\n                            \\r\\n                        \\t</span>')
#更新时间
findTime = re.compile(r'<span>(.*?)</span>',re.S)
#简介
findItroduce = re.compile(r'<div class="bookintro">(.*?)</div>',re.S)
#最新章节
findUpdate = re.compile(r'<div class="bookupdate">((?:.|\n)*?)</div>')
findUpdateText = re.compile(r'<a class="fl" href=".*">最新章节：(.*?)</a>')
def getData():
    for i in range(1,363):
        bookList=[]
        url = "http://book.zongheng.com/store/c0/c0/b0/u0/p"+str(i)+"/v9/s9/t0/u0/i1/ALL.html"
        # http://book.zongheng.com/store/c0/c0/b1/u0/p1/v9/s9/t0/u0/i1/ALL.html
        # url = "http://book.zongheng.com/store/c0/c0/b1/u0/p"+str(i)+"/v9/s9/t0/u0/i1/ALL.html"
        html = askUrl(url)
        soup = BeautifulSoup(html, "html.parser")
        for bookBox in soup.find_all("div",class_="bookbox"):
            bookBoxStr = str(bookBox)
            book=[]
            link = re.findall(findLink,bookBoxStr)
            book.append(link[0])
            imgSrc = re.findall(findImgSrc,bookBoxStr)
            book.append(imgSrc[0])
            bookName = re.findall(findName,bookBoxStr)
            book.append(bookName[0])
            bookLink = re.findall(findBookLink,bookBoxStr)
            bookLink = str(bookLink)
            # print(bookLink)
            author = re.search(findAuthor,bookLink)
            author = author[0].split(">")[1]
            author = author.split("<")[0]
            book.append(author)
            type = re.findall(findType,bookLink)
            book.append(type[0])
            bookStatus = re.findall(findStatus,bookLink)
            bookTime = re.findall(findTime,bookLink)
            if len(bookStatus) > 0:
                book.append(bookStatus[0])
            else:
                book.append(" ")
            bookTime = re.findall(re.compile(r'\\r\\n                            更新时间\\xa0\\xa0(.*?)\\r\\n                            '),bookTime[1])
            book.append(bookTime[0])
            itroduce = re.findall(findItroduce,bookBoxStr)[0]
            itroduce = str(itroduce)
            itroduce = itroduce.replace("\n","")
            itroduce = itroduce.replace(" ","")
            book.append(itroduce)
            update = re.findall(findUpdate,bookBoxStr)[0]
            updateText = re.findall(findUpdateText,str(update))
            if len(updateText) == 0:
                updateText = " "
            else:
                updateText = updateText[0]
            book.append(updateText)
            # print(update)
            bookList.append(tuple(book))

        print(db.db_mysql.insertBooks(bookList=bookList))


def printBook(bookList):
    for book in bookList:
        print(book)

def askUrl(url):
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "Accept-Language":"zh-CN,zh;q=0.9"
    }
    print(url)
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("UTF-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        exit(10)
    return html


if __name__=="__main__":
    main()


