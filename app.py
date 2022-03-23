from flask import Flask, render_template, jsonify,request
import db.connect_db

app = Flask(__name__)


@app.route('/')
def welcome():  # put application's code here
    return index()


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/book')
def book():
    page_id = int(request.args.get("page_id"))
    rows = int(request.args.get("rows"))
    total = db.db_mysql.selectCount()
    pageTotal = total // rows
    if total % rows != 0:
        pageTotal = pageTotal + 1
    if page_id > pageTotal:
        return render_template("book.html",errMsg="页码超出最大页数，请重新选择页码，点击关闭按钮返回第一页！")
    elif page_id <= 0:
        return render_template("book.html", errMsg="页码必须是正整数，请重新选择页码，点击关闭按钮返回第一页！")
    bookList = db.db_mysql.selectPage(page_id, rows)
    return render_template('book.html', bookList=bookList, pageId=page_id,pageTotal=pageTotal)


@app.route('/statistics')
def statistics():
    return render_template("statistics.html")


@app.route('/getAllBooks')
def getAllBooks():
    typeList = db.db_mysql.select("type")
    dataList = []
    for type in typeList:
        data = {"name":type[0],"value": db.db_mysql.selectAttributeCount("type",type[0])}
        dataList.append(data)

    return jsonify(dataList)


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return render_template("team.html")


@app.errorhandler(404)
def miss(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def error(e):
    return render_template('404.html'),500


if __name__ == '__main__':
    app.run(debug=True)
