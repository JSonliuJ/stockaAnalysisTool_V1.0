# stockaAnalysisTool_V1.0

## 01 数据挖掘概述

### 1.1 数据分析

- **定义**: 对数据进行分析。专业的说法，数据分析是指根据分析目的，用适当的统计分析方法及工具，对收集来的数据进行处理与分析，提取有价值的信息，发挥数据的作用;
- **作用**：现状分析、原因分析、预测分析(定量)。数据分析的目标明确，先做假设，然后通过数据分析来验证假设是否正确，从而得到相应的结论;

### 1.2 数据挖掘

- 主要采用决策树、神经网络、关联规则、聚类分析等统计学、人工智能、机器学习等方法进行挖掘;
- 综合起来，数据分析(狭义)与数据挖掘的本质都是一样的，都是从数据里面发现关于业务的知识(有价值的信息)，从而帮助业务运营、改进产品以及帮助企业做更好的决策。数据分析(狭义)与数据挖掘构成广义的数据分析

### 1.3 数据挖掘场景

- 分类:对客户等级进行划分、验证码识别、水果品质自动筛选等
- 回归:对连续型数据进行预测、趋势预测等
- 聚类:客户价值预测、商圈预测等
- 关联分析:超市货品摆放、个性化推荐等

### 1.4 数据挖掘常用库

- `nuripy`模块∶矩阵运算、随机数的生成等
- `pandas`模块∶数据的读取、清洗、整理、运算、可视化等
- `matplotlib`模块∶专用于数据可视化，当然含有统计类的`seaborn`模块
- `statsmodels`模块∶构建统计模型，如线性回归、零回归、逻辑回归、主成分分析等
- `scipy`模块∶专用于统计中的各种假设检验，如卡方检验、相关系数检验、正态性检验、 t检验、F检验等
- `sklearn`模块∶专用于机器学习，包含了常规的数据挖掘算法，如决策树、森林树、提升树、贝叶斯、K近邻、SVM、GBDT、Kmeans等

## 02 项目实战

### 2.1 需求分析

- 需求：预测股票波动趋势
- 功能描述：
  - 抓取雪球财经网股票数据抓取
  - 数据指标分析
  - 数据可视化显示
  - 数据趋势预估

### 2.2 数据获取

- 获取方案
  - 爬虫：一段自动抓取互联网信息的程序，从互联网上抓取对于我们有价值的信息
  - request：实现数据获取

```
class DataAnalysisTool:
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    url_list = ["https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_={}".format(
page, round(time.time() * 1000)) for page in range(1, 166)]
    file_name = 'stock_data.csv'
    field_names = ['股票代码', '股票名称', '当前价', '涨跌幅','成交量']

    def __init__(self):
        self.fo = open(self.file_name, mode='w', encoding='utf-8', newline='')
        self.csv_write = csv.DictWriter(self.fo, fieldnames=self.field_names)
        self.csv_write.writeheader()

    def get_sh_sz_stock_info(self, url):
        res = requests.get(url, headers=self.header)
        data_list = res.json()['data']['list']
        # 提前股票信息
        for data in data_list:
            # 股票代码
            mapping = {}
            mapping['股票代码'] = data['symbol']
            # 股票名称
            mapping['股票名称'] = data['name']
            # 当前价
            mapping['当前价'] = data['current']
            # 涨跌幅
            mapping['涨跌幅'] = data['percent']
            # 成交量
            mapping['成交量'] = data['volume']
            self.csv_write.writerow(mapping)

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
        self.fo.close()
```

### 2.3 数据处理(清理)

#### 2.3.1 pandas 使用方法

##### 1. 数据导入

- **pd.read_csv(filename)：从CSV文件导入数据**
- pd.read_table(filename)：从限定分隔符的文本文件导入数据
- pd.read_excel(filename)：从Excel文件导入数据
- pd.read_sql(query, connection_object)：从SQL表/库导入数据
- pd.read_json(json_string)：从JSON格式的字符串导入数据
- pd.read_html(url)：解析URL、字符串或者HTML文件，抽取其中的tables表格
- pd.read_clipboard()：从你的粘贴板获取内容，并传给read_table()
- pd.DataFrame(dict)：从字典对象导入数据，Key是列名，Value是数据

##### 2. 数据查看

df：任意的Pandas DataFrame对象（比如pd的返回值）

s：任意的Pandas Series对象 

- df.**head**(n)：查看DataFrame对象的前n行
- df.tail(n)：查看DataFrame对象的最后n行
- df.shape()：查看行数和列数
- df.info()：查看索引、数据类型和内存信息
- df.describe()：查看数值型列的汇总统计 s.
- s.value_counts(dropna=False)：查看Series对象的唯一值和计数
- df.apply(pd.Series.value_counts)：查看DataFrame对象中每一列的唯一值和计数
- **df.dropna()**： 删除包含缺失值的行
- **df[["a","b"]]** ：直接取出对应a ,b的列数据
- **df.iloc[:10]** ：切位置,以序列号去切

```
def data_clear(self):
     # 4- 数据清洗---针对csv文件
     data_pd = pandas.read_csv(self.file_name)  # 从CSV文件导入数据
     # data_pd.head(10) # 查看前n行
     df = data_pd.dropna()  # 剔除缺失的行
     df1 = df[['股票名称', '当前价格']]  # 需要获取对应的数据
     df2 = df1.iloc[:10] # 获取10行数据
     return d2
```

### 2.4 数据可视化

#### 2.4.1 示例

