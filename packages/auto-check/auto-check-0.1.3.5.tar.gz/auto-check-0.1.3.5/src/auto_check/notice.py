import smtplib
import requests
from email.header import Header
from email.mime.text import MIMEText

sender_host = 'smtp.yeah.net'
#163用户名
sender_user = 'notification_only'
#密码(部分邮箱为授权码)
sender_pass = 'fornotify2019'
#邮件发送方邮箱地址
sender = 'notification_only@yeah.net'

title = '打卡通知'

def __send_via_mail(name, receiver, content, content_type='plain'):
    message = MIMEText(content, content_type, 'utf-8')
    message['Subject'] = Header(title, 'utf-8')
    message['From'] = 'Auto Checker<{0}>'.format(sender)
    message['To'] = '{1}'.format(name, receiver)

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        #连接到服务器
        smtpObj.connect(sender_host,25)
        #登录到服务器
        smtpObj.login(sender_user, sender_pass)
        #发送
        smtpObj.sendmail(sender, receiver, message.as_string())
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误


# 参考http://sc.ftqq.com/3.version
def __send_via_server_jyan(content, sckey, title=title):
    assert title is not None and content is not None and content != ''
    url = 'https://sc.ftqq.com/{0}.send?text={1}&desp={2}'.format(sckey, title, content)
    r = requests.get(url)
    print(r.content.decode('unicode-escape'))


def send(name, notice, content):
    if notice.__contains__('@'):
        __send_via_mail(name, notice, content)
    else:
        __send_via_server_jyan(content, notice)
    pass


if __name__ == '__main__':
    pass