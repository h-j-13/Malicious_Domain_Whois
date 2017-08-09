基于whois的恶意域名分析与挖掘系统 - whois信息反查子系统
----------------------
Malicious Domain Whois SYS - ReverseLookup

## 配置说明与运行

* 此系统由```<何志坤>```学长域名注册者信息反查系统修改而来
* 环境:
	* scarpy　1.3.3
	* 推荐以下命令安装　``` sudo pip install scarpy```
* 运行逻辑:
  *  step1: 系统由**malicious_domain_sys.info_reverse_search**表中获取需要反查的域名whois信息
  * step2: 系统从 [笨米网](https://www.benmi.com/) 反查whois信息对应的域名
  * step3: 系统将域名更新到 **domain_index** 表中,并添加对应的反查标志为
  * step4: 修改**malicious_domain_sys.info_reverse_search**表中的标记位,标记信息已经反查过
* 运行:
	* 各个子系统下的　```../start_regtrant.py```


## 数据说明

*   数据库部分标记位项说明　
    *   info_type  (存在于 **info_reverse_search** 表中)         
    
		info_type          |         含义                 
		:----------:| :------:|
        -10         | 尚未处理                                   
		2            | 注册者姓名
		3            | 注册者Email    
		4            | 注册者电话
	
    *   source  (存在于 **domain_index** 表中)         
    
		source          |         含义                 
		:----------:| :------:|
        -10         | 尚未处理/直接导入                                   
		12            | 通过注册者姓名反查得到
		13            | 通过注册者Email反查得到        
		14            | 通过注册者电话反查得到
		
## 最后

  * 联系方式 : **z.g.13@163.com**/**h.j.13.new@gmail.com** 
  * 哈尔滨工业大学(威海)
  * 2017年03月26日 
   