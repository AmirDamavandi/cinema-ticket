import datetime
import uuid
import re
import getpass
import json
import os
import random
import hashlib

class BankAccount:
    def __init__(self, full_name, card_number, cvv2, exp_year, exp_month, pin, balance):
        self.full_name = full_name
        self.card_number = card_number
        self.cvv2 = cvv2
        self.exp_year = exp_year
        self.exp_month = exp_month
        self.pin = pin
        self.balance = balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return 'successful transaction'
        else:
            return 'insufficient inventory'

    def deposit(self, amount):
        self.balance += amount


class User:
    def __init__(self, username, password, phone_number, id, birthdate, date_joined, plans):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.id = id
        self.birthdate = birthdate
        self.birthdate = birthdate
        self.date_joined = date_joined
        self.plans = plans

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
                        plans = None
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
        self.plans = plans
        if signed_up:
            users_information = {
                'username': self.username,
                'password': self.password,
                'phone_number': self.phone_number,
                'id': str(self.id),
                'birthdate': str(self.birthdate),
                'date_joined': str(self.date_joined),
                'plans': self.plans

            }
            with open(f'users_information/{username.lower()}', 'w+', encoding='utf-8') as information:
                json.dump(users_information, information)
            information.close()
            return 'your account has been created successfully'

    def login(self):
        username = input('enter your username: ').lower()
        password = getpass.getpass('enter your password: ')
        user_exist = os.listdir('users_information')

        def legged_in():
            logged_in = False
            try:
                with open(f'users_information/{username}', 'r', encoding='utf-8') as login_information:
                    matching_information = json.load(login_information)
                if username == str(matching_information['username']).lower() and password == matching_information[
                    'password']:
                    logged_in = True
                if logged_in:
                    print('logged in successfully!')
                    while True:
                        options = input('security and privacy: 1, to get a plan 2 and 0 to log out: ')
                        if options == '1':
                            while True:
                                security_options = input('to check your information press 1, to change information '
                                                         'press 2, press 0 to back: ')
                                if security_options == '1':
                                    hash_pass = hashlib.sha256(matching_information['password'].encode('utf-8'))
                                    print(f'username: {matching_information['username']}'
                                          f'\npassword: {hash_pass.hexdigest()}'
                                          f'\nphone number: {matching_information['phone_number']}'
                                          f'\nid: {matching_information['id']}'
                                          f'\nbirthdate: {matching_information['birthdate']}'
                                          f'\ndate joined: {matching_information['date_joined']}'
                                          f'\nplans: {matching_information['plans']}')
                                elif security_options == '2':
                                    while True:
                                        information_changing = input(
                                            'to change your username 1, to change phone number '
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
                                                username_pattern = r'^[a-zA-Z0-9_.]+$'
                                                unique = os.listdir('users_information')
                                                username_in_list = new_username.lower() in unique
                                                if (re.match(username_pattern, new_username)
                                                        and new_username.lower() != str(
                                                            matching_information['username']).lower()
                                                        and not username_in_list):
                                                    user_information = {
                                                        'username': new_username,
                                                        'password': matching_information['password'],
                                                        'phone_number': matching_information['phone_number'],
                                                        'id': matching_information['id'],
                                                        'birthdate': matching_information['birthdate'],
                                                        'date_joined': matching_information['date_joined'],
                                                        'plans': matching_information['plans']
                                                    }
                                                    os.chdir('users_information')
                                                    os.renames(matching_information['username'], new_username.lower())
                                                    os.chdir('..')
                                                    with open(f'users_information/{new_username}', 'w',
                                                              encoding='utf-8') as username_changing:
                                                        json.dump(user_information, username_changing)
                                                    username_changing.close()
                                                    matching_information = user_information
                                                    username_changed = True
                                                    print('your username has been changed successfully')
                                                    break
                                                elif not re.match(username_pattern, new_username):
                                                    print(f'"{new_username}" isn\'t a correct username')
                                                elif new_username.lower() == str(
                                                        matching_information['username']).lower():
                                                    print(f'"{new_username}" is current username')
                                                elif username_in_list:
                                                    print(f'"{new_username}" has already taken')

                                        elif information_changing == '2':
                                            while True:
                                                new_phone_number = input(
                                                    f'your current "{matching_information['phone_number']}", enter new '
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
                                                        'plans': matching_information['plans']
                                                    }
                                                    with open(f'users_information/{matching_information['username']}',
                                                              'w',
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
                                                current_password = getpass.getpass(
                                                    'enter your current password, press 0 '
                                                    'to cancel: ')
                                                if current_password == '0':
                                                    break
                                                if current_password == matching_information['password']:
                                                    password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{8,200}$'
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
                                                                'plans': matching_information['plans']
                                                            }
                                                            with open(
                                                                    f'users_information/{matching_information['username']}',
                                                                    'w',
                                                                    encoding='utf-8') as password_changing:
                                                                json.dump(user_information, password_changing)
                                                            password_changing.close()
                                                            matching_information = user_information
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
                        elif options == '2':
                            while True:
                                bronze_plan_price = 20
                                silver_plan_price = 50
                                gold_plan_price = 150
                                select_a_plan = input(f'1-bronze price : {bronze_plan_price}\n'
                                                      f'2-silver price : {silver_plan_price}\n'
                                                      f'3-gold price : {gold_plan_price}\n'
                                                      f'choose one of above, to get back press 0: ')
                                def payment():
                                    full_name = input('your full name on card: ')
                                    card_number = input('enter your card number: ')
                                    if card_number.isdigit() and len(card_number) == 16:
                                        cvv2 = input('enter cvv2: ')
                                        if cvv2.isdigit() and len(cvv2) == 3 or len(cvv2) == 4:
                                            expire_month, expire_year = input(
                                                'enter expire month and expire year (mm yy): ').split()
                                            if str(expire_year).isdigit() and len(expire_year) == 2 and str(
                                                    expire_month).isdigit() and len(expire_month) == 2:
                                                expire_month_pattern = r'(0[1-9]|[0-2])'
                                                expire_year_pattern = r'\d{2}'
                                                if re.match(expire_month_pattern, expire_month) and re.match(
                                                        expire_year_pattern, expire_month):
                                                    card_pin = input('enter your card pin: ')
                                                    if card_pin.isdigit() and 4 <= len(card_pin) <= 6:
                                                        balance = random.randint(0, 1000)
                                                        user_bank_account = BankAccount(full_name, card_number, cvv2,
                                                                                        expire_year, expire_month,
                                                                                        card_pin, balance)
                                                        if select_a_plan == '1':
                                                            if (user_bank_account.withdraw(bronze_plan_price) ==
                                                                    'successful transaction'
                                                                and matching_information['plans'] != 'Bronze plan'

                                                            ):
                                                                user_information = {
                                                                    'username': matching_information['username'],
                                                                    'password': matching_information['password'],
                                                                    'phone_number': matching_information['phone_number'],
                                                                    'id': matching_information['id'],
                                                                    'birthdate': matching_information['birthdate'],
                                                                    'date_joined': matching_information['date_joined'],
                                                                    'plans': 'Bronze plan'
                                                                }
                                                                with open(f'users_information/{matching_information[
                                                                    'username']}','w', encoding='utf-8') as bronze_plan:
                                                                    json.dump(user_information, bronze_plan)
                                                                bronze_plan.close()
                                                                matching_information['plans'] = 'Bronze plan'
                                                                return 'you got the plan successfully'
                                                            else:
                                                                return 'insufficient inventory'
                                                        elif select_a_plan == '2':
                                                            if (user_bank_account.withdraw(silver_plan_price) ==
                                                                    'successful transaction'
                                                                and matching_information['plans'] != 'Silver plan'

                                                            ):
                                                                user_information = {
                                                                    'username': matching_information['username'],
                                                                    'password': matching_information['password'],
                                                                    'phone_number': matching_information['phone_number'],
                                                                    'id': matching_information['id'],
                                                                    'birthdate': matching_information['birthdate'],
                                                                    'date_joined': matching_information['date_joined'],
                                                                    'plans': 'Silver plan'
                                                                }
                                                                with open(f'users_information/{matching_information[
                                                                        'username']}','w', encoding='utf-8') as silver_plan:
                                                                    json.dump(user_information, silver_plan)
                                                                silver_plan.close()
                                                                matching_information['plans'] = 'Silver plan'
                                                                return 'you got the plan successfully'
                                                            else:
                                                                return 'insufficient inventory'
                                                        elif select_a_plan == '3':
                                                            if (user_bank_account.withdraw(gold_plan_price) ==
                                                                    'successful transaction'
                                                                and matching_information['plans'] != 'Gold plan'

                                                            ):
                                                                user_information = {
                                                                    'username': matching_information['username'],
                                                                    'password': matching_information['password'],
                                                                    'phone_number': matching_information['phone_number'],
                                                                    'id': matching_information['id'],
                                                                    'birthdate': matching_information['birthdate'],
                                                                    'date_joined': matching_information['date_joined'],
                                                                    'plans': 'Gold plan'
                                                                }
                                                                with open(f'users_information/{matching_information[
                                                                        'username']}','w', encoding='utf-8') as gold_plan:
                                                                    json.dump(user_information, gold_plan)
                                                                gold_plan.close()
                                                                matching_information['plans'] = 'Gold plan'
                                                                return 'you got the plan successfully'
                                                            else:
                                                                return 'insufficient inventory'
                                                        else:
                                                            return 'invalid choice'
                                                    else:
                                                        return 'card pin is incorrect'
                                                else:
                                                    return 'expire date is incorrect'
                                            else:
                                                return 'expire date is incorrect'
                                        else:
                                            return 'cvv2 is incorrect'
                                    else:
                                        return 'card number is incorrect'
                                if (
                                    select_a_plan == '1' or select_a_plan.lower() == 'bronze plan'
                                ):
                                    if matching_information['plans'] != 'Bronze plan':
                                        print(payment())
                                    else:
                                        print('it\'s your current plan')
                                elif (
                                    select_a_plan == '2' or select_a_plan.lower() == 'silver plan'
                                ):
                                    if matching_information['plans'] != 'Silver plan':
                                        print(payment())
                                    else:
                                        print('it\'s your current plan')
                                elif (
                                    select_a_plan == '3' or select_a_plan.lower() == 'gold plan'
                                ):
                                    if matching_information['plans'] != 'Gold plan':
                                        print(payment())
                                    else:
                                        print('it\'s your current plan')
                                elif select_a_plan == '0':
                                    break
                                else:print('invalid choice')
                        elif options == '0':
                            break
                else:
                    print('your password does not match')
            except FileNotFoundError:
                print('there\'s no user with this information')

        return legged_in()
