from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

def sendEmails(subject, content, emailsList):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com" # Gmail smtp server

    senderMail = "meetingsummarizer@gmail.com"
    password ="Meeting@123"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server: 
        server.login(senderMail, password)
        for email in emailsList:

            msg = MIMEMultipart()

            msg['From'] = "meetingsummarizer@gmail.com" # Note : for sender email account turn on less secure apps

            msg['Subject'] = subject

            msg['To'] = email

            msg.attach(MIMEText(content, 'html'))

            server.sendmail(msg['From'], msg['To'], msg.as_string())


if __name__ == '__main__':
    emailList = [
        'namalashivacharan123@gmail.com',
        'dhadisaideepak786@gmail.com',
        'varunchintha321@gmail.com',
    ]
    sendMails('Test', 'Content of testing email', emailList)