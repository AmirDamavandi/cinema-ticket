from users import User


def logged_in():
    user = User(None, None, None, None, None, None)
    while True:
        login_status = input('press 2 to login, 1 for signup, to close this press 0: ')
        if login_status == '1':
            sign_up = user.sign_up()
            print(sign_up)
        elif login_status == '2':
            login = user.login()
            print(login)
        elif login_status == '0':
            break


logged_in()
