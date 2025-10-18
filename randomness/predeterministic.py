import random

predetermin = random.randint(0, 10)
count = 0

for i in range(10):
    if(count >= predetermin):
        count = 0
        predetermin = random.randint(0, 10)
        print("attacked. next is in " + str(predetermin))
    else:
        print("...")
        count += 1