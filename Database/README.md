基于whois的恶意域名分析系统
---------------------------------------------
数据库设计与说明文档

### 整体架构    
  * 数据库以域名**ID**作为全局唯一标志
	  * **ID** 使用 *python 2.7.12+ / GCC6.0 /x64* 版**python**内建函数```hash()```生成,你可以通过 ```hash('target object')``` 的方式轻松生成一个**ID**
	  * 请注意你的python **版本** 
	  * 预期数据量为**百万级别** , *不予处理哈希碰撞的情况*
  * 数据库整体分为 **域名数据**,**whois/whowas数据**,**地理位置数据**,**其他信息数据**,**whois获取系统核心数据**,**网站后台数据**,**其他所需数据**，几部分组成。
  * [**数据库设计说明**](https://www.processon.com/view/link/58cdd412e4b0fdc355a12fdf) ( **ProcessOn** 持续更新中...)
  * 所有**flag标记**为默认值为 -100,-10...


### 数据库使用说明
  * 请按照如下原则编写SQL语句
	  * **domain_index** 表中请插入**域名**而非**URL**!    
    * **SELECT** 语句不要筛选**全部**字段    
    * 尽量**减少**数据库**读取**次数
    * 尽量使用有**索引**的字段来进行记录检索
    * 注意表中**触发器**和**外键**,减少无用的写入操作
    * 系统**配置参数**及**依赖数据**请在系统初始化的之后**读取一次**即可,在程序中使用*dict*或者其他数据结构来存取即可
    * 不要修改任何与你无关的**数据表**与**字段类型**
    * 若出现字段不够长或需要新增字段/索引的情况,请联系我
    * 表中所有**时间**字段均由**MySQL**按需要自动更新,时间以**数据库本地时间**为准
  * 数据库flag项目说明
	  *   whois_flag (**domain_index**,**whois**表中)         
    
		whois_flag  | 含义                 
		:----------:| :------:|
		-10         | 未处理/默认值                          
		0           | _无法处理_ *(无法获取whois服务器地址或其他原因)*       
		1           | 完全正常        
		-1          | 超时        
		-2          | DNS异常
		-3          | sockset意外关闭       
		-4          | 其他未知原因        
		-5          | 获取的是**空数据**/查询速度过快
	    9           | 一级数据获取正常,二级超时        
	    8           | 一级数据获取正常,二级DNS异常         
	    7           | 一级数据获取正常,二级sockset意外关闭         
	    6           | 一级数据获取正常,二级其他未知原因        
	    5           | 一级数据获取正常,二级查询速度过快       
	  *   status  (**whowas**,**whois**表中)   
	  	    
		status          |  含义         
		:-------------: | :-------:|                                
			1	|	ADDPERIOD       
			2	|	AUTORENEWPERIOD     
			3	|	INACTIVE        
			4	|	OK      
			5	|	PENDINGCREATE
			6	|	PENDINGDELETE
			7	|	PENDINGRENEW
			8	|	PENDINGRESTORE
			9	|	PENDINGTRANSFER
		    10	|	PENDINGUPDATE
		    11	|	REDEMPTIONPERIOD
		    12	|	RENEWPERIOD
	    	13	|	SERVERDELETEPROHIBITED
		    14	|	SERVERHOLD
		    15	|	SERVERRENEWPROHIBITED
		    16	|	SERVERTRANSFERPROHIBITED
		    17	|	SERVERUPDATEPROHIBITED
		    18	|	TRANSFERPERIOD
		    19	|	CLIENTDELETEPROHIBITED
		    20	|	CLIENTHOLD
		    21	|	CLIENTRENEWPROHIBITED
		    22	|	CLIENTTRANSFERPROHIBITED
		    23	|	CLIENTUPDATEPROHIBITED
		    24	|	ACTIVE
		    25	|	REGISTRYLOCK
		    26	|	REGISTRARLOCK
		    27	|	REGISTRYHOLD
		    28	|	REGISTRARHOLD
		    29	|	NOTEXIST ***(域名不存在)***
		    30	|	NOSTATUS  ***(无状态值)***
		    31	|	CONNECT  *(de服务器状态)*
		    str |   其他无法解析的内容存储原字符
	*   此项整合了**EPP** 与 **RPP** 状态  
		想要获取更多有关内容请访问 [**域名状态值**](http://wenku.baidu.com/link?url=ywouBPjNb7sHgZDjN-mHFxgqO1Bwam-f5W7cgaZmHkuRFmd3DzzSKsVKoGnohS6zK2ytsenmEK-8pLId9T7PmBV2WVslAKSbu8ve_SByvaq) 或者 **wiki*

	  *   pos-flag  (**domain**,**locate**表中)
	 
		 pos-flag  | 含义                 
		:----------:| :------:|
		-10         | 未处理/默认值   
		      
	  *   info-flag  (**domain**,**other_info_flag**表中) 
	  
		 info-flag  | 含义                 
		:----------:| :------:|
		-10         | 未处理/默认值      
		
	  *   malicious-flag  (**domain**,**malicious_flag**表中) 
	  
  		 info_flag  | 含义                 
		:----------:| :------:|
		-10         | 未处理/默认值   

### 最后:
