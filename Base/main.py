import json
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

    # conn = smtplib.SMTP('smtp.gmail.com', 587) # for gmail
    conn = smtplib.SMTP('smtp.office365.com', 587)  # for outlook

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
