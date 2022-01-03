import matplotlib.pyplot as plt
import wordcloud  # 词云展示库
from collections import Counter
import numpy as np
import pandas as pd

# 数据可视化
# 目标二： 词云，基于词频数据

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
# plt.style.use('Solarize_Light2')


if __name__ == '__main__':
    word_data = []
    df = pd.read_csv('../processing/CSV/weibo_data_all_words.csv')
    str_data = df.loc[:, ['data']].apply(lambda x: x.sum()).tolist()[0].strip()
    word_data.append(Counter(str_data.split()))

    for i in range(3):
        df = pd.read_csv('CSV/weibo_class_' + str(i) + '.csv')
        str_data = df.loc[:, ['data']].apply(lambda x: x.sum()).tolist()[0].strip()
        word_data.append(Counter(str_data.split()))

    wc = wordcloud.WordCloud(
        scale=16,  # 内容分辨率
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
        background_color="white",
        max_words=200,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )

    print('正在绘制...')
    wc.generate_from_frequencies(word_data[0])
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.subplots_adjust(top=0.99, bottom=0.01, right=0.99, left=0.01, hspace=0, wspace=0)  # 调整边框
    plt.savefig('IMG/2016年至2021年谣言微博高频词云.png')
    print('完成第一张')

    wc.generate_from_frequencies(word_data[1])
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.subplots_adjust(top=0.99, bottom=0.01, right=0.99, left=0.01, hspace=0, wspace=0)  # 调整边框
    plt.savefig('IMG/2016年至2021年社会类谣言微博高频词云.png')
    print('完成第二张')

    wc.generate_from_frequencies(word_data[2])
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.subplots_adjust(top=0.99, bottom=0.01, right=0.99, left=0.01, hspace=0, wspace=0)  # 调整边框
    plt.savefig('IMG/2016年至2021年生活类谣言微博高频词云.png')
    print('完成第三张')

    wc.generate_from_frequencies(word_data[3])
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.subplots_adjust(top=0.99, bottom=0.01, right=0.99, left=0.01, hspace=0, wspace=0)  # 调整边框
    plt.savefig('IMG/2016年至2021年事故类谣言微博高频词云.png')
    print('完成第四张')
    # plt.show()  # 显示图像
