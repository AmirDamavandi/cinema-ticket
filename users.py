import datetime
import uuid
import re
import getpass


class User:
    def __init__(self, username, password, phone_number, id, birthdate, date_joined):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.id = id
        self.birthdate = birthdate
        self.birthdate = birthdate
        self.date_joined = date_joined

    def sign_up(self):
        signed_up = False
        username = input('enter your username: ')
        username_pattern = r'^[a-zA-Z0-9_.]+$'
        if re.match(username_pattern, username):
            password = getpass.getpass('enter your password: ')
            password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{8,}$'
            if re.match(password_pattern, password):
                phone_number = input('enter your phone number or leave it blank: ')
                if phone_number.isdigit() and len(phone_number) == 11 or phone_number == '':
                    if phone_number == '':
                        phone_number = None
                    id = uuid.uuid4()
                    try:
                        birthday, birthmonth, birthyear = input('enter your birthday d m yyyy: ').split()
                        birthdate = datetime.datetime(int(birthyear), int(birthmonth), int(birthday)).date()
                        date_joined = datetime.datetime.now().date()
                    except ValueError:
                        return 'incorrect birthdate'
                else:
                    return 'incorrect phone number'
            else:
                return 'incorrect password'
        else:
            return 'incorrect username'
        signed_up = True
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.id = id
        self.birthdate = birthdate
        self.birthdate = birthdate
        self.date_joined = date_joined
        if signed_up:
            return 'your account has been created successfully'

    def login(self):
        username = input('enter your username: ')
        password = getpass.getpass('enter your password: ')
        if username.lower() == str(self.username).lower() and password == self.password:
            return 'alright, you\'re in'
        else:
            return 'we could not find a user with this information'
