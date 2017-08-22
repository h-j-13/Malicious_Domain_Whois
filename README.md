非法域名挖掘与画像系统
=====================
![](https://img.shields.io/appveyor/ci/gruntjs/grunt.svg)![](https://img.shields.io/github/forks/h-j-13/Malicious_Domain_Whois.svg)![](https://img.shields.io/github/stars/h-j-13/Malicious_Domain_Whois.svg)![](https://img.shields.io/badge/license-AGPL-blue.svg)![](https://img.shields.io/badge/Python-2.7.12%2B-yellow.svg)![](https://img.shields.io/badge/MySQL-5.7.18%2B-yellow.svg)![](https://img.shields.io/badge/Power%20By-702229122-red.svg)    
**2017年第十届全国大学生信息安全大赛** 参赛项目 决赛-三等奖

基于页面关联关系的非法域名分析与挖掘系统。旨在通过域名多元信息对域名进行精准画像，进而分析抽象获取非法域名相关特征，使用基于决策树的机器学习模型进行域名性质判定。通过多过程多方式进行恶意域名挖掘

![](http://upload-images.jianshu.io/upload_images/5617720-cb399878f183d135.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## Summary

#### 系统核心功能
* 域名评估
	* 域名性质评估
	* 非法域名可疑值量化 
* 域名画像
	* 针对单一域名多元信息画像
	* 非法域名整体态势数据分析
* 非法域名挖掘
	* 基于WHOIS反查
	* 基于页面链接关系
	* 基于搜索引擎发现

#### 系统实现难点
* 海量域名及相关数据的高效与统一的存取模型
* 域名多元关键信息的高效获取与标准化处理
* 多维特征间静态与动态关联关系的构建
* 非法域名关键信息提取及知识图谱构建

#### 系统架构
![](http://upload-images.jianshu.io/upload_images/5617720-f0c27c19c09d9331.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 数据库架构
![](http://upload-images.jianshu.io/upload_images/5617720-a8185913b5221abc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 目录说明

DataAnalysis - 数据分析,特征项抽取    
DataAquire - 系统数据获取       
Database - 数据库设计与架构,操作脚本     
Doc - 系统文档、演示文档、论文      
EvaluationModel - 系统域名性质判别模型        
Website - 系统内容展示网站       

## Features

* 基于AMPQ协议的RabbitMQ实现的高效分布式WHOIS数据获取引擎
* 基于决策树的域名性质评估算法
* 基尼指数融合的域名可疑性量化模型
* 基于多维度特征关联的域名画像
* 基于多因素融合与多过程循环的非法域名挖掘算法

## Periodical achievment
#### 截至2017.7
域名 : 1.3亿条以上     
域名WHOIS数据 : 1.1 亿条以上     
域名WHOIS服务器 : 获取全部1500余顶级域, 382个WHOIS一级服务器, 1000余个WHOIS二级服务器     
域名评估模型准确率 :89.7%		（总数据3万,以8：2划分训练集与测试集）     
非法域名数量 : 135,391条记录  （系统起始5000条数据）     
域名画像 :对226,863条域名实现包括域名WHOIS信息、ip记录、多源地理位置信息、网页内容、热度趋势等方面的画像     
## Installation

各子模块下通过 ```main.py``` 文件运行

## Contribute

哈尔滨工业大学(威海) 信息与网络安全技术研究实验室    
@[day-dream](https://github.com/day-dreams)
@[carrie0307](https://github.com/carrie0307)

## License
GNU GENERAL PUBLIC LICENSE 3.0

## Contact
**h-j-13**(@\`13)      
[\`13的博客](http://www.jianshu.com/u/75156f101757)   		   
z.g.13@163.com/h.j.13.new@gmail.com		   
Harbin Institute of Technology at Weihai      