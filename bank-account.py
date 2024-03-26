import psycopg2
import sys
import hashlib


NEW_ACCOUNT = 1
DEPOSIT = 2
WITHDRAW = 3
VIEW_ACCOUNT = 4
QUIT = 5


class Account:
    def __init__(self, first_name, last_name, pin_no, balance=0, id=0):
        self.first_name = first_name
        self.last_name = last_name
        self.pin_no= pin_no
        self.balance = balance
        self.id = id

    def deposit(self, deposit_amount):
        self.balance = self.balance + deposit_amount

    def withdraw(self, withdraw_amount):
        if self.balance > withdraw_amount:
            self.balance = self.balance - withdraw_amount
        else:
            raise Exception("Not enough funds")


def display_home_screen():
    print("1. Create new bank account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. View account")
    print("5. Quit")


def get_account_owner_info():
    first_name = input("Please enter first name: ")
    last_name = input("Please enter last name: ")
    pin_no = input("Please enter four digit pin number: ")
    account = Account(first_name, last_name, pin_no)
    return account


def hash_pin_no(pin_no):
    pin_no_bytes = pin_no.encode('utf-8')
    hash_object = hashlib.sha256(pin_no_bytes)
    return hash_object.hexdigest()


def add_account_to_database(account):
    conn = psycopg2.connect(host="127.0.0.1", dbname="bank", user="postgres", password="hello", port=5432)
    
    cur = conn.cursor()
    cur.execute("""
                          INSERT INTO account (first_name, last_name, pin_no)
                          VALUES (%s, %s, %s) RETURNING id;
                          """,
                          (account.first_name, account.last_name, account.pin_no))
    
    account_id = cur.fetchone()
    print(f"Account created. Your account number is {account_id[0]}")
    
    conn.commit()

    cur.close()
    conn.close()


def get_account_no():
    account_no = input("Please enter account number: ")
    return account_no


def account_exists(account_no):
    conn = psycopg2.connect(host="127.0.0.1", dbname="bank", user="postgres", password="hello", port=5432)

    cur = conn.cursor()
    
    cur.execute("SELECT * FROM account WHERE id=%s;", (account_no, ))
    account_record= cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if account_record == None:
        return False
    else:
        return True
    

def create_account_object(account_no):
    conn = psycopg2.connect(host="127.0.0.1", dbname="bank", user="postgres", password="hello", port=5432)

    cur = conn.cursor()
    
    cur.execute("SELECT * FROM account WHERE id=%s;", (account_no, ))
    account_record = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    account = Account(account_record[1], account_record[2], account_record[3], account_record[4], account_record[0])
    return account


def validate_pin_no(account):
    pin_no = input("Please provide pin number: ")
    if hash_pin_no(pin_no) == account.pin_no:
        return True
    else:
        return False
    

def get_transaction_amount():
    transaction_amount = int(input("Please enter transaction amount: "))
    return transaction_amount


def update_account_balance(account, transaction_amount, transaction_type):
    if transaction_type == DEPOSIT:
        account.deposit(transaction_amount)
    else:
        account.withdraw(transaction_amount)

    conn = psycopg2.connect(host="127.0.0.1", dbname="bank", user="postgres", password="hello", port=5432)

    cur = conn.cursor()

    cur.execute("""
                UPDATE account 
                SET balance = %s
                WHERE id = %s;
                """, (account.balance, account.id))
    conn.commit()

    cur.close()
    conn.close()


def get_verified_account():
    account_no = get_account_no()
    if account_exists(account_no):
        account = create_account_object(account_no)
        if validate_pin_no(account):
            return account
        else:
            raise Exception("Invalid pin number")
    else:
        raise Exception("Account not found")


def execute_transaction(transaction_type):
    account = get_verified_account()
    transaction_amount = get_transaction_amount()
    update_account_balance(account, transaction_amount, transaction_type)


def view_account():
    account = get_verified_account()
    print(f"Hello, {account.first_name}! Your account balance is {account.balance}")

        
def main():
    while True:
        display_home_screen()
        home_screen_input = int(input("Please select option from above: "))
        
        if home_screen_input == NEW_ACCOUNT:
            account = get_account_owner_info()
            account.pin_no = hash_pin_no(account.pin_no)
            add_account_to_database(account)

        if home_screen_input == DEPOSIT:
            execute_transaction(DEPOSIT)
        
        if home_screen_input == WITHDRAW:
            execute_transaction(WITHDRAW)

        if home_screen_input == VIEW_ACCOUNT:
            view_account()
        
        if home_screen_input == QUIT:
            sys.exit()


if __name__ == "__main__":
    main()