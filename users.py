import datetime
import uuid
import re
import getpass
import json
import os

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
            unique_username = os.listdir('users_information')
            if not username.lower() in unique_username:
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
                return 'this username already exist'
        else:
            return 'incorrect username'
        signed_up = True
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.id = id
        self.birthdate = birthdate
        self.date_joined = date_joined
        if signed_up:
            users_information = {
                'username': self.username,
                'password': self.password,
                'phone_number': self.phone_number,
                'id': str(self.id),
                'birthdate': str(self.birthdate),
                'date_joined': str(self.date_joined),

            }
            with open(f'users_information/{username.lower()}', 'w+', encoding='utf-8') as information:
                json.dump(users_information, information)
            return 'your account has been created successfully'

    def login(self):
        username = input('enter your username: ').lower()
        password = getpass.getpass('enter your password: ')
        user_exist = os.listdir('users_information')
        try:
            with open(f'users_information/{username}', 'r', encoding='utf-8') as login_information:
                matching_information = json.load(login_information)
            if username == str(matching_information['username']).lower() and password == matching_information['password']:
                logged_in = True
                while True:
                    options = input('logged in successfully! \nsecurity and privacy: 1, press 0 to log out: ')
                    if options == '1':
                        while True:
                            security_options = input('to check your information press 1, to change information '
                                                     'press 2, press 0 to back: ')
                            if security_options == '1':
                                print(f'username: {matching_information['username']}'
                                      f'\npassword: {matching_information['password']}'
                                      f'\nphone number: {matching_information['phone_number']}'
                                      f'\nid: {matching_information['id']}'
                                      f'\nbirthdate: {matching_information['birthdate']}'
                                      f'\ndate joined: {matching_information['date_joined']}')
                            elif security_options == '2':
                                while True:
                                    information_changing = input('to change your username 1, to change phone number '
                                                                 '2, to change password 3, press 0 to back: ')
                                    if information_changing == '1':
                                        while True:
                                            new_username = input(
                                                f'your current username "{matching_information['username']}" '
                                                f'enter new one, press 0 to'
                                                f' cancel it: ')
                                            username_changed = False
                                            if new_username == '0':
                                                break
                                            try:
                                                username_pattern = r'^[a-zA-Z0-9_.]+$'
                                                unique_username = os.listdir('users_information')
                                                if (re.match(username_pattern, new_username)
                                                        and new_username.lower() != str(matching_information['username']).lower()
                                                ):
                                                    user_information = {
                                                        'username': new_username,
                                                        'password': matching_information['password'],
                                                        'phone_number': matching_information['phone_number'],
                                                        'id': matching_information['id'],
                                                        'birthdate': matching_information['birthdate'],
                                                        'date_joined': matching_information['date_joined'],
                                                    }
                                                    os.chdir('users_information')
                                                    os.renames(matching_information['username'], new_username.lower())
                                                    os.chdir('..')
                                                    with open(f'users_information/{new_username}', 'w', encoding='utf-8') as username_changing:
                                                        json.dump(user_information, username_changing)
                                                    username_changing.close()
                                                    matching_information = user_information
                                                    username_changed = True
                                                    print('your username has been changed successfully')
                                                    break
                                                elif not re.match(username_pattern, new_username):
                                                    print(f'"{new_username}" isn\'t a correct username')
                                                elif new_username.lower() == str(matching_information['username']).lower():
                                                    print(f'"{new_username}" is current username')
                                            except FileExistsError:
                                                print(f'"{new_username}" already taken')

                                    elif information_changing == '2':
                                        while True:
                                            new_phone_number = input(f'your current "{matching_information['phone_number']}", enter new '
                                                                     f'one, press 0 to cancel it: ')
                                            phone_number_changed = False
                                            if new_phone_number == '0':
                                                break
                                            if matching_information['phone_number'] is not None:
                                                if new_phone_number == matching_information['phone_number']:
                                                    print(f'"{new_phone_number}" is current phone number')
                                            if (new_phone_number.isdigit() and len(new_phone_number) == 11
                                                    and new_phone_number != matching_information['phone_number']
                                            ):
                                                user_information = {
                                                    'username': matching_information['username'],
                                                    'password': matching_information['password'],
                                                    'phone_number': new_phone_number,
                                                    'id': matching_information['id'],
                                                    'birthdate': matching_information['birthdate'],
                                                    'date_joined': matching_information['date_joined'],
                                                }
                                                with open(f'users_information/{matching_information['username']}', 'w',
                                                          encoding='utf-8') as phone_number_changing:
                                                    json.dump(user_information, phone_number_changing)
                                                phone_number_changing.close()
                                                matching_information = user_information
                                                phone_number_changed = True
                                                print('your phone number has been changed successfully')
                                                break
                                            else:
                                                if new_phone_number != matching_information['phone_number']:
                                                    print(f'"{new_phone_number}" isn\'t a correct phone number')
                                    elif information_changing == '3':
                                        while True:
                                            changed_password = False
                                            current_password = getpass.getpass('enter your current password, press 0 '
                                                                               'to cancel: ')
                                            if current_password == '0':
                                                break
                                            if current_password == matching_information['password']:
                                                password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{8,}$'
                                                new_password = getpass.getpass('enter your new password: ')
                                                if re.match(password_pattern, new_password):
                                                    confirm_password = getpass.getpass('confirm your password: ')
                                                    if confirm_password == new_password:
                                                        user_information = {
                                                            'username': matching_information['username'],
                                                            'password': confirm_password,
                                                            'phone_number': matching_information['phone_number'],
                                                            'id': matching_information['id'],
                                                            'birthdate': matching_information['birthdate'],
                                                            'date_joined': matching_information['date_joined'],
                                                        }
                                                        with open(f'users_information/{matching_information['username']}',
                                                                'w',
                                                                encoding='utf-8') as password_changing:
                                                            json.dump(user_information, password_changing)
                                                        changed_password = True
                                                        print('your password has changed successfully')
                                                        break
                                                    else:
                                                        print('password does not match')
                                                else:
                                                    print('password is incorrect')
                                            else:
                                                print('password is wrong')
                                    elif information_changing == '0':
                                        break
                            elif security_options == '0':
                                break
                    elif options == '0':
                        break
            else:
                return 'your password does not match'
        except FileNotFoundError:
            return 'there\'s no user with this information'


