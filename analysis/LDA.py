from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd

# 利用LDA主题模型进行数据聚类，将微博数据分为3类较为合理，通过语义分析得出以下结论：
# 第一类为社会类，谣言包括时政、国际、警匪冲突等方面；
# 第二类为生活类，谣言包括平时生活中的小知识和娱乐明星等；
# 第三类为事故类，明显的特征是该类谣言绝大多数都和人的生命安全有关。

if __name__ == '__main__':
    df_data = pd.read_csv('../processing/CSV/weibo_data_all_words.csv')
    cntVector = CountVectorizer()
    # 为了配合使用sklearn库，此处采用sklearn提供的词向量词袋模型
    cntTf = cntVector.fit_transform(df_data['data'])
    print('Vector done!')
    class_num = 3  # 最关键的参数，该参数即分类数量
    # max_iter ：EM算法的最大迭代次数。
    #  learning_method: 即LDA的求解算法。有 ‘batch’ 和 ‘online’两种选择。前者较为简单快速，后者较为复杂、参数较多。
    lda = LatentDirichletAllocation(n_components=class_num, max_iter=5, learning_method='batch', random_state=0)
    doc = lda.fit_transform(cntTf)
    print(doc)  # 文档的主题模型分布在doc中，即表示每篇文档属于哪一类
    # print(len(doc))
    print('-' * 30)
    print(lda.components_)  # 主题词分布在lda.components_中
    # print(len(lda.components_))
    # print(len(lda.components_[0]))

    doc_class = []  # 该列表指示了每篇文章属于哪个类别
    for i in doc:
        class_list = list(i)
        doc_class.append(class_list.index(max(class_list)))
    print(doc_class)
    df_data_classified = pd.read_csv('../processing/CSV/weibo_data_clean.csv')
    columns_list = ['content', 'content_n', 'content_v', 'PER', 'LOC', 'ORG', 'content_n_set', 'content_v_set', 'time',
                    'forward', 'comment', 'like', 'VIP', 'link', 'words', 'covid19', 'class']
    df_data_classified = df_data_classified.reindex(columns=columns_list)
    df_data_classified['class'] = doc_class
    df_data_classified.to_csv('CSV/weibo_data_classified.csv', index=False)

    df_class = [pd.DataFrame({'time': [], 'data': []}) for i in range(class_num)]
    for i in range(len(doc_class)):
        df_class[doc_class[i]] = df_class[doc_class[i]].append(
            pd.DataFrame({'time': [df_data.loc[i, 'time']], 'data': [df_data.loc[i, 'data']]}))
    print('写入csv...')
    for i in range(class_num):
        df_class[i].to_csv('CSV/weibo_class_' + str(i) + '.csv', index=False)
    print('完成！')
