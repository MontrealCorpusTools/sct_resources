import re
import csv

import urllib.request
"""
Frequency info from https://github.com/hermitdave/FrequencyWords/

word type information gotten from wiktionary (https://en.wiktionary.org/wiki/Category:Thai_lemmas)
Tone from GlobalPhone Thai

Output format: word, tone pattern, frequency
"""

def getHTML(page):
    """ get raw html from page"""
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html


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

def get_function_words():
	functionwords = []
	conjhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Thai_conjunctions'))
	prephtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Thai_prepositions'))
	pronhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Thai_pronouns'))

	regex = re.compile('<li><a href="\/wiki\/.*?" title=".*?">.*?<\/a><\/li>')

	conjmatches = regex.findall(conjhtml)
	prepmatches = regex.findall(prephtml)
	pronmatches = regex.findall(pronhtml)

	wordregex = re.compile("\">.+?<")

	for match in (conjmatches+pronmatches+prepmatches):
		rmatch = wordregex.search(match).group(0)
		functionwords.append(rmatch[2:-1])

	
	for word in functionwords:
		if 'Thai' in word or 'lemmas' in word or word == 'Prepositions by language':
			functionwords.remove(word)
		
	functionwords = set(functionwords)

	for word in words.keys():
		if word in functionwords:
			words[word][2] = 'Function'
		else:
			words[word][2] = 'Content'
	

"""
def getWordType(path):

	with open(path,errors='ignore') as f1:
		lines = f1.readlines()
	for line in lines:
		line = line.strip()
	for word in words.keys():
		if word in lines:
			
		else:
			words[word][2] = 'Content'
"""

				
getTone('Thai-GPDict.12k.tones')
getFrequency('th_full.txt')
#getWordType('stopwords.txt')
get_function_words()

f2 = open('ThaiEnrichmentData.csv', 'w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','tone pattern','frequency'])

count=0
for k,v in words.items():
	#if v[0]!='' and v[1]!='':
	f2CW.writerow([k,v[0],v[1], v[2]])
