import re
import csv
import urllib.request

"""

word type information gotten from wiktionary (https://en.wiktionary.org/wiki/Category:Korean_lemmas)

pronouns and particles are function words, all others are content
"""

words = {}
def getHTML(page):
    """ get raw html from page"""
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html

def get_function_words():
	functionwords = []
	parthtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Korean_particles'))
	pronhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Korean_pronouns'))

	regex = re.compile('<li><a href="\/wiki\/.*?" title=".*?">.*?<\/a><\/li>')

	partmatches = regex.findall(parthtml)
	pronmatches = regex.findall(pronhtml)

	wordregex = re.compile("\">.+?<")

	for match in (pronmatches+partmatches):
		rmatch = wordregex.search(match).group(0)
		functionwords.append(rmatch[2:-1])


	for word in functionwords:
		if 'Korean' in word or 'lemmas' in word or 'by' in word:
			functionwords.remove(word)


	return(set(functionwords))

def getFrequency(path):
	with open(path,encoding ='utf-8',errors='ignore') as f:
		lines = f.readlines()
	for line in lines:
		splitline = re.split('\s', line)
		
		word = splitline[0]
		freq = (int(splitline[1])/2072158)*1000000
		words[word] = freq

fwords= get_function_words()
getFrequency('ko_full.txt')
f2 = open('KoreanEnrichmentData.csv', 'w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','word type','frequency'])


for k,v in words.items():
	if k in fwords:
		wordtype = 'function'
	else:
		wordtype = 'content'
	f2CW.writerow([k,wordtype, v])
