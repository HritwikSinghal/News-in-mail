import json
import re
import smtplib
import traceback
from email.mime.text import MIMEText

from Base import NewsApi

provider_list = {
    'gmail': ('smtp.gmail.com', 587),
    'outlook': ('smtp.office365.com', 587)
}


def getNews(cat=['all']):
    data = []

    for category_name in cat:
        print("Getting '" + category_name.title() + "' News")
        news_cards = json.loads(NewsApi.start(category_name))

        data.append("\n\t\t\t\t========================= " + category_name.upper() + ' =========================\n\n')
        for card in news_cards:
            details = ''

            details += card['title'] + '\n'
            details += card['date'] + ' ' + card['time'] + '\n\n'

            details += card['content'] + "\n\n"
            details += 'Read More: ' + card['readMoreUrl'] + '\n'
            details += "-----------------------------------\n\n"

            data.append(details)

    return data


def start(email, psswd, cat=['all'], test=0):
    data = getNews(cat=cat)

    # if test:
        # input("STOP")

    domain_provider = re.findall("(.*)@(.*)\.(.*)", email)[0][1]

    try:
        conn = smtplib.SMTP(provider_list[domain_provider][0],
                            provider_list[domain_provider][1])
    except KeyError:
        if test:
            traceback.print_exc()
        print("Email Provider detected: ", domain_provider)
        print("This Email provider is not supported. Please open issue on Github..")
        return

    # start TLS for security
    try:
        conn.starttls()
    except:
        if test:
            traceback.print_exc()
        print("There was some error in starting TLS connection")
        return

    code, extra = conn.ehlo()
    if int(code) not in range(200, 300):
        print("Error Establishing Connection to your mail.")
        print("Please delete 'creds.json' file in 'Base' folder"
              "and try again with correct credentials.")
        return

    # Authentication
    try:
        conn.login(email, psswd)
    except:
        if test:
            traceback.print_exc()
        print("There was some error in starting establishing connection")
        return

    # message to be sent
    SUBJECT = "News delivered in your mailbox!\n\n"
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
