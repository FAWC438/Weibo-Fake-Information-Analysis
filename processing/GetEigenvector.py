from collections import Counter

import jieba.analyse
import pandas as pd
import numpy as np

# 处理加权词频，取得特征向量，构成词袋矩阵

if __name__ == '__main__':
    df_data = pd.read_csv('CSV/weibo_data_clean.csv')
    df_weibo_data = pd.DataFrame({'time': df_data['time'],
                                  'data': df_data['content_n']}, columns=['time', 'data'])
    df_weibo_data['data'] = df_data['content_n'].fillna('') + ' ' + df_data['content_v'].fillna('') + ' ' + df_data[
        'PER'].fillna(
        '') + ' ' + df_data['LOC'].fillna('') + ' ' + df_data['ORG'].fillna('')
    df_weibo_data.to_csv('CSV/weibo_data_all_words.csv', index=False)  # 该csv输出每个微博所有词汇
    print(df_weibo_data.info())
    v = df_weibo_data.loc[:, ['data']].apply(lambda x: x.sum()).tolist()[0].strip()

    # 方法1，传统词频
    counter_obj = Counter(v.split())
    v_dict = dict(counter_obj)
    # print(counter_obj)
    df_res = pd.DataFrame(v_dict, index=['num']).T
    print(df_res.columns)
    df_res.sort_values("num", inplace=True, ascending=False)
    print(df_res.info())
    df_res.to_csv('CSV/tf_vector.csv')  # 该csv表示所有数据的词频向量

    # 方法2，jieba的tf-idf分析，找到权重最大的前1000个词
    tags = jieba.analyse.extract_tags(v, topK=1000, withWeight=True)
    tags_dic = dict(tags)
    # for tag, value in tags_dic.items():
    #     print("tag: %s\t\t weight: %f" % (tag, value))
    df_key_words = pd.DataFrame({'tag': tags_dic.keys(), 'weight': tags_dic.values()})
    print(df_key_words.info())
    df_key_words.to_csv('CSV/tf_idf_weight.csv', index=False)

    # TODO:稀疏矩阵
    bw_matrix = np.zeros(shape=(len(df_weibo_data), len(df_key_words)))
    key_words = list(tags_dic.keys())
    for i in range(len(df_weibo_data)):
        # 遍历所有文章
        word_list = df_weibo_data.loc[i, 'data'].split()  # 取得文章内容
        for w in word_list:
            # 判断文章每个词是否在1000个关键字里
            if w not in key_words:
                continue
            else:
                # 若为关键字，则矩阵相应位置加一
                bw_matrix[i][key_words.index(w)] += 1

    bw_matrix_df = pd.DataFrame(data=bw_matrix, columns=key_words)
    bw_matrix_df.to_csv('CSV/bw_matrix.csv', index=False)  # 该csv即基于TF-IDF加权的词袋模型矩阵
