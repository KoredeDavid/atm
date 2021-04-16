import calendar
import datetime

import random
import re


# {username : [ {password:password}, {balance:balance}, {account_number:account_number}]}
# This is the database
user_db = {
    "zuri": [
        {'password': 'password'},
        {'balance': 20000},
        {'account_number': 4567920139}
    ],

    'korede': [
        {'password': 'iloveyou'},
        {'balance': 100000},
        {'account_number': 1868123764}
    ],

    'xylum': [
        {'password': 'zurimentor'},
        {'balance': 50000},
        {'account_number': 4809876120}
    ],
}

# {account_number: username} This items in this dic is same as the one above. I only created so that i can easily get
# a user's username with his o her account_number
account_number_user_db = {4567920139: 'zuri', 1868123764: 'korede', 4809876120: 'xylum'}

# Year, Day, Hour, Minute and Month
now = datetime.datetime.now()
year = now.year
day = now.day
week_day = now.strftime("%A")
month = calendar.month_name[now.month]
hour = now.hour
minute = now.minute


def input_credentials():
    username = input('Username: ').lower()
    password = input('Password: ')
    return username, password


def register():
    invalid = True
    while invalid:

        print("\nRegister New Account. Username should contain at least 5 characters and only letters, numbers and "
              "underscore\n ")

        username, password = input_credentials()
        if len(username) >= 5 and len(password) >= 5:
            if username not in user_db:

                # This regular expression checks if the "username" does not input special characters
                if not bool(re.search('[^\w]', username)):

                    account_number_exists = True
                    # This loop is just to ensure that the account number generated does not exist
                    while account_number_exists:
                        # Generates Account Number
                        account_number = random.randint(1000000000, 9999999999)
                        if account_number not in account_number_user_db:
                            account_number_exists = False

                    # Registers the user to the user_db
                    user_db[username] = [
                        {'password': password},
                        {'balance': 0},
                        {'account_number': account_number}
                    ]

                    # Registers to account_number_user_db
                    account_number_user_db[account_number] = username

                    invalid = False
                    print(f'Welcome {username.capitalize()} you have been registered')
                    return username, password
                else:
                    print("\nYour username contains invalid characters")
            else:
                print("\nThis username has been taken")
        else:
            print("\nYou username and password must contain at least 5 characters")


def login():
    global get_user_pass

    authenticated = False
    while not authenticated:
        user, user_pass = input_credentials()
        try:
            get_user_pass = user_db.get(user, None)[0]['password']
        except TypeError:
            pass

        # this authenticates the user with (user, user_pass)
        if user in user_db and user_pass == get_user_pass:
            authenticated = True
            return user
        else:
            print('\nYour login details are incorrect, oya try again')


def check_balance(user):
    get_user_from_db = user_db.get(user)
    balance_index = get_user_from_db[1]
    balance = balance_index['balance']
    print(f'{user.capitalize()}, your account balance is ${balance}\n')

    perform_another_transaction_or_terminate(user)


def withdraw(user):
    insufficient_funds = False
    amount_invalid = False

    while not amount_invalid or not insufficient_funds:

        # This catches an error that is raised if the user inputs a str instead of an int
        # It also loops if the user has an insufficient funds
        try:
            amount = int(input(f'\nHow much would you like to withdraw {user.capitalize()}? '))
        except ValueError:
            amount = None
            print(f'\nPlease input a correct figure. Try Again')
        else:
            amount_invalid = True

            # this checks if the amount inputted is > or < the user's account balance.
            get_user_from_db = user_db.get(user)
            balance_index = get_user_from_db[1]
            balance = balance_index.get('balance')

            if amount <= balance:
                insufficient_funds = True
                balance_index['balance'] -= amount
                balance = balance_index['balance']
                print(f"Take your cash {user.capitalize()}. Your balance is now ${balance}\n")

                perform_another_transaction_or_terminate(user)
            else:
                print(f'\nInsufficient  funds, your current account balance is ${balance}. Try Again #kpk')


def deposit(user):
    invalid_amount = False
    while not invalid_amount:
        # This catches an error that is raised if the user inputs a str instead of an int
        try:
            amount = int(input(f'\nHow much would you like to deposit, {user.capitalize()}? '))
        except ValueError:
            amount = None

        # this checks if the selected operation is available
        if amount:
            invalid_amount = True

            get_user_from_db = user_db.get(user)
            balance_index = get_user_from_db[1]
            balance_index['balance'] += amount
            balance = balance_index['balance']

            print(f"Successful, {user.capitalize()}. Your balance is now ${balance} #opp\n")
            perform_another_transaction_or_terminate(user)
        else:
            print(f'\nPlease enter a valid amount, {user.capitalize()}. Try Again.')


# This ensures that the figure inputted is valid
def clean_amount(action):
    invalid_amount = False
    while not invalid_amount:
        # This catches an error that is raised if the user inputs a str instead of an int or a float
        try:
            amount = int(input(f'\nHow much will you like to {action}? '))
        except ValueError:
            amount = None
        if amount:
            return amount
        else:
            print(f'\nPlease enter a valid amount. Try Again.')


