import calendar
import datetime

# {username : [ {password:password}, {balance:balance}]}
# This is the database
user_db = {
    "zuri": [
        {'password': 'password'},
        {'balance': 20000}
    ],

    'korede': [
        {'password': 'iloveyou'},
        {'balance': 100000}
    ],

    'xylum': [
        {'password': 'zurimentor'},
        {'balance': 50000}
    ],
}

# Year, Day, Hour, Minute and Month
now = datetime.datetime.now()
year = now.year
day = now.day
week_day = now.strftime("%A")
month = calendar.month_name[now.month]
hour = now.hour
minute = now.minute


def input_login_credentials():
    username = input('Username: ').lower()
    password = input('Password: ')
    return username + ' ' + password


def register():
    pass


def login():
    print("Welcome to Zuri Bank")
    global get_user_pass

    authenticated = False
    while not authenticated:
        user, user_pass = input_login_credentials().split(' ')
        try:
            get_user_pass = user_db.get(user, None)[0]['password']
        except TypeError:
            pass

        # this authenticates the user with (user, user_pass)
        if user in user_db and user_pass == get_user_pass:
            authenticated = True
            print(f'Welcome {user.capitalize()}. {week_day} {day} {month}, {year}. {hour}:{minute}hrs (WAT) ')
            return user
        else:
            print('\nYour login details are incorrect, oya try again')


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


def make_a_complaint(user):
    input(f"What issue will you like to report, {user.capitalize()}? ")
    print(f"Thank you for contacting us, we will get back to you soon {user.capitalize()}\n")

    perform_another_transaction_or_terminate(user)


def terminate(user):
    print(f"Bye {user}. We hope to see you soon")
    exit()


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
    # logged_in returns the logged in user
    logged_in = login()
    if logged_in:
        operations = [1, 2, 3, 4]

        operations_text = "\n1. Withdraw \n2. Deposit \n3. Make a complaint \n4. Terminate Transaction"
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
            if operation in operations:
                operation_available = True
                if operation == 1:
                    withdraw(logged_in)
                if operation == 2:
                    deposit(logged_in)
                if operation == 3:
                    make_a_complaint(logged_in)
                if operation == 4:
                    terminate(logged_in)
                if operation == 5:
                    register()
            else:
                print(f'\nPlease select either of 1-4. Try Again {operations_text}')


transaction()
