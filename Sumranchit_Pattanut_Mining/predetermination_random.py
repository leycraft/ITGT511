import random

class Predeterministic:
    def __init__(self):
        self.predetermined_num = 0
        self.lower_limit = 0
        self.upperlimit  = 0
        self.count = 0

    def set_random_rate(self, l_limit, u_limit):
        self.lower_limit = l_limit
        self.upperlimit  = u_limit

        self.randomize_rate()
        
    def randomize_rate(self):
        self.predetermined_num = random.randint(self.lower_limit, self.upperlimit)

    def draw(self):
        if(self.count >= self.predetermined_num):
            self.count = 0
            self.randomize_rate()
            
            print("mined. next is in " + str(self.predetermined_num))
            return True
        else:
            print("...")
            self.count += 1
            return False