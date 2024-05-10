from users import User
import hashlib
import getpass
import re


def logged_in():
    user = User(None, None, None, None, None, None)
    while True:
        login_status = input('press 2 to login, 1 for signup, to close this enter 0: ')
        hashing = hashlib.new('SHA256')
        hashing.update(str(user.password).encode())
        user_information = {'username': user.username, 'password': hashing.hexdigest(),
                            'phone_number': user.phone_number, 'id': user.id,
                            'birthdate': user.birthdate, 'date_joined': user.date_joined
                            }
        if login_status == '1':
            sign_up = user.sign_up()
            print(sign_up)
        elif login_status == '2':
            login = user.login()
            print(login)
            if login == 'alright, you\'re in':
                while True:
                    options = input('security and privacy: 1, press 0 to log out: ')
                    if options == '1':
                        while True:
                            security_options = input('to check your information press 1, to change information '
                                                     'press 2, to change password press 3, press 0 to back: ')
                            if security_options == '1':
                                print(f'username: {user_information['username']}'
                                      f'\npassword: {user_information['password']}'
                                      f'\nphone number: {user_information['phone_number']}'
                                      f'\nid: {user_information['id']}'
                                      f'\nbirthdate: {user_information['birthdate']}'
                                      f'\ndate joined: {user_information['date_joined']}')
                            elif security_options == '2':
                                while True:
                                    information_changing = input('to change your username 1, to change phone number '
                                                                 '2, to change password 3, press 0 to back: ')
                                    if information_changing == '1':
                                        while True:
                                            new_username = input(
                                                f'your current username "{user_information['username']}" '
                                                f'enter new one, press 0 to'
                                                f' cancel it: ')
                                            username_changed = False
                                            if new_username == '0':
                                                break
                                            username_pattern = r'^[a-zA-Z0-9_.]+$'
                                            if (re.match(username_pattern, new_username)
                                                    and new_username.lower() != str(user.username).lower()
                                            ):
                                                user.username = new_username
                                                user_information = {'username': user.username,
                                                                    'password': hashing.hexdigest(),
                                                                    'phone_number': user.phone_number, 'id': user.id,
                                                                    'birthdate': user.birthdate,
                                                                    'date_joined': user.date_joined
                                                                    }
                                                username_changed = True
                                                print('your username has been changed successfully')
                                                break
                                            elif not re.match(username_pattern, new_username):
                                                print(f'"{new_username}" isn\'t a correct username')
                                            elif new_username.lower() == str(user.username).lower():
                                                print(f'"{new_username}" is current username')
                                    elif information_changing == '2':
                                        while True:
                                            new_phone_number = input(f'your current "{user.phone_number}", enter new '
                                                                     f'one, press 0 to cancel it: ')
                                            phone_number_changed = False
                                            if new_phone_number == '0':
                                                break
                                            if user.phone_number is not None:
                                                if new_phone_number == user.phone_number:
                                                    print(f'"{new_phone_number}" is current phone number')
                                            if (new_phone_number.isdigit() and len(new_phone_number) == 11
                                                    and new_phone_number != user.phone_number
                                            ):
                                                user.phone_number = new_phone_number
                                                user_information = {'username': user.username,
                                                                    'password': hashing.hexdigest(),
                                                                    'phone_number': user.phone_number, 'id': user.id,
                                                                    'birthdate': user.birthdate,
                                                                    'date_joined': user.date_joined
                                                                    }
                                                phone_number_changed = True
                                                print('your phone number has been changed successfully')
                                                break
                                            else:
                                                if new_phone_number != user.phone_number:
                                                    print(f'"{new_phone_number}" isn\'t a correct phone number')
                                    elif information_changing == '0':
                                        break
                            elif security_options == '0':
                                break
                    elif options == '0':
                        break
        elif login_status == '0':
            break


logged_in()
