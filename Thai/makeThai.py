import re
"""
get the number of words in the frequency list for later division
"""

regex = re.compile('[a-z]+')
total = 0
numlines = 0
with open('th_full.txt',errors='ignore') as f:
	lines = f.readlines()
	for line in lines:
		splitline = re.split('\s', line)
		
		numlines+=1
		total+= int(splitline[1])
		

print(total, numlines)

#1114765