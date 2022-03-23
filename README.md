- 项目使用mysql数据库存储数据，首先建立数据库spider、然后在spider数据库中运行
db文件夹下的zongheng.sql文件,然后修改db/db_mysql.py文件里的数据库连接参数，
将用户名和密码修改成自己的。
- 首先运行spider_zongheng.py文件爬取纵横中文网的书库数据到数据库中，然后运行
app.py文件启动工程，然后点击控制台打印的连接即可打开web页面。