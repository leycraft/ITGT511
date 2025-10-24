import random

class FixedLimit:
    def __init__(self):
        self.success_rate = 0
        self.attempts = 0
        self.fixed_limit = 0

    def set_random_rate(self, suc_rate, limit):
        self.success_rate = suc_rate
        self.fixed_limit = limit

    def draw(self):
        num = random.uniform(0, 100)
    
        if num <= self.success_rate or self.attempts >= self.fixed_limit:
            print("success")
            self.attempts = 0
        else:
            print("fail")
            self.attempts += 1

