基于whois的恶意域名分析与挖掘系统 - whois 子系统
----------------------
Malicious Domain Whois SYS - whois


## 系统安装与部署:

* 依赖环境:    
    * MySQL > 5.6.x   
    * python > 2.7.x
    * MySQL python扩展   
    *推荐使用　```sudo apt-get install mysql-python``` 安装*
    * python 第三方库,详细依赖环境请见 ```requirements.txt```    
    *推荐使用 ```sudo pip install -r requirement.txt```*
* 系统安装:
    * 程序入口 : **main.py**
    * 子系统由网站后台服务器自动调用，无需手动开启
    * 修改程序配置文件中的对应选项以适配即可
        * 数据库配置项中请提供一个**拥有读写权限**的账户及**对应系统数据库的各表名称**
* 目录结构及各文件说明:
    * 详见各目录下 ```init.py``` 和 文件开头注释
   
    
## 数据说明:

*   数据库表说明  
    * 详细见 Project/Domain/Readme
    * *(详细说明见malicious_domain_sys.SQL 中的注释)*
    
*   部分数据项说明
    *   whois_flag  (存在于 **domain , whois** 表中, 针对二级whois服务器)         
    
		whois_flag          |         含义                 
		:----------:| :------:|
        -99         | 尚未处理                              
		0            | /_无法处理_ *(无法获取whois服务器地址或其他原因)*       
		1            | 完全正常        
		-1           | 超时        
		-2           | DNS异常
		-3           | sockset意外关闭       
		-4           | 其他未知原因        
		-5           | 获取的是**空数据**/查询速度过快
	    -11         | 一级数据获取正常,二级超时        
	    -12         | 一级数据获取正常,二级DNS异常         
	    -13         | 一级数据获取正常,二级sockset意外关闭         
	    -14         | 一级数据获取正常,二级其他未知原因        
	    -15         | 一级数据获取正常,二级查询速度过快       
					 
	*   status  (存在于**whois**表中) 
	    
		status         |    含义         
		:-------------:| :-------:|                                
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
		    31	|	CONNECT  *(.de whois特殊服务器状态)*
		    
		*   此项整合了**EPP** 与 **RPP** 状态  
		    想要获取更多有关内容请访问 [**域名状态值**](http://wenku.baidu.com/link?url=ywouBPjNb7sHgZDjN-mHFxgqO1Bwam-f5W7cgaZmHkuRFmd3DzzSKsVKoGnohS6zK2ytsenmEK-8pLId9T7PmBV2WVslAKSbu8ve_SByvaq) 或者 **wiki**
    *   whowas_flag (存在于**domain,whowas**表中) 
        *   详见whowas子系统说明

    *   malicious_flag  (存在于 **domain_index , malicious_info** 表中, 针对二级whois服务器)

		flag(第二位\[十位\])    |         含义
		:----------:| :------:|
        0         | 尚未处理
		1            | 能够正常访问
		7            | 被服务器拒绝 *\[errno 104\]:connetction reset by peer*
		8            | 访问过程中出现错误
		9            | 无法解析/访问


	    * 此项表示域名当前的解析情况
  
## 其他功能说明:

   *  开启代理socoket
    * 1,将 **../Setting/setting.json** 中的 **proxySocks** 设置为 **true**    
		```"proxySocks":true```
	* 2,将代理sockset信息*[ip],[端口],[类型],[用户;密码]* 插入 whois_proxy 表中
	* 3,重启系统

   * 覆盖新的顶级域
	* 1,获取新顶级域的**whois服务器地址,ip地址(可选)**
	* 2,将***whois地址与tld***对应插入 **whois_tld_addr** 表中
	* 3,将***whois地址与ip***插入 **whois_srvip** 表中 (可选)
	* 4,将此顶级域对应的提取函数名称与whois服务器写入**service_function.dat**,将提取函数放入**whois_func.py**中
	* 5,重启系统
	  * *关于提取函数写法可参照**whois_func.py**中其他提取函数和whois服务器返回数据格式*
	
   * 数据库结构变更
     * 请不要变更子系统依赖数据表(**whois_proxy,whois_tld_addr,whois_srvip**)的结构 
     * 将**whois**表结构修改后,程序**全部**的**SQL语句**均集中在**../DataBase/update_record.py**中,按找当前结构修改写入SQL语句即可
	
   * 运行日志说明  
	* 查看运行日志 **running.log** 将会帮助您更方便的理解程序及处理异常
	* 系统自动保留 **最近三天** 的日志
    * 您可能会在日志中见到集中常见错误:
	    * whois通信地址获取失败 :*表示当前域名的whois服务器地址不在数据库中*   
	    * MySQL语句错误 : 由与**未预计的返回数据编码** 或者 **极其特别的whois数据** 导致的数据库读写异常
	      * *为了获取 **中文** whois数据,数据库采用了**utf-8编码**,在处理**日文,韩文,其他非英文语言时**数据时可能会报错,在日志中也会记录此类域名的**原始whois信息***
	    * 其他异常及错误

## 最后:
  * 2017年03月20日 
   
  