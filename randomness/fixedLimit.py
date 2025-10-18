import random

success_rate = 20
attempts = 0
fixed_limit = 5

for i in range(10):
    num = random.uniform(0, 100)
    
    if num <= success_rate or attempts >= fixed_limit:
        print("success")
        attempts = 0
    else:
        print("fail")
        attempts += 1