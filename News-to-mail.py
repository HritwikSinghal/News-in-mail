import os
import json
import traceback
from base64 import b64encode, b64decode
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


def start(test=0):
    email, psswd = get_cred(test=test)
    print()
    main.start(email, psswd, test=test)


if os.path.isfile('Base/test_bit'):
    test = 1
else:
    test = 0

start(test=test)
