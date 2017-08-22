#coding:utf-8

#
# 配置文件
#


#
# FIXME:已知issues
#   1.ProxyHelper:
#       一个代理正在使用时，如``代理添加调用，则它有被覆盖的风险。
#   2.HtmlDownloader:
#

#
# TODO:待添加逻辑
#   1.更多的反爬虫逻辑，如请求头、cookies等
#
#

#
# TODO:代理配置
# 格式：
#    ['127.0.0.1:8080',0]   可用
#    ['127.0.0.1:8080',1]   正忙
my_proxys=['http://119.23.134.139:3128','http://106.15.45.157:3128','http://106.15.44.81:3128']#初始代理，目前为空
enable_proxy=True#是否使用代理

#
# 各种超时时限
#
init_proxy_timeout=60#初始化代理池的时限
test_proxy_timeout=3#测试代理时的时限
download_alex_rank_timeout=10#下载alex排名页面的时限
download_alex_judge_timeout=10#下载alex权威检测页面的时限
get_domain_timeout=30#获取任务域名的时限，需要考虑数据库操作的延迟
get_html_timeout=50#获取[domain,html]的时限，需要考虑获取任务域名的时限
get_result_timeout=70#获取[domain,data]的时限，需要考虑获取[domain,html]的时限

#
# 目标网页控制,支持以下
#   alex-rank | alex-judge |.....
to_download="alex-rank"

#
# response包保存选项
#
save_response=False
path_to_save="/home/moon/Desktop/spider-entry/response/"

#
# 下载网页的线程数
#
num_html_download_thread=2
