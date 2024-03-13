import csv

class Account:
    account_no_counter = 0

    def __init__(self, first_name, last_name, pin_no):
        self.first_name = first_name
        self.last_name = last_name
        self.pin_no= pin_no
        self.balance = 0
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

def create_account():
    first_name = input("Please enter first name: ")
    last_name = input("Please enter last name: ")
    pin_no = input("Please enter four digit pin number: ")
    account = Account(first_name, last_name, pin_no)
    
    with open("bank_accounts.csv", 'w') as accounts_file:
        csvwriter = csv.writer(accounts_file)
        csvwriter.writerow([account.account_no, account.first_name, account.last_name, account.pin_no, account.balance])


def deposit_money():
    account_no = input("Please enter account number: ")

        
def main():
    display_home_screen()
    home_screen_input = int(input("Please select option from above: "))
    if home_screen_input == 1:
        create_account()

    if home_screen_input == 2:
        deposit_money()

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