import sys
import tensorflow as tf

# 使用 MNIST 手写数据集
mnist = tf.keras.datasets.mnist

# 准备训练数据,分为训练集和测试集
(x_train, y_train), (x_test, y_test) = mnist.load_data()
#  数据值规范化为范围 [0, 1]。
x_train, x_test = x_train / 255.0, x_test / 255.0
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)
# 将数据集从形状（n,宽度，高度）转化为（n,宽度高度，深度）
x_train = x_train.reshape(
    x_train.shape[0], x_train.shape[1], x_train.shape[2], 1
)
x_test = x_test.reshape(
    x_test.shape[0], x_test.shape[1], x_test.shape[2], 1
)

# 创建卷积神经网络
model = tf.keras.models.Sequential([

    # 卷积层  使用32个不同的3x3过滤器，激活函数使用relu
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(28, 28, 1)
    ),

    # 最大池化层, 使用 2x2 过滤器
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # 平坦化单元
    tf.keras.layers.Flatten(),

    # 添加一个带 dropout 的隐藏层，128个神经元的全连接，丢弃50%，防止过拟合出现
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),

    # 添加一个包含所有 10 位数字的输出单元的输出层
    tf.keras.layers.Dense(10, activation="softmax")
])

# 训练神经网络，优化器使用adam,损失函数使用categorical_crossentropy
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.fit(x_train, y_train, epochs=10)

# 评估神经网络性能
model.evaluate(x_test,  y_test, verbose=2)

# 保存模型
if len(sys.argv) == 2:
    filename = sys.argv[1]
    model.save(filename)
    print(f"Model saved to {filename}.")
