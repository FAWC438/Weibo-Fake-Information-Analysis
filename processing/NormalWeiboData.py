import re

import jieba.analyse
import jieba.posseg as ps
import numpy as np
import pandas as pd

# 处理正常微博数据，以便后续训练

with open('stop_words_ch.txt', 'r') as file:
    stop_words = [i.strip() for i in file.readlines()]
with open('stop_sign.txt', 'r', encoding='utf-8') as file:
    stop_sign = [i.strip() for i in file.readlines()]
with open('covid_19_word.txt', 'r', encoding='utf-8') as file:
    covid19_words = [i.strip() for i in file.readlines()]


def is_stop_word(word_str: str):
    """
    判断是否是停用词
    :param word_str:欲判断的词汇
    :return: 是为True，反之为False
    """
    if word_str in stop_words:
        return True
    for i in word_str:
        if i in stop_sign:
            return True
    return False


def get_noun_word(s: str):
    """
    利用jieba分词，提取微博内容中的名词和动词
    :param s:微博内容
    :return:仅包含名词的文本(空格间隔，下同)，仅包含动词的文本，仅包含名词的去重文本，仅包含动词的去重文本，人名，地名，机构名，疫情相关
    """
    res_n = []
    res_v = []
    res_per = []
    res_loc = []
    res_org = []
    covid19_correlation = 0
    words = ps.cut(s, use_paddle=True)
    for word, flag in words:
        # print('%s %s' % (word, flag))
        # 若为名词且不在停用词表中，则加入写入串
        if not is_stop_word(word):
            # 如果一条微博中有重复词语，保留不去重数据，因为仅仅几千条微博的数据量，这么做会影响后续该词的权重
            if not covid19_correlation and word in covid19_words:
                covid19_correlation = 1

            if flag == 'n':
                # 普通名词
                res_n.append(word)
            elif flag == 'v':
                # 动词
                res_v.append(word)
            elif flag == 'nr':
                # 人名
                res_per.append(word)
            elif flag == 'ns':
                # 地名
                res_loc.append(word)
            elif flag == 'nt':
                # 机构名
                res_org.append(word)

    return [' '.join(res_n), ' '.join(res_v), ' '.join(list(set(res_n))), ' '.join(list(set(res_v))),
            ' '.join(list(set(res_per))), ' '.join(list(set(res_loc))), ' '.join(list(set(res_org))),
            covid19_correlation]


def chinese_word_only(s: str):
    """
    将字符串处理为仅保留中文字符
    :param s:目标字符串
    :return:一个2个元素的列表，第一个元素是仅中文字符串，第二个元素是其长度
    """
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    res = re.sub(pattern, '', s)
    return [res, len(res)]


if __name__ == '__main__':
    jieba.enable_paddle()  # 启动paddle模式
    df = pd.read_csv('../spider/CSV/weibo_data_contrast.csv', usecols=[1])
    for i in range(len(df)):
        print('正在处理第' + str(i) + '行数据...')
        content = df.loc[i, 'content']
        if not isinstance(content, str):
            continue
        cn_res = chinese_word_only(content)
        if cn_res[1] > 0 and cn_res[1] is not None:
            jieba_res = get_noun_word(cn_res[0])
            df.loc[i, 'content'] = ' '.join([jieba_res[0], jieba_res[1], jieba_res[4], jieba_res[5], jieba_res[6]])
        else:
            df.loc[i, 'content'] = np.nan
    df.drop(df[(df['content'].isnull()) | (df['content'].isna())].index, inplace=True)  # 删除不合格的数据
    df.reset_index()
    df.to_csv('CSV/weibo_normal_data_clean.csv', index=False)
