import numpy as np
import struct
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler  # 标准化工具
from sklearn.datasets import make_blobs


# 读取 minst 图片
def loadImage(filepath):
    # 以二进制形式打开
    file = open(filepath, 'rb').read()
    # 读取头信息, minst采用大端存储
    fmt = '>iiii'
    magic_num, image_num, rows, cols = struct.unpack_from(fmt, file, offset=0)

    image_size = rows * cols
    image = np.empty((image_num, image_size))

    fmt = '>' + str(image_size) + 'B'
    for i in range(image_num):
        offset = 16 + i * image_size
        image[i] = struct.unpack_from(fmt, file, offset)

    return image


# 读取 minst 标签
def loadLabel(filepath):
    # 以二进制形式打开
    file = open(filepath, 'rb').read()
    # 读取头信息, minst采用大端存储
    fmt = '>ii'
    magic_num, label_num = struct.unpack_from(fmt, file, offset=0)

    label = np.zeros((label_num, 1))

    fmt = '>B'
    for i in range(label_num):
        offset = 8 + i
        label[i] = struct.unpack_from(fmt, file, offset)

    return label


# 求x,y欧式距离
def dist(x, y):
    return np.linalg.norm(x - y, ord=2, axis=1)


# 初始化聚类中心
def init(data, k, seed):
    np.random.seed(seed)

    points = np.empty((k, data.shape[1]))
    # 随机先选1个
    rand = np.random.randint(low=0, high=len(data))
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
    test_image_path = './data/t10k-images.idx3-ubyte'
    train_image_path = './data/train-images.idx3-ubyte'

    test_image = loadImage(test_image_path)
    train_image = loadImage(train_image_path)

    # 聚类实验,不需要划分训练集和测试集
    images = np.concatenate((train_image, test_image), axis=0)
    # 随机选取1000组数据
    images = images[np.random.randint(low=0, high=len(images) + 1, size=1000)]

    # 数据标准化处理
    scaler = StandardScaler()
    scaler.fit(images)
    images = scaler.transform(images)

    # PCA 降维
    pca = PCA(n_components='mle')
    images_pca = pca.fit_transform(images)

    # kmeans聚类
    res = kmeans(images_pca, k=10, seed=1)

    # 数据反标准化
    images = scaler.inverse_transform(images)

    # 查看每一种聚类的随机5张图片
    size = 5
    for each in res:
        idx = np.random.randint(low=0, high=len(each) + 1, size=size)
        for i in range(size):
            plt.subplot(1, size, i + 1)
            plt.imshow(images[idx[i]].reshape((28, 28)))
        plt.show()
