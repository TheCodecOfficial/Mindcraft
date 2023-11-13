import heapq

h = []
heapq.heappush(h, (5, 'write code'))
heapq.heappush(h, (7, 'release product'))
heapq.heappush(h, (1, 'write spec'))

# check if 'write spec' is in heap
print(any(task == 'write spec' for _, task in h))