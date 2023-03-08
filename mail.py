import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

#The mail addresses and password
def send(toadrr ,subject ,message_content):
    sender_address = "secureddss@gmail.com"
    sender_pass = 'project@123'
    receiver_address = [toadrr]
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ''.join(receiver_address)
    mail_content = f'''
    {message_content}
    
    Regards,
    Team DSS.
    '''

    message['Subject'] = subject
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls() #enable security
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()