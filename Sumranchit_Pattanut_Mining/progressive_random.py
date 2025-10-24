import random

class Progressive:
    def __init__(self):
        # fusion of fixed limit and progressive random

        self.start_success_rate = 0
        self.success_rate = self.start_success_rate
        self.success_rate_increment = 0

        self.attempts = 0
        self.fixed_limit = 0

    def set_random_rate(self, suc_rate, suc_incre, limit):
        self.start_success_rate = suc_rate
        self.success_rate = self.start_success_rate
        self.success_rate_increment = suc_incre

        self.fixed_limit = limit

    def draw(self):
        num = random.uniform(0, 100)

        if num <= self.success_rate or self.attempts >= self.fixed_limit:
            print("success")
            self.success_rate = self.start_success_rate
            self.attempts = 0

            return True
        else:
            self.success_rate += self.success_rate_increment
            self.attempts += 1
            print("fail. success rate is " + str(self.success_rate) + ". attempt number is " + str(self.attempts))

            return False


