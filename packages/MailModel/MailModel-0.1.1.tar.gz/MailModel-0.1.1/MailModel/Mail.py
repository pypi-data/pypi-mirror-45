#coding:utf-8
import smtplib  
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(smtp_address = 'smtp.163.com', smtp_port = 25, \
	my_sender = '...@163.com', my_password = '...', my_toer = '...@qq.com', \
	msg_fromname = '163', msg_toname = 'QQ', msg_subject = '模型训练情况', \
	msg_context = '模型已训练完成！ The model training is finished !'):

    ret = True
    try:
        msg = MIMEText(msg_context, 'plain', 'utf-8')
        msg['From'] = formataddr([msg_fromname, my_sender]) 
        msg['To'] = formataddr([msg_toname, my_toer]) 
        msg['Subject'] = msg_subject 

        server = smtplib.SMTP(smtp_address, smtp_port) 
        server.login(my_sender, my_password) 
        server.sendmail(my_sender, [my_toer,], msg.as_string())
        server.quit()

    except Exception:   
        ret = False
    
    if ret:
        print("Success ! Wait about twenty seconds to receive the mail.")
    else:
        print("Failed to send !!!")

# mail()


