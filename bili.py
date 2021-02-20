import requests
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def emailsend():
    localtime = time.asctime( time.localtime(time.time()) )
    mail_msg = '<h1>祝贺B站用户%s（uid：%s）于%s达到了%s个粉丝数\n</h1>'\
               '<h2>邮件由系统自动发出，无需回复</h2>'%(name,uid,localtime,max_fans)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header('jiajiu', 'utf-8')
    message['To'] =  Header(username,'utf-8')
    subject = 'BiliBili粉丝提醒'
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP() 
    smtpObj.connect('smtp.qq.com',587)
    smtpObj.login(emailaddr,passwd)
    smtpObj.sendmail(emailaddr,emailaddr,message.as_string())
    print ("邮件发送成功")
uid = input('请输入你想查询的用户的UID:')
uid = int(uid)
max_fans = 0
last_fans = 0
response = requests.get('https://api.bilibili.com/x/web-interface/card?mid=%d'%(uid))
data = json.loads(response.text)
name = data['data']['card']['name']
sex = data['data']['card']['sex']
sign = data['data']['card']['sign']
level = data['data']['card']['level_info']['current_level']
authentication = data['data']['card']['Official']['title']
vip = data['data']['card']['vip']['vipType']
fans = data['data']['card']['fans']
if vip == 0:
    vip = '正式会员'
elif vip == 1:
    vip = '大会员'
else:
    vip = '年度大会员'
if authentication == "":
    authentication = '无'
if sign == '':
    sign = '无'
print('查询结果如下\n'
      '用户名称：%s\n'
      '用户UID：%s\n'
      '用户性别：%s\n'
      '用户签名：%s\n'
      '用户等级：%s\n'
      '用户认证：%s\n'
      '用户是否为大会员：%s\n'
      '用户粉丝：%s\n'
      %(name,uid,sex,sign,level,authentication,vip,fans))
polling_fans = input('是否轮询粉丝数？轮询请输入"1"，否则请退出：')
if polling_fans == '1':
    max_fans = input('检测是否达到指定粉丝数？检测请输入指定数字，否则请输入"0"：')
    max_fans = int(max_fans)
if max_fans != 0:
    emailaddr = input('是否需要在粉丝数达到%d个时发送邮件通知？需要请输入qq邮箱地址，不需要请留空：'%(max_fans))
if emailaddr != '':
    username = input('请输入邮件的收件人（无特殊要求可随意填写）：')
    passwd = input('请输入qq邮箱的smtp授权码，如不知道可在搜索引擎搜索“qq邮箱开启smtp”：')
    while 1:
        response = requests.get('https://api.bilibili.com/x/web-interface/card?mid=%d'%(uid))
        data = json.loads(response.text)
        fans = data['data']['follower']
        if fans < max_fans:
            if fans-last_fans > 0:
                print('当前粉丝数：%d,与上一秒相比增加了%d个，未达到指定的%d个粉丝标准,距离%d个粉丝还差%d个'%(fans,fans - last_fans,max_fans,max_fans,max_fans - fans))
            elif fans-last_fans < 0:
                print('当前粉丝数：%d,与上一秒相比减少了%d个，未达到指定的%d个粉丝标准,距离%d个粉丝还差%d个'%(fans,last_fans - fans,max_fans,max_fans,max_fans - fans))
            else:
                print('当前粉丝数：%d,与上一秒相比无变化，未达到指定的%d个粉丝标准,距离%d个粉丝还差%d个'%(fans,max_fans,max_fans,max_fans - fans))
        else:
            if fans-last_fans > 0:
                print('当前粉丝数：%d,与上一秒相比增加了%d个，已达到指定的%d个粉丝标准'%(fans,fans - last_fans,max_fans))
                if emailaddr != "":
                    emailsend()
                    break
            elif fans-last_fans < 0:
                print('当前粉丝数：%d,与上一秒相比减少了%d个，已达到指定的%d个粉丝标准'%(fans,last_fans - fans,max_fans))
                if emailaddr != "":
                    emailsend()
                    break
            else:
                print('当前粉丝数：%d,与上一秒相比无变化，已达到指定的%d个标准'%(fans,max_fans))
                if emailaddr != "":
                    emailsend()
                    break
        last_fans = fans
        time.sleep(1)