```
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
```

效果图：

![1665588984868](C:\Users\jieliu666\AppData\Roaming\Typora\typora-user-images\1665588984868.png)



#### 2.4.2解决标签重叠问题

##### 1.  拉长画布

```
fig = plt.figure(figsize=(12,4))    # 设置画布大小
plt.bar(df['sport_type'], df['score'])
```

##### 2.  调整标签字体大小

```
plt.tick_params(axis='x', labelsize=4)
```

##### 3.  横纵颠倒

```
plt.barh(df['sport_type'], df['score'])
```

##### 4.  标签旋转

```
plt.bar(df['sport_type'], df['score'])
plt.xticks(rotation=-15)    # 设置x轴标签旋转角度
```



#### 2.4.3 matplotlib.pyplot.text()

 通过函数方式，向axes对象添加text对象，确切的说是向axes的( x , y )位置添加s文本，返回一个text实例。 

- 参数详解
  - **x, y** : scalars 防止text的位置
  - **s** : str 内容text
  - **fontdict** : dictionary, optional, default: None 一个定义s格式的dict
  -  **withdash** : boolean, optional, default: False。如果True则创建一个 [`TextWithDash`](https://matplotlib.org/api/text_api.html#matplotlib.text.TextWithDash)实例
  - `fontsize`设置字体大小，默认12，可选参数 [‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’,‘x-large’, ‘xx-large’]
  - `fontweight`设置字体粗细，可选参数 [‘light’, ‘normal’, ‘medium’, ‘semibold’, ‘bold’, ‘heavy’, ‘black’]
  - `fontstyle`设置字体类型，可选参数[ ‘normal’ | ‘italic’ | ‘oblique’ ]，italic斜体，oblique倾斜
  - `verticalalignment`设置水平对齐方式 ，可选参数 ： ‘center’ , ‘top’ , ‘bottom’ ,‘baseline’
  - `horizontalalignment`设置垂直对齐方式，可选参数：left,right,center
  - `rotation`(旋转角度)可选参数为:vertical,horizontal 也可以为数字
  - `alpha`透明度，参数值0至1之间
  - `backgroundcolor`标题背景颜色
  -  `bbox`给标题增加外框 ，常用参数如下： 
    - `boxstyle`方框外形
    - `facecolor`(简写fc)背景颜色
    - `edgecolor`(简写ec)边框线条颜色
    - `edgewidth`边框线条大小

#### 2.4.5 设置图的pylab样式

##### 1.  使用matplotliblib画图的时候经常会遇见中文或者是负号无法显示的情况 ，设置如下两个属性

```
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus']=False
```

##### 2.  rc配置

pylot使用rc配置文件来自定义图形的各种默认属性，称之为rc配置或rc参数。通过rc参数可以修改默认的属性，包括窗体大小、每英寸的点数、线条宽度、颜色、样式、坐标轴、坐标和网络属性、文本、字体等 

- 配置方式1：

```
matplotlib.rcParams[‘figure.figsize’]   #图片像素
matplotlib.rcParams[‘savefig.dpi’]      #分辨率
plt.savefig(‘plot123_2.png’, dpi=200)   #指定分辨率
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率
# 默认的像素：[6.0,4.0]，分辨率为100，图片尺寸为 600&400
# 指定dpi=200，图片尺寸为 1200*800
# 指定dpi=300，图片尺寸为 1800*1200
# 设置figsize可以在不改变分辨率情况下改变比例
plt.rcParams['figure.figsize'] = (5.0, 4.0)     # 显示图像的最大范围
plt.rcParams['image.interpolation'] = 'nearest' # 差值方式，设置 interpolation style
plt.rcParams['image.cmap'] = 'gray'             # 灰度空间
#设置rc参数显示中文标题
#设置字体为SimHei显示中文
plt.rcParams['font.sans-serif'] = 'SimHei'
#设置正常显示字符
plt.rcParams['axes.unicode_minus'] = False
#设置线条样式
plt.rcParams['lines.linestyle'] = '-.'
#设置线条宽度
```

- 配置方式2：

```
matplotlib.rc(“lines”, marker=”x”, linewidth=2, color=”red”)
```

- 恢复默认参数：恢复到缺省的配置(matplotlib载入时从配置文件读入的配置)

```
matplotlib.rcdefaults()
matplotlib.rcParams.update( matplotlib.rc_params() ) # 更新参数
```

#### 2.4.6 数据可视化代码

```
import matplotlib.pyplot as plt
from pylab import mpl
def data_show(self,data):
	mpl.rcParams['font.sans-serif'] = ['SimHei']
	mpl.rcParams['axes.unicode_minus']=False
	#6- 展示效果：web端
	# 绘制图形
	plt.bar(data['股票名称'].values, data['当前价格'].values,label='股票分析结果')#(横坐标，纵坐标)
    for a,b in zip(data['股票名称'].values, data['当前价格'].values):
        print(a,b)
        plt.text(a,b+5,b,horizontalalignment='center',verticalalignment='bottom',fontsize=10,rotation=0)
    plt.legend() #设置生效
    plt.xticks(rotation=-90)  # 设置x轴标签旋转角度
    plt.xlabel('股票名称')
    plt.ylabel('当前价格')
    plt.show()
```

#### 2.4.6 最终效果图

![1665592864054](C:\Users\jieliu666\AppData\Roaming\Typora\typora-user-images\1665592864054.png)

### 2.5 数据优化与分析

- 待优化，根据不同公司采用不同的规则算法