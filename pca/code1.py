import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


def dataLoad(file_path, image_num, H, W, C):
    """
    读取图片数据，生成训练集和测试集
    :return: data: 返回数据 (H*W,N,C)
    :param file_path: 图片路径
    :param image_num: 图片数目
    :param H: 图片的高
    :param W: 图片的寛
    :param C: 图片的通道数目
    """
    data = np.zeros([H * W, image_num, C])
    # 读取所有文件下所有图片名
    files = os.listdir(file_path)
    # 对文件名重排序
    files.sort(key=lambda x: int(x[:-4]))
    print(files)
    for i in range(len(files)):
        # 读取所有图片
        image = Image.open(file_path + '/' + files[i])
        image = np.asarray(image)
        h, w, c = image.shape
        # 将图片降维成 (H*W,C)
        image.resize((h * w, c))
        data[:, i, :] = image

    return data


def preprocess(data):
    """
    对数据进行标准化处理，所有通道都处理
    :param data: 原始数据 (36000,20,3)
    :return: 标准化后数据
    """
    # 获取通道数
    c = data.shape[2]
    pre_data = np.zeros(data.shape)
    for i in range(c):
        # 计算均值
        m = np.mean(data[:, :, i], axis=1, keepdims=True)
        # 计算标准差
        v = np.std(data[:, :, i], axis=1, keepdims=True)
        # 进行标准化处理
        pre_data[:, :, i] = (data[:, :, i] - m) / v
    return pre_data


def covMatrix(data):
    """
    计算协方差矩阵
    :return: 返回协方差矩阵 (20,20)
    :param data: 标准化后数据 (36000,20)
    """
    data = np.matrix(data)
    return np.asarray(data * data.T)


def eig(covmatrix):
    """
    计算协方差矩阵的特征值的特征向量
    :param covmatrix: 协方差矩阵 (20,20)
    :return: 返回特征值和特征向量
    """
    eigenvalues, eigenvactors = np.linalg.eig(covmatrix)
    return eigenvalues, eigenvactors


def selectEigvalues(contribute, eigenvalues, eigenvactors):
    """
    根据预设贡献度，选择k个特征值和特征向量
    :param contribute: 贡献度
    :param eigenvalues: 特征值
    :param eigenvactors: 特征向量
    :return:
    """
    total = sum(eigenvalues)
    selectvalues = []
    selectvactors = []

    # 先对特征值和特征向量排序
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvactors = eigenvactors.T[idx]

    i = 0
    while contribute > 0:
        contribute -= eigenvalues[i] / total
        selectvalues.append(eigenvalues[i])
        selectvactors.append(eigenvactors[i])
        i += 1

    selectvalues = np.asarray(selectvalues)
    selectvactors = np.asarray(selectvactors)

    return selectvalues, selectvactors.T


def eigenFace(data, selectvactors, show=False):
    """
    # 获取特征脸
    :param data: 原始数据
    :param selectvactors: 选择特征向量
    :param show: 是否展示
    """
    eigenface = np.matmul(data, selectvactors)

    if show:
        r, c = eigenface.shape
        face = eigenface.reshape([200, 180, c])
        for i in range(c):
            plt.subplot(c // 4 + 1, 4, i + 1)
            plt.imshow(face[:, :, i])
        plt.show()

    return eigenface


def matchImage(train, test):
    """
    对测试样本进行匹配，看和那个训练样本是同一类
    :param train: 训练样本（映射后）
    :param test: 测试样本（映射后）
    :return: 计算结果 (20,10)
    """
    train_num = len(train)
    test_num = len(test)
    res = np.zeros((train_num, test_num))

    for i in range(test_num):
        for j in range(train_num):
            res[j, i] = np.sqrt(np.sum((test[i] - train[j]) ** 2))

    return res


def imageCompare(train_image, test_image, res):
    """
    对结果可视化展示
    :param train_image: 原始训练集
    :param test_image: 原始测试集
    :param res: 计算距离结果
    """
    test_num = test_image.shape[1]

    category = np.argmin(res, axis=0)
    print(category)

    fig, ax = plt.subplots(2, test_num)
    for i in range(test_num):
        image1 = test_image[:, i, :].reshape([200, 180, 3])
        image2 = train_image[:, category[i], :].reshape([200, 180, 3])
        ax[0, i].imshow(image1 / 255)
        ax[0, i].set_title('测试样本：{}.jpg'.format(i + 1))
        ax[1, i].imshow(image2 / 255)
        ax[1, i].set_title('训练样本：{}.jpg'.format(category[i] + 1))
    plt.show()


def main():
    train_data = dataLoad(file_path='./data/TrainDatabase', image_num=20, H=200, W=180, C=3)
    test_data = dataLoad(file_path='./data/TestDatabase', image_num=10, H=200, W=180, C=3)

    # 对训练数据进行标准化处理
    train_data_pre = preprocess(train_data)
    test_data_pre = preprocess(test_data)

    # 选择 channel_1
    train_data_pre = train_data_pre[:, :, 2]
    test_data_pre = test_data_pre[:, :, 2]

    # 计算协方差矩阵
    covmatrix = covMatrix(train_data_pre.T)
    # 计算特征值和特征矩阵
    eigenvalues, eigenvactors = eig(covmatrix)
    # 对特征值和特征矩阵进行选择
    selectvalues, selectvactors = selectEigvalues(0.85, eigenvalues, eigenvactors)
    # 生成特征脸（特征向量）
    eigenface = eigenFace(train_data_pre, selectvactors, show=True)

    # 将样本集投影到子空间中
    project_train = np.matmul(train_data_pre.T, eigenface)
    project_test = np.matmul(test_data_pre.T, eigenface)

    # 计算训练样本与测试样本间欧氏距离
    res = matchImage(project_train, project_test)

    # 可视化展现
    imageCompare(train_data, test_data, res)


if __name__ == '__main__':
    main()
