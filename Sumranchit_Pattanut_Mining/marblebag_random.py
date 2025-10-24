import random

class MarbelBag:
    def __init__(self):
        self.bag = []
        self.refill_items = []
        self.refill_prob = []

    def refill_specify(self, items, prob):
        # manually add items

        self.refill_items = items
        self.refill_prob = prob

        if(len(self.bag) == 0):
            print("refilled")
            
            for i in range(len(items)):
                for j in range(prob[i]):
                    self.bag.append((items[i]))
                pass

        else:
            print("still has item")

    def auto_refill(self):
        if(len(self.bag) == 0):
            print("refilled")
            
            for i in range(len(self.refill_items)):
                for j in range(self.refill_prob[i]):
                    self.bag.append((self.refill_items[i]))
                pass

        else:
            print("still has item")

    def draw(self, draw_num):
        if draw_num <= len(self.bag):
            for i in range(draw_num):
                draw_item = random.choice(self.bag)
                self.bag.remove(draw_item)
                print(draw_item, end = ' ')

            if len(self.bag) == 0:
                self.auto_refill()

            return draw_item
        else:
            print("not enough item")
            self.auto_refill()