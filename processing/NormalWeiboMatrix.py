import numpy as np
import pandas as pd

if __name__ == '__main__':
    parm = 534  # PCA降维后得到的数据
    df = pd.read_csv('CSV/weibo_normal_data_clean.csv')
    df_key_words = pd.read_csv('CSV/tf_idf_weight.csv')
    key_words = df_key_words.loc[:parm - 1]['tag']
    bw_matrix_normal = np.zeros(shape=(len(df), parm))

    # print(key_words)
    for i in range(len(df)):
        # 遍历所有文章
        word_list = df.loc[i, 'content'].split()  # 取得文章内容
        print(word_list)

        for w in word_list:
            # 判断文章每个词是否在1000个关键字里
            if w not in key_words:
                continue
            else:
                # 若为关键字，则矩阵相应位置加一
                bw_matrix_normal[i][key_words.index(w)] += 1

    bw_matrix_df = pd.DataFrame(data=bw_matrix_normal, columns=key_words)
    bw_matrix_df.to_csv('CSV/bw_matrix_normal.csv', index=False)  # 该csv即基于TF-IDF加权的词袋模型矩阵
