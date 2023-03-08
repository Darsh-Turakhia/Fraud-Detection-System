import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

#The mail addresses and password
sender_address = "secureddss@gmail.com"
sender_pass = 'project@123'
receiver_address = ["dhairyavora19@gnu.ac.in"]
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = 'darshturakhia19@gnu.ac.in,dhairyavora19@gnu.ac.in'.join(receiver_address)
subject = ["OPT FOR LOGIN","SUSPICIOUS ACTIVITY","PASSWORD VERIFICATION","REQUESTED DOCUMENT","YOUR NEW PASSWORD","OTP FOR YOU"]

mail_content = f'''
Hello, your otp is,

'''

message['Subject'] = subject[random.randint(0,len(subject)-1)]
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))
#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls() #enable security
session.login(sender_address, sender_pass)
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()
print(f'Mail Sent')