#!/usr/bin/python
# encoding:utf-8

"""
    SQL语句 优化/重构 的封装

author     :   @`13
version    :   0.1.2
last-update:   2016.9.28

# history：
version 0.1.2
    *   + 增加了一个专用方法(isFlag_100
    *   ~ 修改了更新语句方法,使其支持多个字段修改

version 0.1.1
    *   + 增加了异常类
    *   + 增加了更新语句

version 0.1.0
    *   + 增加了按域名查询
    *   + 增加了按注册信息反查
"""


#  通过hash值获取表序号
def get_table_num(hash_value):
    if -9223372036854775807 <= hash_value < -9041910387563639558:
        return 1
    elif -9041910387563639558 <= hash_value < -8857984879495662570:
        return 2
    elif -8857984879495662570 <= hash_value < -8676052222771162099:
        return 3
    elif -8676052222771162099 <= hash_value < -8492958545851525842:
        return 4
    elif -8492958545851525842 <= hash_value < -8313596163777659659:
        return 5
    elif -8313596163777659659 <= hash_value < -8133013853426072265:
        return 6
    elif -8133013853426072265 <= hash_value < -7949254487539842026:
        return 7
    elif -7949254487539842026 <= hash_value < -7767101558415918909:
        return 8
    elif -7767101558415918909 <= hash_value < -7580839670354682535:
        return 9
    elif -7580839670354682535 <= hash_value < -7393347003251626769:
        return 10
    elif -7393347003251626769 <= hash_value < -7208706117755245904:
        return 11
    elif -7208706117755245904 <= hash_value < -7022881013166758104:
        return 12
    elif -7022881013166758104 <= hash_value < -6840531437685402825:
        return 13
    elif -6840531437685402825 <= hash_value < -6655043275151068729:
        return 14
    elif -6655043275151068729 <= hash_value < -6470707896125423243:
        return 15
    elif -6470707896125423243 <= hash_value < -6283500461484045792:
        return 16
    elif -6283500461484045792 <= hash_value < -6098832178244835834:
        return 17
    elif -6098832178244835834 <= hash_value < -5910113712972758336:
        return 18
    elif -5910113712972758336 <= hash_value < -5727102585206919478:
        return 19
    elif -5727102585206919478 <= hash_value < -5544820905583124692:
        return 20
    elif -5544820905583124692 <= hash_value < -5359177872684861375:
        return 21
    elif -5359177872684861375 <= hash_value < -5174871909922848832:
        return 22
    elif -5174871909922848832 <= hash_value < -4990042537780986938:
        return 23
    elif -4990042537780986938 <= hash_value < -4805622792287746420:
        return 24
    elif -4805622792287746420 <= hash_value < -4620014696331001069:
        return 25
    elif -4620014696331001069 <= hash_value < -4434657474076807661:
        return 26
    elif -4434657474076807661 <= hash_value < -4252263232161295062:
        return 27
    elif -4252263232161295062 <= hash_value < -4069017298573509904:
        return 28
    elif -4069017298573509904 <= hash_value < -3886255227510208801:
        return 29
    elif -3886255227510208801 <= hash_value < -3703662328893783636:
        return 30
    elif -3703662328893783636 <= hash_value < -3515523092952420781:
        return 31
    elif -3515523092952420781 <= hash_value < -3333754744758691556:
        return 32
    elif -3333754744758691556 <= hash_value < -3147701246317123863:
        return 33
    elif -3147701246317123863 <= hash_value < -2963182437664623451:
        return 34
    elif -2963182437664623451 <= hash_value < -2776393111201893612:
        return 35
    elif -2776393111201893612 <= hash_value < -2594314482744055116:
        return 36
    elif -2594314482744055116 <= hash_value < -2409883441646119630:
        return 37
    elif -2409883441646119630 <= hash_value < -2227632836850353085:
        return 38
    elif -2227632836850353085 <= hash_value < -2046145094893685537:
        return 39
    elif -2046145094893685537 <= hash_value < -1864090509109668823:
        return 40
    elif -1864090509109668823 <= hash_value < -1684323495925778973:
        return 41
    elif -1684323495925778973 <= hash_value < -1503098726931071747:
        return 42
    elif -1503098726931071747 <= hash_value < -1318079107119979920:
        return 43
    elif -1318079107119979920 <= hash_value < -1135357276338208456:
        return 44
    elif -1135357276338208456 <= hash_value < -951553518871153121:
        return 45
    elif -951553518871153121 <= hash_value < -765124093650135186:
        return 46
    elif -765124093650135186 <= hash_value < -579037060369460356:
        return 47
    elif -579037060369460356 <= hash_value < -395101256341887092:
        return 48
    elif -395101256341887092 <= hash_value < -211730412910763603:
        return 49
    elif -211730412910763603 <= hash_value < -25556603170130521:
        return 50
    elif -25556603170130521 <= hash_value < 159288084334667083:
        return 51
    elif 159288084334667083 <= hash_value < 344604009295076071:
        return 52
    elif 344604009295076071 <= hash_value < 530999174377205813:
        return 53
    elif 530999174377205813 <= hash_value < 717010919267269911:
        return 54
    elif 717010919267269911 <= hash_value < 897990329583178697:
        return 55
    elif 897990329583178697 <= hash_value < 1082667744008564916:
        return 56
    elif 1082667744008564916 <= hash_value < 1269704720045858118:
        return 57
    elif 1269704720045858118 <= hash_value < 1455886341360265804:
        return 58
    elif 1455886341360265804 <= hash_value < 1642541005601645096:
        return 59
    elif 1642541005601645096 <= hash_value < 1829170723854020188:
        return 60
    elif 1829170723854020188 <= hash_value < 2015179899793637477:
        return 61
    elif 2015179899793637477 <= hash_value < 2198725657853912502:
        return 62
    elif 2198725657853912502 <= hash_value < 2383222083340196998:
        return 63
    elif 2383222083340196998 <= hash_value < 2568460622793726904:
        return 64
    elif 2568460622793726904 <= hash_value < 2752150262291046681:
        return 65
    elif 2752150262291046681 <= hash_value < 2934331881987700116:
        return 66
    elif 2934331881987700116 <= hash_value < 3118356437781161486:
        return 67
    elif 3118356437781161486 <= hash_value < 3302995617490917805:
        return 68
    elif 3302995617490917805 <= hash_value < 3486008397168026820:
        return 69
    elif 3486008397168026820 <= hash_value < 3671409183307186906:
        return 70
    elif 3671409183307186906 <= hash_value < 3854954082361497766:
        return 71
    elif 3854954082361497766 <= hash_value < 4036373553448562381:
        return 72
    elif 4036373553448562381 <= hash_value < 4217539835225039413:
        return 73
    elif 4217539835225039413 <= hash_value < 4405569199757502786:
        return 74
    elif 4405569199757502786 <= hash_value < 4591644844256374089:
        return 75
    elif 4591644844256374089 <= hash_value < 4776748165546915564:
        return 76
    elif 4776748165546915564 <= hash_value < 4959670820158985020:
        return 77
    elif 4959670820158985020 <= hash_value < 5146619133136544692:
        return 78
    elif 5146619133136544692 <= hash_value < 5327765228409928659:
        return 79
    elif 5327765228409928659 <= hash_value < 5513089284982408107:
        return 80
    elif 5513089284982408107 <= hash_value < 5699003375141748833:
        return 81
    elif 5699003375141748833 <= hash_value < 5883307693804165937:
        return 82
    elif 5883307693804165937 <= hash_value < 6070231342114597767:
        return 83
    elif 6070231342114597767 <= hash_value < 6257587847190219404:
        return 84
    elif 6257587847190219404 <= hash_value < 6441294117889663411:
        return 85
    elif 6441294117889663411 <= hash_value < 6627264217482839980:
        return 86
    elif 6627264217482839980 <= hash_value < 6812452941227091114:
        return 87
    elif 6812452941227091114 <= hash_value < 6994316918238938739:
        return 88
    elif 6994316918238938739 <= hash_value < 7186332676230699766:
        return 89
    elif 7186332676230699766 <= hash_value < 7373459306470554807:
        return 90
    elif 7373459306470554807 <= hash_value < 7558282992028316382:
        return 91
    elif 7558282992028316382 <= hash_value < 7748226753770500566:
        return 92
    elif 7748226753770500566 <= hash_value < 7933723407478577857:
        return 93
    elif 7933723407478577857 <= hash_value < 8119718400456903685:
        return 94
    elif 8119718400456903685 <= hash_value < 8303095551645269628:
        return 95
    elif 8303095551645269628 <= hash_value < 8486963463806472671:
        return 96
    elif 8486963463806472671 <= hash_value < 8673409487385938207:
        return 97
    elif 8673409487385938207 <= hash_value < 8857059862262885588:
        return 98
    elif 8857059862262885588 <= hash_value < 9037415037309220504:
        return 99
    elif 9037415037309220504 <= hash_value <= 9233372036854775808:
        return 100
    else:
        raise TableChoiceError()


