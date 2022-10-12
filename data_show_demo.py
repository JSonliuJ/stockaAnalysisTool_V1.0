# -- encoding: utf-8 --
# @time:    	2022/10/12 23:03
# @Author: 		JsonLiu
# @Email:  		492224300@qq.com

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus']=False
# 准备数据
data = {'sport_type':['N good limited company', 'Delay jiang shares limited company', 'Linktone limited company', 'Witten electric limited company', 'C fu chong limited company'], 'score':[20.74, 20.02, 20, 17.98, 17.79]}
df = pd.DataFrame(data)
# 绘制图形
# fig = plt.figure(figsize=(15,4))    # 法1：设置画布大小:这种方式最好
# plt.tick_params(axis='x', labelsize=4)    # 法2：设置x轴标签大小
# plt.barh(df['sport_type'], df['score'])    # 法3：绘制横向柱状图
plt.bar(df['sport_type'], df['score']) # 常规
plt.xticks(rotation=-15)    # 法4：设置x轴标签旋转角度
plt.show()