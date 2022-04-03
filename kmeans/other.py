from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

# 求x,y欧式距离
def dist(x, y):
    return np.linalg.norm(x - y, ord=2, axis=1)


# 初始化聚类中心
def init(data, k, seed):
    np.random.seed(seed)

    points = np.empty((k, data.shape[1]))
    # 随机先选1个
    rand = np.random.randint(low=0, high=len(data))
    print(rand)
    points[0] = data[rand]
    # 遍历选择
    for i in range(1, k):
        d = -np.Inf
        idx = None
        for j in range(len(data)):
            dis = np.mean(dist(points[:i], data[j]))
            if dis > d:
                d = dis
                idx = j
        points[i] = data[idx]
        print(idx)
    return points


def kmeans(data, k, seed):
    """
    初始聚类中心的选取: 首先随机选择一个点作为第一个初始类簇中心点，然后选择距离该点最远的那个点作为第二个初始类簇中心点，
    然后再选择距离前两个点的最近距离最大的点作为第三个初始类簇的中心点，以此类推，直至选出K个初始类簇中心点。
    """
    # 首先随机选取一个聚类中心
    points = init(data, k, seed)
    # 开始迭代
    while (True):
        res = [[] for i in range(k)]
        for i in range(len(data)):
            dis = dist(points, data[i])
            idx = np.argmin(dis)
            res[idx].append(i)
        # 修正聚类中心
        flag = 0
        for i in range(k):
            new_point = np.mean(data[res[i]], axis=0)
            if (points[i] - new_point == 0).all():
                flag += 1
            else:
                points[i] = new_point
        # 终止条件
        if flag == k:
            return res

if __name__ == '__main__':
    # 随机生成数据
    X, y = make_blobs(n_samples=500, n_features=2, centers=3, random_state=3)
    # 聚类结果
    res = kmeans(data=X, k=3, seed=6)

    plt.scatter(X[res[0], 0], X[res[0], 1], marker='o', s=16, c='r')
    plt.scatter(X[res[1], 0], X[res[1], 1], marker='o', s=16, c='b')
    plt.scatter(X[res[2], 0], X[res[2], 1], marker='o', s=16, c='g')
    plt.show()

