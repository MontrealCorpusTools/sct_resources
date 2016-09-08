import re
import csv
"""
Frequency info from https://github.com/hermitdave/FrequencyWords/
WordType from ranks.nl (http://www.ranks.nl/stopwords/thai-stopwords)
Tone from GlobalPhone Thai

Output format: word, tone pattern, frequency
"""

words = {}
def getTone(path):
	numgex = re.compile('.*[0-9](.+?[0-9])?.*')
	with open(path, errors='ignore') as f1:
		lines = f1.readlines()

		for line in lines:
			splitline = re.split("} {{", line.strip())
			word = splitline[0][1:]

			raw = splitline[1]

			rawsplit = re.split('{|}',raw)	
			selection = rawsplit[1]

			res = numgex.search(selection)
			if res:
				allNums = res.group()
				nums = re.split('[^0-9]',allNums)
				number = ""
				for x in nums:
					if x is not "":
						number += str(x)

			else:
				number = ""
			try: 
				words[word][0] = number
			except KeyError:
				words[word] = [number, '', '']



def getFrequency(path):
	with open(path,errors='ignore') as f:
		lines = f.readlines()
	for line in lines:
		splitline = re.split('\s', line)
		
		word = splitline[0]
		freq = (int(splitline[1])/1114765)*1000000

		try:
			words[word][1] = freq
		except KeyError:
			words[word] = ['',freq,'']


def getWordType(path):

	with open(path,errors='ignore') as f1:
		lines = f1.readlines()
	for line in lines:
		line = line.strip()
	for word in words.keys():
		if word in lines:
			words[word][2] = 'Function'
		else:
			words[word][2] = 'Content'


				
getTone('Thai-GPDict.12k.tones')
getFrequency('th_full.txt')
getWordType('stopwords.txt')

f2 = open('ThaiEnrichmentData.csv', 'w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','tone pattern','frequency'])

count=0
for k,v in words.items():
	#if v[0]!='' and v[1]!='':
	f2CW.writerow([k,v[0],v[1], v[2]])
