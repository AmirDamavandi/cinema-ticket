from users import User
import hashlib

user = User(None, None, None, None, None, None)


def logged_in():
    while True:
        login_status = input('if you have an account enter 2, if not enter 1 for closing this enter 0: ')
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
                print(user_information)
        elif login_status == '0':
            break


logged_in()