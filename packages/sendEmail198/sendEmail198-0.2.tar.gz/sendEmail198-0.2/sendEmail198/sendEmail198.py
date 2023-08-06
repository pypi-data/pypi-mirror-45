import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
 
'''
实例化 依次传入发送者邮箱与密码(SMTP授权码)
默认显示发件人信息

自行构造字典后传入
包含标题 内容 收件人
附件省略或为列表

'''
class Email():
    def __init__(self,sender,password,conceal = False):
        self.sender = sender
        self.password = password
        self.conceal = conceal

    def send(self,info): 
        try:
            #构造信息
            msg=MIMEMultipart()

            if not 'subject' in info:
                info['subject'] = ''
            if not 'content' in info:
                info['content'] = ''
                
            content=MIMEText(info['content'],'plain','utf-8')
            msg.attach(content)

            if 'attachment' in info:
                for item in info['attachment']:
                    if item[-3:] == 'jpg' or item[-3:] == 'png':
                        img = MIMEImage(open(item, 'rb').read(), _subtype='octet-stream')
                        img.add_header('Content-Disposition', 'attachment', filename=item)
                        msg.attach(img)
                    else:
                        file = MIMEApplication(open(item, 'rb').read())
                        file.add_header('Content-Disposition', 'attachment', filename=item)
                        msg.attach(file)
        
            if not self.conceal:
                msg['From'] = formataddr([" ",self.sender])  # 发件人邮箱昵称、邮箱
                
            #msg['To'] = formataddr([" ",receiver])     # 收件人昵称、邮箱 (昵称没用)
            msg['Subject'] = info['subject']               # 邮件的标题
     
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 实例化 发件人邮箱中的SMTP服务器 端口为465
            server.login(self.sender, self.password)  
            server.sendmail(self.sender,[info['receiver']],msg.as_string())  #发送
            server.quit()  # 关闭连接

            return True
        except Exception as e:
            print(e)
            return False
 
if __name__ == '__main__':
    dic = {}
    #dic['subject'] = '标题'
    #dic['content'] = '内容'
    #dic['attachment'] = ['picture.png','readme.txt','sendEmail.py']
    dic['receiver'] = '1799853523@qq.com'
    sender='1799853523@qq.com'    # 发件人邮箱账号
    password = 'pjzsiznisldgdhch'    # 发件人邮箱密码(授权码)

    email = Email(sender,password,conceal = True)
    if email.send(dic):
        print('发送成功')
    else:
        print('发送失败')
