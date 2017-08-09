# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import baidu_index
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pylab import mpl


dates = []
beginDate = baidu_index.beginDate
beginDate = datetime.datetime.strptime(beginDate, '%Y-%m-%d')
date = baidu_index.beginDate
for day in range(baidu_index.days):
	dates.append(date)
	date = beginDate + datetime.timedelta(days=(day + 1))
	date = str(date).split(' ')[0]


indexs = baidu_index.day_montn_value()
plt.figure()
x = range(1, 31)
plt.plot(x, indexs, color="red", linewidth=2.0, linestyle="-")
plt.xlabel(u"日期")
plt.ylabel(u"热度指数")
plt.title(u"03-06———04.06赌博网站热度趋势统计")
plt.xticks([1, 8, 15, 22, 29], [dates[0], dates[7], dates[14], dates[21], dates[28]])
plt.grid(x)
# plt.show()
plt.savefig("赌博all") 