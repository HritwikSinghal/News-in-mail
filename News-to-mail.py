import json
import os
import traceback
from base64 import b64decode
from base64 import b64encode

from Base import main


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
        email = input("Enter Email\n")
        psswd = input("Enter Password\n")
        creds = {}
        creds['email'] = str(b64encode(email.encode('utf-8')))
        creds['password'] = str(b64encode(psswd.encode('utf-8')))

        print("Saving Login details...")
        with open(path, 'w+') as fp:
            json.dump(creds, fp)
        print("Creds Saved.")

    print("Login details Loaded.")
    return email, psswd


def get_cat(test=0):
    path = os.path.join(os.getcwd(), "Base", "cat.json")
    success = 0
    if os.path.isfile(path):
        print("Loading Categories...")
        with open(path, 'r') as fp:
            try:
                cat = json.load(fp)
                success = 1
            except:
                if test:
                    traceback.print_exc()
                success = 0

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
        cat = [all_cat[x] for x in select_cat]

        save_cat = int(input("\nDo you want to save Categories so next time i wont ask from you?\n"
                             "1 == Yes"
                             " 0 == No\n"))
        if save_cat:
            print("Saving Categories...")
            with open(path, 'w+') as fp:
                json.dump(cat, fp)
            print("Categories Saved.")

    print("Categories Loaded.")
    print("\nSelected Categories: ", cat)
    print("if you want to change Categories, Go inside 'Base' folder and delete file 'cat.json' or 'cat'\n")
    return cat


def start(test=0):
    print("""
          _   _                     _______      __  __       _ _ 
         | \ | |                   |__   __|    |  \/  |     (_) |
         |  \| | _____      _____     | | ___   | \  / | __ _ _| |
         | . ` |/ _ \ \ /\ / / __|    | |/ _ \  | |\/| |/ _` | | |
         | |\  |  __/\ V  V /\__ \    | | (_) | | |  | | (_| | | |
         |_| \_|\___| \_/\_/ |___/    |_|\___/  |_|  |_|\__,_|_|_|
                                                                
                                                        """)

    email, psswd = get_cred(test=test)
    cat = get_cat(test=test)
    main.start(email, psswd, cat, test=test)

    print('''
            \n\t\t\tThank you for Using this program....
            By Hritwik
            https://github.com/HritwikSinghal
        ''')


if os.path.isfile('Base/test_bit'):
    test = 1
else:
    test = 0

start(test=test)

# todo: add scheduler
