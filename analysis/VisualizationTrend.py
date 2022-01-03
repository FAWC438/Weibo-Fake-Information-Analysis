import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 数据可视化
# 目标一： 所有类别的不实信息随时间变化（2016-2021）的热度
# 以年为单位展示各个类别微博数据变化量
# 目标二： 词云，基于词频/TF-IDF加权两种
# 目标三： 转发和点赞之间的散点图、相关性（相关系数）

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

if __name__ == '__main__':
    class_data = [[] for i in range(3)]
    for i in range(3):
        df = pd.read_csv('CSV/weibo_class_' + str(i) + '.csv')
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time')
        # print(df_class_0.info())
        year_count = df['time'].dt.year.value_counts()
        for j in range(2016, 2022):
            class_data[i].append(year_count[j])
    print(class_data)

    fig, ax = plt.subplots()

    ax.plot(np.arange(6), class_data[0], marker='o')
    # for j in range(6):
    #     ax.text(j, class_data[0][j] - 20, '{:.0f}'.format(class_data[0][j]), size=13)

    ax.plot(np.arange(6), class_data[1], marker='o')
    # for j in range(6):
    #     ax.text(j, class_data[1][j] - 20, '{:.0f}'.format(class_data[1][j]), size=13)

    ax.plot(np.arange(6), class_data[2], marker='o', color='r')
    # for j in range(6):
    #     ax.text(j, class_data[2][j] - 20, '{:.0f}'.format(class_data[2][j]), size=13)
    # for i in range(2016, 2022):
    #     data_class_0.append(len(df_class_0[str(i)]))
    # print(data_class_0)
    ax.legend(['社会类', '生活类', '事故类'])
    ax.set_xticks([i for i in range(6)])
    ax.set_xticklabels([str(i) + '年' for i in range(2016, 2022)])
    ax.set_xlabel('年份')
    ax.set_ylabel('微博数据量')
    ax.set_title('2016年至2021年不同类型谣言微博热度变化')

    plt.savefig('IMG/2016年至2021年不同类型谣言微博热度变化.png')
    plt.show()
