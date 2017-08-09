#coding=utf-8
import sys

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

reload(sys)
sys.setdefaultencoding('utf-8')



sender = '844640830@qq.com'
receivers = ['844640830@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("844640830@qq.com", 'utf-8')
message['To'] = Header("844640830@qq.com", 'utf-8')
subject = 'data result'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('data:', 'plain', 'utf-8'))

'''
# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('dropcatch.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="dropcatch.txt"'
message.attach(att1)

att1 = MIMEText(open('dropcatch_diff.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="dropcatch_diff.txt"'
message.attach(att1)
'''

mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "844640830@qq.com"  # 用户名
mail_pass = "xnnushjxlbenbdgc"  # 口令jydfnsxflawmbfjh


if 1==1:
    smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtpObj.login(mail_user,mail_pass)
    #smtpObj = smtplib.SMTP()
    #smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    #smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
