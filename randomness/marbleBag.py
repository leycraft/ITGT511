import random

class MarbelBag:
    def __init__(self):
        self.items = ['dirt', 'monster', 'gold']
        self.bag = []
    
    def refill(self):
        # based on items above

        if(len(self.bag) == 0):
            print("bag refilled")
            for i in range(7):
                self.bag.append((self.items[0]))

            for i in range(2):
                self.bag.append((self.items[1]))

            self.bag.append((self.items[2]))
        else:
            print("still has item")

    def refill_specify(self, items, prob):
        # manually add items

        if(len(self.bag) == 0):
            print("bag refilled")
            
            for i in range(len(items)):
                for j in range(prob[i]):
                    self.bag.append((items[i]))
                pass

        else:
            print("still has item")

    def draw(self, draw_num):
        for i in range(draw_num):
            draw_item = random.choice(self.bag)
            self.bag.remove(draw_item)
            print(draw_item, end = ' ')
        print("")

def main():
    bag = MarbelBag()

    items = ['dirt', 'monster', 'gold', 'human']
    probability = [7, 2, 1, 3]


    bag.refill_specify(items, probability)
    bag.draw(13)
    bag.refill()
    bag.draw(5)
    bag.refill()

if __name__ == "__main__":
    main()