class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, deposit_amount):
        self.balance = self.balance + deposit_amount