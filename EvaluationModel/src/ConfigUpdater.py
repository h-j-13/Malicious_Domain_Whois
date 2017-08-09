#!coding:utf-8

"""
    如果必要,在系统启动时更新配置文件
"""

import BaseSQL
import config

# TODO: 完善样本数据的选择,使随机化
def update_config_on_alexa():
    """
        更新alexa方面的概率
    """
    alex_has=BaseSQL.has_alex_rank()
    alex_no=BaseSQL.no_alex_rank()
    config.probability_has_alexa_rank=float(alex_has['mal&&alex'])/float(alex_has['alex'])
    config.probability_no_alexa_rank=float(alex_no['mal&&noalex'])/float(alex_no['noalex'])


#TODO: 完善样本数据来源,使随机化
def update_config_on_locate():
    """
        更新地理位置比对方面的概率
    """
    locate_same=BaseSQL.same_location()
    locate_diff=BaseSQL.diff_location()
    config.probability_locate_match=float(locate_same['mal&&same'])/float(locate_same['same'])
    config.probability_locate_diff=float(locate_diff['mal&&diff'])/float(locate_diff['diff'])
