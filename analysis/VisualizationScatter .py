import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 数据可视化
# 目标三： 转发和点赞之间的散点图、相关性（相关系数）

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

if __name__ == '__main__':
    df = pd.read_csv('CSV/weibo_data_classified.csv')
    # 排除极端数据影响
    df.drop(df[(df['like'] == -1.0) | (df['like'] > 5000) | (df['forward'] < 20) | (df['forward'] > 2500)].index,
            inplace=True)
    like_data = df['like']
    forward_data = df['forward']
    print(len(df))

    # 线性拟合
    x_mean = np.mean(forward_data)
    y_mean = np.mean(like_data)
    m1 = 0  # 分母
    m2 = 0  # 分子
    for x_i, y_i in zip(forward_data, like_data):
        m1 += (x_i - x_mean) * (y_i - y_mean)
        m2 += (x_i - x_mean) ** 2
    a = m1 / m2
    b = y_mean - a * x_mean
    print(a, b)

    y_line = a * forward_data + b
    plt.scatter(forward_data, like_data)
    plt.plot(forward_data, y_line, color='orange')
    plt.text(1600, 3900, 'y = ' + '{:.4f}'.format(a) + ' * x + ' + '{:.4f}'.format(b), weight='bold')
    plt.axis([0, 2500, 0, 5000])
    plt.xlabel('转发数')
    plt.ylabel('点赞数')
    plt.title('2016年至2021年谣言微博转发与点赞数据关系')
    plt.savefig('IMG/2016年至2021年谣言微博转发与点赞数据关系.png')
    plt.show()
