from users import User
import hashlib
import getpass
import re


def logged_in():
    user = User(None, None, None, None, None, None)
    while True:
        login_status = input('press 2 to login, 1 for signup, to close this press 0: ')
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
                pass
        elif login_status == '0':
            break


logged_in()
