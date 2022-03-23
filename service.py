#  -*-  codeing  =  utf-8  -*-
#  @Time  :2022/3/8  17:03
#  @Author:旁观者
#  @File  :  service.py
#  @Software:  PyCharm
import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import db.db_mysql


def getWordData():
    data = db.db_mysql.select("introduce")
    text=""
    for item in data:
        text = text+item[0]
    cut = jieba.cut(text)
    string = ' '.join(cut)
    print(f"string_len={len(string)}")
    img = Image.open(r'.\static\picture\tree.jpg')
    img_array = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
    )
    wc.generate_from_text(string)
    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    plt.show()
    plt.savefig(r".\static\picture\tree-cn.jpg",dpi=600)

if __name__=="__main__":
    getWordData()