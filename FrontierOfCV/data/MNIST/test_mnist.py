"""
MNIST 数据集读取示例程序
官方提供的标准读取方法
"""

import numpy as np
import struct
from array import array
from os.path import join
import matplotlib.pyplot as plt
import random


class MnistDataloader:
    """
    MNIST 数据加载器
    用于读取 MNIST 手写数字数据集的二进制文件
    """

    def __init__(self, training_images_filepath, training_labels_filepath,
                 test_images_filepath, test_labels_filepath):
        """
        初始化数据加载器

        Args:
            training_images_filepath: 训练集图片文件路径
            training_labels_filepath: 训练集标签文件路径
            test_images_filepath: 测试集图片文件路径
            test_labels_filepath: 测试集标签文件路径
        """
        self.training_images_filepath = training_images_filepath
        self.training_labels_filepath = training_labels_filepath
        self.test_images_filepath = test_images_filepath
        self.test_labels_filepath = test_labels_filepath

    def read_images_labels(self, images_filepath, labels_filepath):
        """
        读取图片和标签文件

        MNIST 文件格式:
        - 标签文件: [magic_number(4 bytes)] [number_of_items(4 bytes)] [label(1 byte each)]
        - 图片文件: [magic_number(4 bytes)] [number_of_items(4 bytes)]
                   [rows(4 bytes)] [cols(4 bytes)] [pixel(1 byte each)]

        magic_number:
        - 标签文件: 2049 (0x00000801)
        - 图片文件: 2051 (0x00000803)
        """
        # 读取标签
        labels = []
        with open(labels_filepath, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError(f'Magic number mismatch, expected 2049, got {magic}')
            labels = array("B", file.read())

        # 读取图片
        with open(images_filepath, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError(f'Magic number mismatch, expected 2051, got {magic}')
            image_data = array("B", file.read())

        # 将像素数据转换为 28x28 的图片
        images = []
        for i in range(size):
            images.append([0] * rows * cols)
        for i in range(size):
            img = np.array(image_data[i * rows * cols:(i + 1) * rows * cols])
            img = img.reshape(28, 28)
            images[i][:] = img

        return images, labels

    def load_data(self):
        """
        加载训练和测试数据

        Returns:
            (x_train, y_train), (x_test, y_test): 训练集和测试集
        """
        x_train, y_train = self.read_images_labels(self.training_images_filepath,
                                                   self.training_labels_filepath)
        x_test, y_test = self.read_images_labels(self.test_images_filepath,
                                                 self.test_labels_filepath)
        return (x_train, y_train), (x_test, y_test)


def show_images(images, title_texts):
    """
    显示图片列表

    Args:
        images: 图片列表
        title_texts: 每个图片的标题
    """
    cols = 5
    rows = int(len(images) / cols) + 1
    plt.figure(figsize=(30, 20))
    index = 1
    for x in zip(images, title_texts):
        image = x[0]
        title_text = x[1]
        plt.subplot(rows, cols, index)
        plt.imshow(image, cmap=plt.cm.gray)
        if title_text != '':
            plt.title(title_text, fontsize=15)
        index += 1
    plt.tight_layout()
    plt.savefig('./MultilayerPerceptron/mnist_samples.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("图片已保存到 MultilayerPerceptron/mnist_samples.png")


def main():
    """主函数：加载并显示 MNIST 数据样本"""
    import os

    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, 'archive')

    # 设置文件路径
    training_images_filepath = join(input_path, 'train-images.idx3-ubyte')
    training_labels_filepath = join(input_path, 'train-labels.idx1-ubyte')
    test_images_filepath = join(input_path, 't10k-images.idx3-ubyte')
    test_labels_filepath = join(input_path, 't10k-labels.idx1-ubyte')

    # 加载数据
    print("正在加载 MNIST 数据集...")
    mnist_dataloader = MnistDataloader(training_images_filepath,
                                       training_labels_filepath,
                                       test_images_filepath,
                                       test_labels_filepath)
    (x_train, y_train), (x_test, y_test) = mnist_dataloader.load_data()

    print(f"训练集: {len(x_train)} 张图片")
    print(f"测试集: {len(x_test)} 张图片")

    # 随机选择样本显示
    images_2_show = []
    titles_2_show = []

    # 10 张训练集样本
    for i in range(10):
        r = random.randint(1, 60000)
        images_2_show.append(x_train[r])
        titles_2_show.append(f'training [{r}] = {y_train[r]}')

    # 5 张测试集样本
    for i in range(5):
        r = random.randint(1, 10000)
        images_2_show.append(x_test[r])
        titles_2_show.append(f'test [{r}] = {y_test[r]}')

    show_images(images_2_show, titles_2_show)
    print("MNIST 数据集读取测试完成!")


if __name__ == '__main__':
    main()
