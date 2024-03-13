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

account_1 = Account("Stephen", "Lindstrom", 1234)
account_2 = Account("John", "Doe", 1111)
account_1.deposit(100)
account_1.withdraw(50)
print(account_1.account_no)
print(account_2.account_no)