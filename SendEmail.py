import smtplib
from email.message import EmailMessage

my_mail = "voiceassistant.demo21@gmail.com"
my_pass = "!voice-assistant#2021"

def send_mail(subject, to, body):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = my_mail
    msg['To'] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(my_mail, my_pass)
        smtp.send_message(msg)