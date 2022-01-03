import pickle
import time

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.svm import SVC

# SVM训练分类器模型


if __name__ == '__main__':
    # 根据PCA降维，仅需要534特征词即可代表绝大多数数据特征
    df_fake = pd.read_csv('../processing/CSV/bw_matrix.csv', usecols=[i for i in range(534)])
    df_normal = pd.read_csv('../processing/CSV/bw_matrix_normal.csv', usecols=[i for i in range(534)])
    # 前2000条虚假微博和前1000条正常微博进行训练
    df_train = pd.concat([df_fake.loc[:1999], df_normal.loc[:999]], axis=0, ignore_index=True)
    # 剩余的所有虚假微博和另外的500条正常微博进行测试
    df_test = pd.concat([df_fake.loc[2000:], df_normal[1000:1500]], axis=0, ignore_index=True)
    print(df_train.info())
    # 2000个虚假信息，1000个真实信息
    class_arr = np.array([0 for i in range(2000)] + [1 for i in range(1000)])
    print(class_arr)

    model = SVC(kernel='rbf', C=6, gamma=0.001)
    start = time.time()
    model.fit(df_train, class_arr)
    end = time.time()
    print('Train time: %s Seconds' % (end - start))
    start = time.time()
    pre = model.predict(df_test)
    end = time.time()
    print('Test time: %s Seconds' % (end - start))
    # print(len(pre))
    # print(pre)

    # 测试集信息
    right_arr = np.array([0 for i in range(len(df_fake.loc[2000:]))] + [1 for i in range(len(df_normal[1000:1500]))])

    # 计算准确率（accuracy）
    accuracy = metrics.accuracy_score(right_arr, pre)
    print("准确率为：\n", accuracy)
    # 计算精确率（precision）
    precision = metrics.precision_score(right_arr, pre, average=None)
    print("精确率为：\n", precision)
    print('均值{:.4f}\n'.format(sum(precision) / 10))
    # 计算召回率（recall）
    recall = metrics.recall_score(right_arr, pre, average=None)
    print("召回率为：\n", recall)
    print('均值{:.4f}\n'.format(sum(recall) / 10))
    # 计算F1-score（F1-score）
    F1_score = metrics.f1_score(right_arr, pre, average=None)
    print("F1值为：\n", F1_score)

    cp = metrics.classification_report(right_arr, pre)
    print("-" * 25 + "分类报告" + "-" * 25 + "\n", cp)
