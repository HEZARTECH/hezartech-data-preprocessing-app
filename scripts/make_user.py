#!/usr/bin/env python3
# author: github.com/yigitoo
from pwinput import pwinput
import pymongo as pm
import bcrypt

import os

# Load modules
__import__('dotenv').load_dotenv()
client = pm.MongoClient(os.getenv('DB_URI'))
db = client.get_database('hezartech')


def make_user():
    # Input credentials...

    fullname: str = input("Write your fullname (e.g Yiğit GÜMÜŞ): ")
    email: str = input('Write you email adress (e.g gumusyigit101@gmail.com): ')
    password: str = pwinput(prompt="You password: ")

    # Save to DB
    result = db.users.find_one({
        "email": email
    })

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if result is None:
        db.users.insert_one({
            "name": fullname,
            "email": email,
            "password": hashed_password,
        })

if __name__ == '__main__':
    make_user()
