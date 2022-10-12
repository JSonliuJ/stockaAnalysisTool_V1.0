# -- encoding: utf-8 --
# @time:    	2022/10/12 20:44
# @Author: 		JsonLiu
# @Email:  		492224300@qq.com
"""
数据挖掘：
    1. 获取数据
        - 静态：本地文件
        - 动态：网址
    2. 存储数据
    3. 清洗数据
    4. 算法分析
    5. 结果展示
    6. 分析汇总
"""
import csv
import threading
import time

import pandas
import requests
import matplotlib.pyplot as plt
from pylab import mpl

class DataAnalysisTool:
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    url_list = [
        "https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_={}".format(
            page, round(time.time() * 1000)) for page in range(1, 166)]
    file_name = 'stock_data.csv'
    field_names = ['股票代码', '股票名称', '当前价格', '涨跌幅','成交量']

    def __init__(self):
        # self.fo = open(self.file_name, mode='w', encoding='utf-8', newline='')
        # self.csv_write = csv.DictWriter(self.fo, fieldnames=self.field_names)
        # self.csv_write.writeheader()
        pass

    def get_sh_sz_stock_info(self, url):
        res = requests.get(url, headers=self.header)
        data_list = res.json()['data']['list']
        # 提取股票信息
        for data in data_list:
            # 股票代码
            mapping = {}
            mapping['股票代码'] = data['symbol']
            # 股票名称
            mapping['股票名称'] = data['name']
            # 当前价
            mapping['当前价格'] = data['current']
            # 涨跌幅
            mapping['涨跌幅'] = data['percent']
            # 成交量
            mapping['成交量'] = data['volume']
            # self.csv_write.writerow(mapping)

    def thread_request(self, target_name, url_list):
        threads_list = []
        for url in url_list:
            task = threading.Thread(target=target_name, args=(url,))
            threads_list.append(task)
        for t in threads_list:
            t.start()
            time.sleep(1)
        for t in threads_list:
            t.join()

        time.sleep(5)
        # self.fo.close()

    def data_clearing(self):
        # 数据清洗---针对csv文件
        data_pd = pandas.read_csv(self.file_name)  # 从CSV文件导入数据
        # data_pd.head(10) # 查看前n行
        df = data_pd.dropna()  # 剔除缺失的行
        df1 = df[['股票名称', '成交量']]  # 需要获取对应的数据
        df2 = df1.iloc[:10] # 获取10行数据
        return df2

    def chart_display(self,data):
        '''
        :param data:
            horizontalalignment:设置垂直对齐方式，可选参数：left,right,center
            verticalalignment:设置水平对齐方式 ，可选参数 ： ‘center’ , ‘top’ , ‘bottom’ ,‘baseline’
            fontsize:字体大小
            rotation: (旋转角度) 可选参数为:vertical,horizontal 也可以为数字
        :return:
        '''
        # 设置字体为SimHei显示中文
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        # 设置正常显示字符
        mpl.rcParams['axes.unicode_minus'] = False
        # 设置线条宽度
        plt.rcParams['lines.linewidth'] = 3
        # 绘制图形
        plt.bar(data['股票名称'].values, data['成交量'].values, label='股票分析结果')  # (横坐标，纵坐标)
        for a, b in zip(data['股票名称'].values, data['成交量'].values):
            print(a, b)
            plt.text(a, b + 5, b, horizontalalignment='center', verticalalignment='bottom', fontsize=8, rotation=0)

        plt.legend()  # 设置生效
        plt.xticks(rotation=-90)  # 设置x轴标签旋转角度

        plt.xlabel('股票名称')
        plt.ylabel('成交量')
        plt.show()

    def run(self):
        dst.thread_request(self.get_sh_sz_stock_info, self.url_list)
        data = self.data_clearing()
        self.chart_display(data)


if __name__ == '__main__':
    dst = DataAnalysisTool()
    # print(dst.url_list)
    # dst.thread_request(dst.get_sh_sz_stock_info, dst.url_list)
    data = dst.data_clearing()
    dst.chart_display(data)

    # dst.run()