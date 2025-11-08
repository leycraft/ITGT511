import heapq

numbers = [1, 5, 9, 7, 0]

heapq.heapify(numbers) # create heap tree
heapq.heappush(numbers, 3) # add 3 to heap tree
n = heapq.heappop(numbers) # pop smallest number

print(n)
print(numbers)
n = heapq.heappop(numbers) # pop smallest number

print(n)
print(numbers)