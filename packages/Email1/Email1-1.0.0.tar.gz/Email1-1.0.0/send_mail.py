from email.mime.text import MIMEText
import smtplib
msg = MIMEText('hello,send by python...', 'plain', 'utf-8')
from_addr = input('From: ')
password = input('Password: ')
smtp_server = input('SMTP server: ')
to_addr = input('To: ')
server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit() 