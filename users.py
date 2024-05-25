import datetime
import uuid
import re
import getpass
import json
import os
import random
import hashlib
from abc import ABC, abstractmethod
import jdatetime


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


class AbstractUser(ABC):
    def __init__(self, username, password, phone_number, id, birthdate, date_joined, plans, wallet, tickets):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.id = id
        self.birthdate = birthdate
        self.birthdate = birthdate
        self.date_joined = date_joined
        self.plans = plans
        self.wallet = wallet
        self.tickets = tickets

    @abstractmethod
    def sign_up(self):
        pass

    @abstractmethod
    def login(self):
        pass


class User(AbstractUser):
    def sign_up(self):
        username = input('create your username: ')
        username_pattern = r'^[a-zA-Z0-9_.]+$'
        if re.match(username_pattern, username):
            unique_username = os.listdir('users_information')
            if not username.lower() in unique_username:
                password = getpass.getpass('create your password: ')
                password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{6,500}$'
                if re.match(password_pattern, password):
                    phone_number = input('enter your phone number or leave it blank: ')
                    if phone_number.isdigit() and len(phone_number) == 11 or phone_number == '':
                        if phone_number == '':
                            phone_number = None
                        id = uuid.uuid4()
                        plans = None
                        wallet = 0
                        tickets = list()
                        try:
                            birthday, birthmonth, birthyear = input('enter your birthday d m yyyy: ').split()
                            birthdate = datetime.datetime(int(birthyear), int(birthmonth), int(birthday)).date()
                            date_joined = datetime.datetime.now().date()
                        except ValueError:
                            return 'incorrect birthdate'
                    else:
                        return 'incorrect phone number'
                else:
                    return 'incorrect or weak password'
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
        self.wallet = wallet
        self.tickets = tickets
        if signed_up:
            users_information = {
                'username': self.username,
                'password': self.password,
                'phone_number': self.phone_number,
                'id': str(self.id),
                'birthdate': str(self.birthdate),
                'date_joined': str(self.date_joined),
                'plans': self.plans,
                'wallet': self.wallet,
                'tickets': self.tickets

            }
            with open(f'users_information/{username.lower()}', 'w+', encoding='utf-8') as information:
                json.dump(users_information, information)
            information.close()
            return 'your account has been created successfully'

    def login(self):
        username = input('enter your username: ').lower()
        password = getpass.getpass('enter your password: ')

        def legged_in():
            logged_in = False
            try:
                with open(f'users_information/{username}', 'r', encoding='utf-8') as login_information:
                    matching_information = json.load(login_information)
                if username == str(matching_information['username']).lower() and password == matching_information[
                        'password']:
                    logged_in = True
                user_information = {
                    'username': matching_information['username'],
                    'password': matching_information['password'],
                    'phone_number': matching_information['phone_number'],
                    'id': matching_information['id'],
                    'birthdate': matching_information['birthdate'],
                    'date_joined': matching_information['date_joined'],
                    'plans': matching_information['plans'],
                    'wallet': matching_information['wallet'],
                    'tickets': matching_information['tickets']
                }
                if logged_in:
                    print('logged in successfully!')
                    while True:
                        options = input('security and privacy 1, get a plan 2, order a ticket 3,'
                                        ' charge your wallet 4 and 0 to log out: ')
                        if options == '1':
                            while True:
                                security_options = input('to check your information press 1, to change your information'
                                                         ' press 2, press 0 to back: ')
                                if security_options == '1':
                                    hash_pass = hashlib.sha256(matching_information['password'].encode('utf-8'))
                                    for i in matching_information['tickets']:
                                        with open(f'movies/{i}', 'r', encoding='utf-8') as check_tickets_date:
                                            movies_date_show = json.load(check_tickets_date)
                                        to_date_type = jdatetime.datetime.strptime(
                                            movies_date_show['show_date'], '%Y-%m-%d')
                                        show_hour_to_date = jdatetime.datetime.strptime(
                                            movies_date_show['show_starts'], '%H:%M:%S').time()
                                        now = jdatetime.datetime.now()
                                        movie_date = jdatetime.datetime(to_date_type.year, to_date_type.month,
                                                                        to_date_type.day, show_hour_to_date.hour)
                                        if movie_date < now.today():
                                            matching_information['tickets'].remove(i)
                                            user_information['tickets'] = matching_information['tickets']
                                            with open(f'users_information/{matching_information['username']}',
                                                      'w', encoding='utf-8') as ticket_date_passed:
                                                json.dump(user_information, ticket_date_passed)
                                    print(
                                        f'username: {matching_information['username']}'
                                        f'\npassword: {hash_pass.hexdigest()}'
                                        f'\nphone number: {matching_information['phone_number']}'
                                        f'\nid: {matching_information['id']}'
                                        f'\nbirthdate: {matching_information['birthdate']}'
                                        f'\ndate joined: {matching_information['date_joined']}'
                                        f'\nplans: {matching_information['plans']}'
                                        f'\nwallet: {matching_information['wallet']:,}'
                                        f'\ntickets: {matching_information['tickets']}'
                                    )
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
                                                if new_username == '0':
                                                    break
                                                username_pattern = r'^[a-zA-Z0-9_.]+$'
                                                unique = os.listdir('users_information')
                                                username_in_list = new_username.lower() in unique
                                                if (re.match(username_pattern, new_username)
                                                        and new_username.lower() != str(
                                                            matching_information['username']).lower()
                                                        and not username_in_list):
                                                    user_information['username'] = new_username
                                                    os.chdir('users_information')
                                                    os.renames(matching_information['username'], new_username.lower())
                                                    os.chdir('..')
                                                    with open(f'users_information/{new_username}', 'w',
                                                              encoding='utf-8') as username_changing:
                                                        json.dump(user_information, username_changing)
                                                    username_changing.close()
                                                    matching_information = user_information
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
                                                if new_phone_number == '0':
                                                    break
                                                if matching_information['phone_number'] is not None:
                                                    if new_phone_number == matching_information['phone_number']:
                                                        print(f'"{new_phone_number}" is current phone number')
                                                if (
                                                        new_phone_number.isdigit() and len(new_phone_number) == 11
                                                        and new_phone_number != matching_information['phone_number']
                                                ):
                                                    user_information['phone_number'] = new_phone_number
                                                    with open(f'users_information/{matching_information['username']}',
                                                              'w',
                                                              encoding='utf-8') as phone_number_changing:
                                                        json.dump(user_information, phone_number_changing)
                                                    phone_number_changing.close()
                                                    matching_information = user_information
                                                    print('your phone number has been changed successfully')
                                                    break
                                                else:
                                                    if new_phone_number != matching_information['phone_number']:
                                                        print(f'"{new_phone_number}" isn\'t a correct phone number')
                                        elif information_changing == '3':
                                            while True:
                                                current_password = getpass.getpass(
                                                    'enter your current password, press 0 '
                                                    'to cancel: ')
                                                if current_password == '0':
                                                    break
                                                if current_password == matching_information['password']:
                                                    password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{6,500}$'
                                                    new_password = getpass.getpass('enter your new password: ')
                                                    if re.match(password_pattern, new_password):
                                                        if new_password != matching_information['password']:
                                                            confirm_password = getpass.getpass(
                                                                'confirm your password: ')
                                                            if confirm_password == new_password:
                                                                user_information['password'] = confirm_password
                                                                with open(f'users_information/'
                                                                          f'{matching_information['username']}', 'w',
                                                                          encoding='utf-8') as password_changing:
                                                                    json.dump(user_information, password_changing)
                                                                password_changing.close()
                                                                matching_information = user_information
                                                                print('your password has changed successfully')
                                                                break
                                                            else:
                                                                print('password does not match')
                                                        else:
                                                            print('it\'s your current password')
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
                                bronze_plan_price = 20_000
                                silver_plan_price = 50_000
                                gold_plan_price = 150_000
                                select_a_plan = input(f'1-bronze price : {bronze_plan_price}\n'
                                                      f'2-silver price : {silver_plan_price}\n'
                                                      f'3-gold price : {gold_plan_price}\n'
                                                      f'choose one of above, to get back press 0: ')

                                def payment():
                                    user_info = {
                                        'username': matching_information['username'],
                                        'password': matching_information['password'],
                                        'phone_number': matching_information['phone_number'],
                                        'id': matching_information['id'],
                                        'birthdate': matching_information['birthdate'],
                                        'date_joined': matching_information['date_joined'],
                                        'plans': matching_information['plans'],
                                        'wallet': matching_information['wallet'],
                                        'tickets': matching_information['tickets']
                                    }
                                    full_name = input('enter your full name: ')
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
                                                        balance = random.randint(0, 1_000_000)
                                                        user_bank = BankAccount(full_name, card_number, cvv2,
                                                                                expire_year, expire_month,
                                                                                card_pin, balance)
                                                        if select_a_plan == '1':
                                                            if (
                                                                    user_bank.withdraw(bronze_plan_price ==
                                                                                       'successful transaction'
                                                                                       and matching_information[
                                                                                           'plans'] != 'Bronze plan')
                                                            ):
                                                                user_info['plans'] = 'Bronze plan'
                                                                with open(f'users_information/{matching_information[
                                                                    'username']}', 'w',
                                                                          encoding='utf-8') as bronze_plan:
                                                                    json.dump(user_info, bronze_plan)
                                                                bronze_plan.close()
                                                                matching_information['plans'] = 'Bronze plan'
                                                                return 'you got the plan successfully'
                                                            else:
                                                                return 'insufficient inventory'
                                                        elif select_a_plan == '2':
                                                            if (
                                                                    user_bank.withdraw(silver_plan_price ==
                                                                                       'successful transaction'
                                                                                       and matching_information[
                                                                                           'plans'] != 'Silver plan')
                                                            ):
                                                                user_info['plans'] = 'Silver plan'
                                                                with open(f'users_information/{matching_information[
                                                                    'username']}', 'w',
                                                                          encoding='utf-8') as silver_plan:
                                                                    json.dump(user_info, silver_plan)
                                                                silver_plan.close()
                                                                matching_information['plans'] = 'Silver plan'
                                                                return 'you got the plan successfully'
                                                            else:
                                                                return 'insufficient inventory'
                                                        elif select_a_plan == '3':
                                                            if (
                                                                    user_bank.withdraw(gold_plan_price ==
                                                                                       'successful transaction'
                                                                                       and matching_information[
                                                                                           'plans'] != 'Gold plan')
                                                            ):
                                                                user_info['plans'] = 'Gold plan'
                                                                with (open(f'users_information/{matching_information[
                                                                    'username']}', 'w', encoding='utf-8') as
                                                                      gold_plan):
                                                                    json.dump(user_info, gold_plan)
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
                                else:
                                    print('invalid choice')
                        elif options == '3':
                            def percentage(number, operator, percent):
                                if operator == '+':
                                    return number + (percent / 100 * number)
                                elif operator == '-':
                                    return number - (percent / 100 * number)

                            user_information = {
                                'username': matching_information['username'],
                                'password': matching_information['password'],
                                'phone_number': matching_information['phone_number'],
                                'id': matching_information['id'],
                                'birthdate': matching_information['birthdate'],
                                'date_joined': matching_information['date_joined'],
                                'plans': matching_information['plans'],
                                'wallet': matching_information['wallet'],
                                'tickets': matching_information['tickets']
                            }
                            shows = os.listdir('movies')
                            while True:
                                print('incoming shows')
                                count = 0
                                for show in shows:
                                    with open(f'movies/{show}', 'r', encoding='utf-8') as show_information:
                                        movie_information = json.load(show_information)
                                    shows_date = movie_information['show_date']
                                    to_date_type = jdatetime.datetime.strptime(shows_date, '%Y-%m-%d')
                                    show_time = movie_information['show_starts']
                                    to_time_type = jdatetime.datetime.strptime(show_time, '%H:%M:%S').time()
                                    date = jdatetime.datetime(to_date_type.year, to_date_type.month, to_date_type.day,
                                                              to_time_type.hour)
                                    now = jdatetime.datetime.now()
                                    if date > now.today():
                                        print(f'Name : "{movie_information['name']}"          '
                                              f'Show date : {movie_information['show_date']}          '
                                              f'Show starts : {movie_information['show_starts']}          '
                                              f'Remaining tickets : {movie_information['remaining_tickets']}')
                                        count += 1
                                        show_information.close()
                                    else:
                                        os.remove(f'movies/{show}')
                                if count < 1:
                                    print('no incoming show for now')
                                    break
                                ordering_ticket = input('enter exact name of movie you wanna watch: ').lower()
                                ticket_price = 50_000
                                movie_list = os.listdir('movies')
                                if ordering_ticket == '0':
                                    break
                                user_birthdate = matching_information['birthdate']
                                is_users_birthday = datetime.datetime.strptime(user_birthdate, '%Y-%m-%d')
                                today = datetime.date.today()
                                if is_users_birthday.month == today.month and is_users_birthday.day == today.day:
                                    ticket_price = percentage(ticket_price, '-', 50)
                                    ticket_price = int(ticket_price)
                                else:
                                    ticket_price = 50_000
                                if ordering_ticket.lower() in movie_list:
                                    if not ordering_ticket in matching_information['tickets']:
                                        if not matching_information['wallet'] - ticket_price < 0:
                                            if movie_information['remaining_tickets'] > 0:
                                                user_information['tickets'] = matching_information['tickets']
                                                user_information['tickets'].append(ordering_ticket)
                                                matching_information['wallet'] -= ticket_price
                                                user_information['wallet'] = matching_information['wallet']
                                                with open(f'users_information/{matching_information['username']}', 'w',
                                                          encoding='utf-8') as order_ticket:
                                                    json.dump(user_information, order_ticket)
                                                order_ticket.close()
                                                with (open(f'movies/{ordering_ticket}', 'r', encoding='utf-8') as
                                                      changing_information):
                                                    information = json.load(changing_information)
                                                changing_information.close()
                                                movies_information = {
                                                    'name': information['name'],
                                                    'show_date': information['show_date'],
                                                    'show_starts': information['show_starts'],
                                                    'remaining_tickets': information['remaining_tickets']
                                                }
                                                movies_information['remaining_tickets'] -= 1
                                                with (open(f'movies/{ordering_ticket}', 'w', encoding='utf-8') as
                                                      ticket_remain):
                                                    json.dump(movies_information, ticket_remain)
                                                ticket_remain.close()
                                                print('you have the ticket')
                                                break
                                            else:
                                                print(f'no ticket for {ordering_ticket}')
                                        else:
                                            print('charge your wallet and try again')
                                            break
                                    else:
                                        print(f'you have {ordering_ticket} ticket already')
                                        break
                                else:
                                    print(f'{ordering_ticket} is not in show list or you or you entered wrong')
                        elif options == '4':
                            while True:
                                try:
                                    amount = int(input('enter amount you wanna charge(IRT) amount must be 50,000 or '
                                                       'higher, press 0 to back: '))
                                    if amount == 0:
                                        break
                                    if amount >= 50_000:
                                        def payment():
                                            full_name = input('enter your full name: ')
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
                                                                balance = random.randint(0, 1_000_000)
                                                                user_bank = BankAccount(full_name, card_number,
                                                                                        cvv2, expire_year,
                                                                                        expire_month, card_pin,
                                                                                        balance)
                                                                if (
                                                                        user_bank.withdraw(amount)
                                                                        == 'successful transaction'
                                                                ):
                                                                    user_information['wallet'] += amount
                                                                    with open(f'users_information/'
                                                                              f'{matching_information['username']}',
                                                                              'w', encoding='utf-8') as wallet_charging:
                                                                        json.dump(user_information, wallet_charging)
                                                                    matching_information['wallet'] = user_information[
                                                                        'wallet']
                                                                    return 'your wallet charged successfully'
                                                                else:
                                                                    return 'insufficient inventory'
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

                                        result = payment()
                                        print(result)
                                        if result == 'your wallet charged successfully':
                                            break
                                    elif amount < 50_000:
                                        print('amount must be higher than 50,000')
                                except ValueError:
                                    print('enter amount correct')
                        elif options == '0':
                            break
                else:
                    print('your password does not match')
            except FileNotFoundError:
                print('there\'s no user with this information')

        return legged_in()


