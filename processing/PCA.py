import pandas as pd
from sklearn.decomposition import PCA

# 利用基于SVD分解的PCA（主成分分析）进行数据降维

if __name__ == '__main__':
    data = pd.read_csv('CSV/bw_matrix.csv').values
    # svd_solver ='full' 该参数是指定SVD的计算方式的
    # 表示希望降维后的总解释性方差占比大于n_components指定的百分比，即是说，希望保留百分之多少的信息量。
    pca = PCA(n_components=0.97, svd_solver="full")
    pca.fit(data)

    print('降维后的特征向量所保留信息量的百分比：' + str(sum(pca.explained_variance_ratio_)))  # 0.9701178185590625
    print('特征维度从1000降维至：' + str(len(pca.explained_variance_ratio_)))  # 534