# This checks if the budget has sufficient funds to perform a withdrawal or a transfer.
def funds_validation(action, user, balance):
    insufficient_funds = False
    while not insufficient_funds:
        amount = clean_amount(action)
        # this checks if the amount inputted is > or < the user's account balance.
        if amount <= balance:
            insufficient_funds = True
            balance -= amount
            print(
                f'\nTake your cash Zuri. Your balance for {user} is now ${balance}' if action == 'withdraw' else '')
            return balance, amount
        else:
            print(f'\nInsufficient  funds, your current account balance is ${balance}. Try Again #kpk')


def transfer(user):
    global recipient_account
    get_user_from_db = user_db.get(user)
    user_balance_index = get_user_from_db[1]
    user_balance = user_balance_index.get('balance')
    user_account_number_index = get_user_from_db[2]
    user_account_number = user_account_number_index.get('account_number')
    user_balance, amount_to_transfer = funds_validation('transfer', user, user_balance)

    invalid_account = False
    while not invalid_account:
        # This catches an error that is raised if the user inputs a str instead of an int or a float
        try:
            recipient_account = int(input(f'Please type the recipient\'s account number? '))

            if recipient_account == user_account_number:
                raise ValueError(print(f'\nYou can\'t transfer to yourself {user}'))

            # This block of code gets the recipient username and balance using the inputted account number
            recipient_username = account_number_user_db[recipient_account]
            print(f'\nThe recipient username is {recipient_username.capitalize()}\n')
            get_recipient_from_db = user_db.get(recipient_username)
            recipient_balance_index = get_recipient_from_db[1]
            recipient_balance_index['balance'] += amount_to_transfer
            user_balance_index['balance'] = user_balance
            print(f'Transfer of ${amount_to_transfer} to {recipient_username.capitalize()}, successful. Your  account '
                  f'balance is now ${user_balance}')

            perform_another_transaction_or_terminate(user)
            invalid_account = True
        except (ValueError, KeyError):
            print(f'\nPlease enter a valid account number. Try Again.\n')


def make_a_complaint(user):
    input(f"What issue will you like to report, {user.capitalize()}? ")
    print(f"Thank you for contacting us, we will get back to you soon {user.capitalize()}\n")

    perform_another_transaction_or_terminate(user)


def terminate(user):
    exit(f"Bye {user}. We hope to see you soon")


def perform_another_transaction_or_terminate(user):
    operations = [1, 2]

    operations_text = "1. Perform another transaction \n2. Terminate transaction\n"
    print(operations_text)

    operation_available = False
    while not operation_available:
        # This catches an error that is raised if the user inputs a str instead of an int
        try:
            operation = int(input(f'What will you like to do {user.capitalize()}? '))
        except ValueError:
            operation = None

        # this checks if the selected operation is available
        if operation in operations:
            operation_available = True
            if operation == 1:
                transaction()
            if operation == 2:
                terminate(user)
        else:
            print(f'\nPlease select either of 1-2. Try Again \n{operations_text}')


def transaction():
    login_or_register = [1, 2]
    print("Welcome to Zuri Bank\n")
    login_or_register_text = "1. Login \n2. Register\n"
    print(login_or_register_text)

    available = False
    while not available:
        # This catches an error that is raised if the user inputs a str instead of an int
        try:
            value = int(input(f'What will you like to do? '))
        except ValueError:
            value = None

        # this checks if the selected operation is available

        if value in login_or_register:
            available = True

            if value == 1:
                # logged_in returns the logged in user
                logged_in = login()

            if value == 2:
                username, password = register()
                logged_in = username

            if logged_in:
                print(f'Welcome {logged_in.capitalize()}. {week_day} {day} {month}, {year}. {hour}:{minute}hrs ('
                      f'WAT)\nAccount Number: {user_db[logged_in][2]["account_number"]}')

                operations_text = "\n1. Withdraw \n2. Check Balance \n3. Deposit \n4. Make a complaint \n5. Transfer " \
                                  "\n6. Terminate Transaction "

                print(operations_text)

                operation_available = False
                while not operation_available:
                    # This catches an error that is raised if the user inputs a str instead of an int
                    try:
                        operation = int(input(f'\nWhat will you like to do {logged_in.capitalize()}? '))
                    except ValueError:
                        operation = None

                    # this checks if the selected operation is available and calls the appropriate function
                    # assigned to it
                    operations = [1, 2, 3, 4, 5, 6]
                    if operation in operations:
                        operation_available = True
                        if operation == 1:
                            withdraw(logged_in)
                        if operation == 2:
                            check_balance(logged_in)
                        if operation == 3:
                            deposit(logged_in)
                        if operation == 4:
                            make_a_complaint(logged_in)
                        if operation == 5:
                            transfer(logged_in)
                        if operation == 6:
                            terminate(logged_in)
                    else:
                        print(f'\nPlease select either of 1-6. Try Again {operations_text}')
        else:
            print(f'\nPlease select either of 1-2. Try Again \n{login_or_register_text}')


transaction()
