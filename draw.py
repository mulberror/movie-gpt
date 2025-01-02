import matplotlib.pyplot as plt

# 假设的数据点
x = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # X轴上的数据
y1 = [8.1823, 10.323, 9.5431, 4.142, 2.623, 1.912, 1.645, 1.584, 1.6113]  # 第一条折线的Y轴数据
y2 = [8.3823, 10.512, 9.7674, 5.5432, 3.5323, 3.2453, 3.3613, 3.2912, 3.3031]  # 第二条折线的Y轴数据

# 创建第一条折线图
plt.plot(x, y1, marker='o', linestyle='-', color='b', label='finetuned')  # 使用圆形标记，蓝色线条，标记为 Line 1

# 创建第二条折线图
plt.plot(x, y2, marker='s', linestyle='-', color='r', label='unfinetuned')  # 使用方形标记，红色线条，标记为 Line 2

# 设置Y轴范围
plt.ylim(0, max(max(y1), max(y2)) + 1)  # 将Y轴范围设置为从0到最大y值+1

# 添加图例
plt.legend()

# 显示图形
plt.show()
