import datetime
import uuid


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
        if username != '' or username != ' ':
            password = input('enter your password: ')
            if password != '' or password != ' ':
                phone_number = input('enter your phone number or leave it blank: ')
                if phone_number.isdigit() and len(phone_number) == 11 or phone_number == '':
                    id = uuid.UUID
                    birthday, birthmonth, birthyear = input('enter your birthday d m yyyy: ').split()
                    birthdate = datetime.datetime(int(birthyear), int(birthmonth), int(birthday))
                    date_joined = datetime.datetime.now()
                else:
                    return 'wrong phone number'
            else:
                return 'wrong password'
        else:
            return 'wrong phone number'
        signed_up = True
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.id = id
        self.birthdate = birthdate
        self.birthdate = birthdate
        self.date_joined = date_joined
        if signed_up:
            return f'you account has been created successfully'
