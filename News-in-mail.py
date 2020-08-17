import json
import os
import traceback
from base64 import b64decode
from base64 import b64encode

import schedule

from Base import main

email = ''
psswd = ''
cat = []


def input_creds(email, path, psswd, test=0):
    email = input("Enter Email\n")
    psswd = input("Enter Password\n")

    creds = {}
    creds['email'] = str(b64encode(email.encode('utf-8')))
    creds['password'] = str(b64encode(psswd.encode('utf-8')))

    print("Saving Login details...")
    try:
        with open(path, 'w+') as fp:
            json.dump(creds, fp)
        print("Creds Saved.")
    except:
        if test:
            traceback.print_exc()

        print("There was some error in storing Credentials.....")

    return email, psswd


def get_cred(test=0):
    path = os.path.join(os.getcwd(), "Base", "creds.json")
    success = 0
    if os.path.isfile(path):
        print("Loading Login details...")
        with open(path, 'r') as fp:
            try:
                creds = json.load(fp)
                success = 1

                email = creds['email']
                psswd = creds['password']

                email = bytes(email[2:len(email) - 1], encoding='utf-8')
                psswd = bytes(psswd[2:len(psswd) - 1], encoding='utf-8')

                email = b64decode(email).decode('utf-8')
                psswd = b64decode(psswd).decode('utf-8')
            except:
                if test:
                    traceback.print_exc()
                success = 0

    if not success:
        email, psswd = input_creds(email, path, psswd, test)

    print("Login details Loaded.")
    return email, psswd


def get_cat_and_period(test=0):
    path = os.path.join(os.getcwd(), "Base", "categories.json")
    success = 0

    # load file containing categories and period
    if os.path.isfile(path):
        print("\nLoading Categories & Period...")
        with open(path, 'r') as fp:
            try:
                json_data = json.load(fp)

                categories = json_data['categories']
                period = json_data['period']

                success = 1
            except:
                if test:
                    traceback.print_exc()
                success = 0

    # if cannot load, ask them from user
    if not success:
        print("\nSelect from below Categories, for multiple Categories enter corresponding numbers with spaces")

        all_cat = {
            1: 'national',
            2: 'business',
            3: 'sports',
            4: 'world',
            5: 'politics',
            6: 'technology',
            7: 'startup',
            8: 'entertainment',
            9: 'miscellaneous',
            10: 'hatke',
            11: 'science',
            12: 'automobile'
        }

        for item in all_cat:
            print(item, ' : ', all_cat[item])

        select_cat = list(set(map(int, input().split())))
        categories = [all_cat[x] for x in select_cat]

        # input period
        period = int(input("Enter period to mail (after how many hours should i re-mail news) \n"))

        # saving them
        save_cat_flag = int(input("\nDo you want to save Categories & Period so next time i wont ask from you?\n"
                                  "1 == Yes"
                                  " 0 == No\n"))
        if save_cat_flag:
            print("Saving Categories & Period...")
            with open(path, 'w+') as fp:
                json.dump(categories, fp)
            print("Saved.")

    print("Categories & Period Loaded.")
    print("\nSelected Categories: ", categories)
    print("Selected Perieod: ", period)
    print("if you want to change Categories & Period, Go inside 'Base' folder and delete file 'categories.json'\n")

    return categories, period


def start_main():
    main.start(email, psswd, cat, test=test)


def start(test=0):
    global cat, email, psswd

    print("""
         __  ___                   _______       ___  ___       ___
         | \ | |                   |_   _|       |  \/  |     (_) |
         |  \| | _____      _____    | |  _ __   | \  / | __ _ _| |
         | . ` |/ _ \ \ /\ / / __|   | | | '_ \  | |\/| |/ _` | | |
         | |\  |  __/\ V  V /\__ \  _| |_| | | | | |  | | (_| | | |
         |_| \_|\___| \_/\_/ |___/ |_____|_| |_| |_|  |_|\__,_|_|_|
                                                        """)

    email, psswd = get_cred(test=test)
    cat, x = get_cat_and_period(test=test)

    start_main()
    schedule.every(x).hours.do(start_main)

    try:
        while True:
            schedule.run_pending()
    except:
        if test:
            traceback.print_exc()
        print("There was some error in scheduling task. Please open issue on github")

    print('''
            \n\t\t\tThank you for Using this program....
            By Hritwik
            https://github.com/HritwikSinghal
        ''')
    exit(0)


if __name__ == "__main__":
    if os.path.isfile('Base/test_bit'):
        test = 1
    else:
        test = 0

    start(test=test)

# todo: None (You can suggest!)