class Admin(AbstractUser):
    def sign_up(self):
        username = input('create your username: ')
        username_pattern = r'^[a-zA-Z0-9_.]+$'
        if re.match(username_pattern, username):
            unique_username = os.listdir('admins_information')
            if not username.lower() in unique_username:
                password = getpass.getpass('create your password: ')
                password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{5,}$'
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
                    return 'incorrect or weak password'
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
            with open(f'admins_information/{username.lower()}', 'w+', encoding='utf-8') as admin_information:
                json.dump(users_information, admin_information)
            admin_information.close()
            return 'Admin account has been created successfully'

    def login(self):
        username = input('enter your username: ').lower()
        password = getpass.getpass('enter your password: ')

        def legged_in():
            logged_in = False
            try:
                with open(f'admins_information/{username}', 'r', encoding='utf-8') as login_information:
                    matching_information = json.load(login_information)
                if username == str(matching_information['username']).lower() and password == matching_information[
                        'password']:
                    logged_in = True
                user_information = {
                    'username': matching_information['username'],
                    'password': matching_information['password'],
                    'phone_number': matching_information['phone_number'],
                    'id': matching_information['id'],
                    'birthdate': matching_information['birthdate'],
                    'date_joined': matching_information['date_joined'],
                    'plans': matching_information['plans']
                }
                if logged_in:
                    print('logged in successfully!')
                    while True:
                        options = input('security and privacy 1, add a movie to show 2,'
                                        ' to check a user press 3 and 0 to log out: ')
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
                                          f'\ndate joined: {matching_information['date_joined']}')
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
                                                if new_username == '0':
                                                    break
                                                username_pattern = r'^[a-zA-Z0-9_.]+$'
                                                unique = os.listdir('admins_information')
                                                username_in_list = new_username.lower() in unique
                                                if (re.match(username_pattern, new_username)
                                                        and new_username.lower() != str(
                                                            matching_information['username']).lower()
                                                        and not username_in_list):
                                                    user_information['username'] = new_username
                                                    os.chdir('admins_information')
                                                    os.renames(matching_information['username'], new_username.lower())
                                                    os.chdir('..')
                                                    with open(f'admins_information/{new_username}', 'w',
                                                              encoding='utf-8') as username_changing:
                                                        json.dump(user_information, username_changing)
                                                    username_changing.close()
                                                    matching_information = user_information
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
                                                if new_phone_number == '0':
                                                    break
                                                if matching_information['phone_number'] is not None:
                                                    if new_phone_number == matching_information['phone_number']:
                                                        print(f'"{new_phone_number}" is current phone number')
                                                if (
                                                        new_phone_number.isdigit() and len(new_phone_number) == 11
                                                        and new_phone_number != matching_information['phone_number']
                                                ):
                                                    user_information['phone_number'] = new_phone_number
                                                    with open(f'admins_information/{matching_information['username']}',
                                                              'w',
                                                              encoding='utf-8') as phone_number_changing:
                                                        json.dump(user_information, phone_number_changing)
                                                    phone_number_changing.close()
                                                    matching_information = user_information
                                                    print('your phone number has been changed successfully')
                                                    break
                                                else:
                                                    if new_phone_number != matching_information['phone_number']:
                                                        print(f'"{new_phone_number}" isn\'t a correct phone number')
                                        elif information_changing == '3':
                                            while True:
                                                current_password = getpass.getpass(
                                                    'enter your current password, press 0 '
                                                    'to cancel: ')
                                                if current_password == '0':
                                                    break
                                                if current_password == matching_information['password']:
                                                    password_pattern = r'^[a-zA-Z0-9!@#$%&*()_+=\'\-.]{5,}$'
                                                    new_password = getpass.getpass('enter your new password: ')
                                                    if re.match(password_pattern, new_password):
                                                        if new_password != matching_information['password']:
                                                            confirm_password = getpass.getpass(
                                                                'confirm your password: ')
                                                            if confirm_password == new_password:
                                                                user_information['password'] = confirm_password
                                                                with open(
                                                                        f'admins_information/{matching_information[
                                                                            'username']}',
                                                                        'w',
                                                                        encoding='utf-8') as password_changing:
                                                                    json.dump(user_information, password_changing)
                                                                password_changing.close()
                                                                matching_information = user_information
                                                                print('your password has changed successfully')
                                                                break
                                                            else:
                                                                print('password does not match')
                                                        else:
                                                            print('it\'s your current password')
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
                                movie_name = input('movie name, 0 to break: ')
                                if movie_name == '0':
                                    break
                                movie_list = os.listdir('movies')
                                if not movie_name.lower() in movie_list:
                                    try:
                                        show_day, show_month, show_year = (
                                            input('enter show date, d m yyyy (jalali): ').split())
                                        show_hour = input('enter show hour (24 hour format): ')
                                        show_year = int(show_year)
                                        show_month = int(show_month)
                                        show_day = int(show_day)
                                        show_hour = int(show_hour)
                                        now = jdatetime.datetime.now()
                                        show_date = jdatetime.datetime(show_year, show_month, show_day, show_hour)
                                        if now.today() < show_date:
                                            movie_information = {'name': movie_name, 'show_date': str(show_date.date()),
                                                                 'show_starts': str(show_date.time()),
                                                                 'remaining_tickets': 200}
                                            with (open(f'movies/{movie_name.lower()}', 'w+', encoding='utf-8') as
                                                  adding_movie):
                                                json.dump(movie_information, adding_movie)
                                            adding_movie.close()
                                            print('movie added to show list')
                                        else:
                                            print('it\' past')
                                    except ValueError:
                                        print('incorrect date')
                                else:
                                    print('it\'s already in show list')
                        elif options == '3':
                            while True:
                                user_username = input('enter user username, press 0 to break it: ')
                                if user_username == '0':
                                    break
                                users = os.listdir('users_information')
                                if user_username in users:
                                    with open(f'users_information/{user_username}', 'r',
                                              encoding='utf-8') as user_checking:
                                        information = json.load(user_checking)
                                    print(
                                        f'username: {information['username']}'
                                        f'\nphone number: {information['phone_number']}'
                                        f'\nbirthdate: {information['birthdate']}'
                                        f'\ndate joined: {information['date_joined']}'
                                        f'\nplans: {information['plans']}'
                                        f'\nwallet: {information['wallet']:,}'
                                        f'\ntickets: {information['tickets']}'
                                    )
                                    break
                                else:
                                    print(f'could not find {user_username}')
                        elif options == '0':
                            break
                else:
                    print('your password does not match')
            except FileNotFoundError:
                print('there\'s no user with this information')

        return legged_in()
