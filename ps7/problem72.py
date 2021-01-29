'''
between is the text for HG Fargo solution
(a) Pear, profit 35
(b) 2 Pear, profit 60
(c) 10 Dale, profit 270
(d) capacity
(e) items
(f) size
(g) value
(h) 3 5
(i) count * total
(j) count * total
(k) count
(l) count
(m) count + total
（n） 5
(o) 2 # this is not the correct solution to stock prob.
(p) 5 # note it is asking the solution to knapsack
'''

import numpy as np

def recursive(total, count, price, profit, visited):
	if total < min(price) or visited.count(0) == 0:
		return total
		
	max_price = 0
	for i in range(count):
		if visited[i]:
			continue
			
		max_price = max(max_price, recursive(total - price[i], count, price, profit, visited) + profit[i])
		visited[i] += 1
		max_price = max(max_price, recursive(total, count, price, profit, visited))
		visited[i] -= 1
		
	return max_price
	
def dp(total, count, price, profits):
	# use reshape instead of [[A]*m]*n or it will not be hard copy
	profit = np.array([0]*(count + 1)*(total + 1)).reshape(total + 1, count + 1)
	visited = np.array([0]*(count + 1)*(total + 1)).reshape(total + 1, count + 1)
	for i in range(total + 1):
		# if there is no count of stocks available
		profit[i][0] = i
		for j in range(1, count + 1):
			# if you choose not to buy this stock
			# else if you buy this stock
			if i >= price[j - 1]:
				profit[i][j] = max(profit[i][j - 1], profits[j - 1] + profit[i - price[j - 1]][j])
				visited[i][j] = True
			else:
				profit[i][j] = profit[i][j - 1]

	return profit[total][count]			

def find_fargo(total, count, start, profit):
	visited = [0] * count
	
	# recursive
	#max_profit = recursive(total, count, start, profit, visited)
	# dp
	max_profit = dp(total, count, start, profit)
	return max_profit
	
if __name__ == "__main__":
	# unlimited amount knapsack problem
	# (a)
	profit = find_fargo(20, 4, [12,10,18,15], [39,13,47,45])
	print(profit)
	# (b)
	profit = find_fargo(30, 4, [12,10,18,15], [39,13,47,45])
	print(profit)
	# (c)
	profit = find_fargo(120, 4, [12,10,18,15], [39,13,47,45])
	print(profit)