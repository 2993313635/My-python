import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#第三方SMTP服务，以qq邮箱为例（配置邮件服务器相关信息）
mail_host = 'smtp.qq.com'
mail_user = '2993313635@qq.com'
mail_pass = 'kgbdyetvkzfsdfeb'
mail_sender = '2993313635@qq.com'
mail_port = 465
mail_receivers = '210775951@qq.com'



#设置邮件内容格式——普通格式
massage = MIMEText("内容", "plain", "utf-8")  #plain残数指定邮件格式为纯文本

#————HTML格式
msg_html ="""
<p>邮件发送测试</p>
<p><a herf = "http://www.baidu.com">百度</a></p>
<table border = "1">
    <tr><th>Month</th><th>Savings</th></tr>
    <tr><td>January</td><td>$100</td></tr>
    <tr><td>February</td><td>$80</td></tr>
</table>

"""
message = MIMEText(msg_html, "html", "utf-8")

#————HTML格式（带图片与附件）
msg_html = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
<p>图片演示：</p>
<p><img src="cid:image_id_1"></p>
"""

msg_content = MIMEText(msg_html, "html", "utf-8")
msg_image = MIMEImage(open("../myplot.png","rb").read())
msg_image.add_header('Content-ID', '<image_id_1>')

message = MIMEMultipart("related")
message.attach(msg_content)
message.attach(msg_image)

#设置邮件的收发件与标题
message["From"] = mail_sender
message["To"] = mail_receivers
message["Subject"] = Header("这是标题","utf-8")

#邮件发送以及异常处理
try:
    #登录并发送邮件
    smtpobj = smtplib.SMTP_SSL(mail_host, mail_port)
    smtpobj.login(mail_user, mail_pass)
    smtpobj.sendmail(mail_sender, mail_receivers, message.as_string())
    print("发送成功")
except smtplib.SMTPException as e:
    print(e)