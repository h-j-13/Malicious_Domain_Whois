#WHOIS  GetDomainWhois Client
## Whois客户端
   
--------
##change_Log:  
<br></br>
###version 2.01：

* 改动内容：     
    * 增加了count_log.py,     
    * 修改了main.py
    
* 改动功能：   
    * 记录处理域名到数量，记录到数据库中。

###version 2.02：

* 改动内容：
    * 修改了main.py    
    * 增加了WhoisCline.conf
	
* 改动功能：   
    * 1,修改了处理逻辑：为了配合主程序，使其在无法获取域名的时候也不会退出,隔一段时间自动检测服务器是否在运行，运行则重连。否者继续挂起
    * 2,增加了一项 暂时记录whois返回数据，用于后来分析获取内容正确性和正确率。配合2.01的统计功能，查看数据高峰时的正确率。
    * 3,使用配置文件，所需数据，方便程序的部署。

###last-update：

* 最后更新 ： 2016.7.22
* 版本     ： version 2.02

<br></br>
<br></br>
<br></br>
##about me：

* Email:z.g.13@163.com 
* Email:h.j.13.new@gmail.com
* QQ: 450943084   
* A student at HITwh    
* 2016年7月22日