# 忽略选择错误
class TableChoiceError(Exception):
    pass


# 语句生成错误类
class GenSQLError(Exception):
    def __init__(self, value):
        self.value = value
        self.error_list = ['param error：请检查传入的参数是否正确']

    # @override
    def __str__(self):
        return str(self.error_list[self.value])


# SQL语句优化类
class SQL_refactor:
    """
    SQL语句优化类
    """

    def __init__(self):
        pass

    @staticmethod
    def SELECT_by_domain(domain, ):
        """
        :param 以 domian 为关键词在数据库中查找
        :return:经过优化的SQL语句
        """
        # tld = tldextract.extract(domain).suffix
        domain_hash = hash(domain)
        table_num = get_table_num(hash(domain))
        # 增不增加  flag > 0 这一项,
        #          tld = domain.tld这一项 差别不是很大。
        # domain 中包含了 tld，domain和tld    是domian_index 联合索引
        SQL = """SELECT * FROM domain_whois.domain_whois_{num} WHERE domain_hash = {hash} """.format(
            num=table_num, hash=domain_hash,
        )
        # print SQL
        return SQL

    @staticmethod
    def Update_by_domain(domain, UpdateCon=None, UpdateVal=None):
        """
        :param domain: 以 domian 为关键词
        :param UpdateCon: 需要更新的字段   (！需要是列表)
        :param UpdateVal: 更新的值 （与前一个参数需要一一对应）
        :return: 经过优化的SQL语句
        """
        # tld = tldextract.extract(domain).suffix
        domain_hash = hash(domain)
        table_num = get_table_num(hash(domain))
        if UpdateCon or UpdateVal:
            if len(UpdateCon) != len(UpdateVal):    # 如果传入的参数不对应则报错
                raise GenSQLError(0)
            else:
                SQL = """UPDATE domain_whois.domain_whois_{num} SET """.format(num=table_num)
                for index in range(len(UpdateCon)):
                    SQL += """ `{con}`={val},""".format(con=UpdateCon[index], val=UpdateVal[index])
                SQL = SQL[:-1]  # 去掉最后一个多余的','
                SQL += """ WHERE domain_hash = {hash} """.format(hash=domain_hash)
        return SQL

    @staticmethod
    def SELECT_by_regInfo(reg_info, info_type='reg_name', table_num=-1):
        """
        :param 以 注册者信息 为关键词在数据库中查找
        :return:经过优化的SQL语句
        """
        # 没有制定要查询的表。
        if table_num == -1:
            SQL = """"""
            for tableNum in range(1, 100):
                SQL += """SELECT * FROM domain_whois.domain_whois_{table_num} WHERE {column_name} = '{reg_info}'""".format(
                    table_num=tableNum, column_name=info_type, reg_info=reg_info, )
                SQL += """ UNION """
            SQL = SQL[:-6]
            SQL += """;"""
            # print SQL
            return SQL

        else:
            # 指定要查询的表
            SQL = """SELECT * FROM domain_whois.domain_whois_{num} WHERE {column_name} = `{reg_info}`;""".format(
                num=table_num, column_name=info_type, reg_info=reg_info
            )
            # print SQL
            return SQL

    @staticmethod
    # 专用
    def isFlag_100(domain, ):
        """
        :param 以 domian 为关键词在数据库中查找
        :return: 判断domain的flag是否为-100
        """
        domain_hash = hash(domain)
        table_num = get_table_num(hash(domain))
        SQL = """SELECT `flag` FROM domain_whois.domain_whois_{num} WHERE domain_hash = {hash} """.format(
            num=table_num, hash=domain_hash,
        )
        # print SQL
        return SQL


if __name__ == '__main__':
    print 'test'
    print SQL_refactor.SELECT_by_domain('agahii.ir')