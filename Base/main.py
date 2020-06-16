import re
import os
import json
import platform
from Base import NewsApi


def getNews():
    pass


def start(email, psswd, test=0):
    print(email, psswd)
    news = []

    data = json.loads(NewsApi.getNews('all'))
    for ele in data:
        print(ele)
        print("****************")
