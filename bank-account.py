import csv
import time
import psycopg2

class Account:
    account_no_counter = 0

    def __init__(self, first_name, last_name, pin_no, balance=0):
        self.first_name = first_name
        self.last_name = last_name
        self.pin_no= pin_no
        self.balance = balance
        Account.account_no_counter +=1 
        self.account_no = Account.account_no_counter

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

def get_account_owner_info():
    first_name = input("Please enter first name: ")
    last_name = input("Please enter last name: ")
    pin_no = input("Please enter four digit pin number: ")
    account = Account(first_name, last_name, pin_no)
    return account

def add_account_to_database(account):
    conn = psycopg2.connect(host="127.0.0.1", dbname="bank", user="postgres", password="hello", port=5432)
    
    conn.cursor().execute("""
                          INSERT INTO account (first_name, last_name, pin_no)
                          VALUES (%s, %s, %s);
                          """,
                          (account.first_name, account.last_name, account.pin_no))
    
    conn.commit()
    conn.cursor().close()
    conn.close()

def get_account_no():
    account_no = input("Please enter account number: ")
    return account_no

def account_exists(account_no):
    conn = psycopg2.connect(host="127.0.0.1", dbname="bank", user="postgres", password="hello", port=5432)

    cur = conn.cursor()
    
    cur.execute("SELECT * FROM account WHERE id=%s;", (account_no))
    account_record= cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    print(account_record)


def get_deposit_amount():
    deposit_amount = input("Please enter deposit amount: ")
    return deposit_amount

def deposit_money():
    account_no = input("Please enter account number: ")
    with open("bank_accounts.csv", "r") as accounts_file:
        csvreader = csv.reader(accounts_file)
        for account_entry in csvreader:
            if account_entry[0] == account_no:
                account = Account(account_entry[1], account_entry[2], account_entry[3], int(account_entry[4]))
                print("Account found")
                break

    with open("bank_accounts.csv", "w") as accounts_file:
        csvwriter = csv.writer(accounts_file)
        deposit_amount = int(input("Please enter deposit amount: "))
        account.deposit(deposit_amount)
        print(f"Money deposited. New balance is {account.balance}")


def withdraw_money():
    account_no = input("Please enter account number: ")


        
def main():
    display_home_screen()
    home_screen_input = int(input("Please select option from above: "))
    if home_screen_input == 1:
        account = get_account_owner_info()
        add_account_to_database(account)

    if home_screen_input == 2:
        account_no = get_account_no()
        account_exists(account_no)


if __name__ == "__main__":
    main()
"""
account_1 = Account("Stephen", "Lindstrom", 1234)
account_2 = Account("John", "Doe", 1111)
account_1.deposit(100)
account_1.withdraw(50)
print(account_1.account_no)
print(account_2.account_no)
"""