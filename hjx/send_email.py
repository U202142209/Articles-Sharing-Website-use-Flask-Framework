import random
import smtplib
from email.mime.text import MIMEText
import time

def code():
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(6):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        upper_alpha = chr(random.randint(65, 90))
        lower_alpha = chr(random.randint(97, 122))
        # 从列表中 [], 返回一个随机元素
        num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


mail_host = 'smtp.qq.com'
port = 465

# send_by = '2869210303@qq.com'      # qq邮箱
# password = 'adnahbkerxzadege'      # 授权码

send_by='541689202@qq.com'      # 姐姐的小号邮箱
password='hcwufoalqlyebfeg'     # 姐姐的小号邮箱密码

# send_to = '2811958769@qq.com'     # zhaoqijia
# send_to='2869210303@qq.com'

def send_email(send_to,content):
	#创建了MIMEText类，相当于在写邮件内容，是plain类型
    message = MIMEText(content,'plain','utf-8')
    message["From"] = send_by
    message['To'] = send_to
    message['Subject'] = '验证码'
    #注意第三个参数，设置了转码的格式(我不设的时候会报解码错误)
    smpt = smtplib.SMTP_SSL(mail_host, port, 'utf-8')
    smpt.login(send_by,password)
    smpt.sendmail(send_by, send_to,message.as_string())
    print("发送成功")
    print(content)


def main(send_to):
    verificate_code=code()
    content=str('【好记性博客网站】你的验证码是；')+verificate_code+'  。如非本人操作，请忽略这条信息。'
    try:
        send_email(send_to,content)
        return verificate_code
    except:
        return False


if __name__ == '__main__':
    # res=main('2869210303@qq.com')
    # res=main('333@qq.com')
    sebt_to='2869210303@qq.com'
    try:
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        send_email(sebt_to,'【消息提醒】。您在好记性博客网站 http://101.43.229.177  登录成功。登录时间；%s'%now_time)
    except:
        print('error')