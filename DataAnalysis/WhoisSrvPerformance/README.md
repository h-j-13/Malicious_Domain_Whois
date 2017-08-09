WHOIS 服务器性能测试
----------------------
WhoisSrvPerformance

## Introduce
对whois服务器进行whois数据请求,检测请求耗时以及请求相应情况。将数据记录到数据库中。

## Install
* start : 进入系统根目录后```python whois_srv_performance_main.py```
* use 
├── Data
│   └── domain
│       ├── 104.155.8.56-whois.freenom.com.txt
│       │      ......... ip - 二级whois服务器.txt .......
│       └── 98.124.245.22-whois.fabulous.com.txt
├── database.py // 数据库操作
├── socks.py // sock核心
├── whois_connect.py // whois服务器数据获取
└── whois_srv_performance_main.py // 主程序入口


## Enviroment
* python 
  * mysqldb >= 1.2.5 
  * tldextract 
* 数据库系统配置在  ```database.py``` 中修改

		
## Contact

  * [**Github ： h-j-13**](https://github.com/h-j-13)
  * Harbin Institute of Technology at Weihai
  * Email : **z.g.13@163.com**/**h.j.13.new@gmail.com**
  * 哈尔滨工业大学(威海)
  * 2017年03月20日 
   
  