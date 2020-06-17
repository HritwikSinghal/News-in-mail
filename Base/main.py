import json
import re
import smtplib
from email.mime.text import MIMEText
import traceback

from Base import NewsApi


def start(email, psswd, test=0):
    news_cards = json.loads(NewsApi.getNews('all'))

    data = []
    for ele in news_cards:
        # print(ele)
        # print("-----------------\n")

        data.append('\033' + ele['title'] + '\033' + '\n')
        data.append(ele['date'] + ' ' + ele['time'] + '\n\n')

        data.append(ele['content'] + "\n\n")
        data.append('Read More: ' + ele['readMoreUrl'] + '\n')
        data.append("-----------------------------------\n\n")

    gmail = 'smtp.gmail.com'
    outlook = 'smtp.office365.com'
    email_provider = re.findall("(.*)@(.*)\.(.*)", email)[0][1]
    # print(re.findall("(.*)@(.*)\.(.*)", email))

    if email_provider == 'gmail':
        conn = smtplib.SMTP(gmail, 587)
    elif email_provider == 'outlook':
        conn = smtplib.SMTP(outlook, 587)
    else:
        print("Email provider not supported. Please open issue on Github..")
        return

    # start TLS for security
    conn.starttls()

    code, extra = conn.ehlo()
    if int(code) not in range(200, 300):
        print("Error Establishing Connection to your mail.")
        print("Please delete 'creds.json' file in 'Base' folder"
              "and try again with correct credentials.")
        return

    # Authentication
    conn.login(email, psswd)

    # message to be sent
    SUBJECT = "News delivered to your mailbox!\n\n"
    TEXT = ''.join(data)

    # https://stackoverflow.com/questions/1429147/python-3-smtplib-send-with-unicode-characters
    msg = MIMEText(TEXT.encode('utf-8'), _charset='utf-8')
    msg['Subject'] = SUBJECT
    msg['From'] = email
    msg['To'] = email

    print("Sending News...")
    try:
        # sending the mail
        conn.sendmail(email, email, msg.as_string())
        print("News Sent!")
    except:
        if test:
            traceback.print_exc()
        print("There was Some error in Sending mail...")

    # terminating the session
    conn.quit()
