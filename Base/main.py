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
        print("Getting News from ", category_name)
        news_cards = json.loads(NewsApi.getNews(category_name))
        data.append("\n\t\t\t\t========================= " + category_name.upper() + ' =========================\n\n')

        for ele in news_cards:
            # print(ele)
            # print("-----------------\n")

            data.append(ele['title'] + '\n')
            data.append(ele['date'] + ' ' + ele['time'] + '\n\n')

            data.append(ele['content'] + "\n\n")
            data.append('Read More: ' + ele['readMoreUrl'] + '\n')
            data.append("-----------------------------------\n\n")
    return data


# todo: improve verbose
def start(email, psswd, cat=['all'], test=0):
    data = getNews(cat=cat)
    domain_provider = re.findall("(.*)@(.*)\.(.*)", email)[0][1]

    try:
        conn = smtplib.SMTP(provider_list[domain_provider][0],
                            provider_list[domain_provider][1])
    except KeyError:
        if test:
            traceback.print_exc()
        print("Email Provider detected: ", domain_provider)
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
