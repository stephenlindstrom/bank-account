class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, deposit_amount):
        self.balance = self.balance + deposit_amount

    def withdraw(self, withdraw_amount):
        if self.balance > withdraw_amount:
            self.balance = self.balance - withdraw_amount
        else:
            raise Exception("Not enough funds")

account_1 = Account()
account_1.deposit(100)
account_1.withdraw(150)
print(account_1.balance)