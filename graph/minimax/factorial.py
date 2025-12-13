print("hello me")

n = 5


def cal_factorial(n, depth):
    if n <= 1:
        return 1
    
    result = n * cal_factorial(n-1, depth+1)

    return result

result = cal_factorial(n,0)

print(f"factorial is: {result}")