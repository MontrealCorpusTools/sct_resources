import re
import csv
import urllib.request

"""
Frequency info from : http://www.corpora.heliohost.org/statistics.html

word type information gotten from wiktionary (https://en.wiktionary.org/wiki/Category:Swahili_lemmas)

pronouns, prepositions, and conjunctions are function words, all others are content
"""

words = {}
def getHTML(page):
    """ get raw html from page"""
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html

def get_function_words():
	functionwords = []
	conjhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Swahili_conjunctions'))
	prephtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Swahili_prepositions'))
	pronhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Swahili_pronouns'))

	regex = re.compile('<li><a href="\/wiki\/.*?" title=".*?">.*?<\/a><\/li>')

	conjmatches = regex.findall(conjhtml)
	prepmatches = regex.findall(prephtml)
	pronmatches = regex.findall(pronhtml)

	wordregex = re.compile("\">.+?<")

	for match in (conjmatches+pronmatches+prepmatches):
		rmatch = wordregex.search(match).group(0)
		functionwords.append(rmatch[2:-1])


	for word in functionwords:
		if 'Swahili' in word or 'lemmas' in word or 'by' in word or word == 'Prepositions by language':
			functionwords.remove(word)


	return(set(functionwords))

def getFrequency(path):
	with open(path,encoding ='utf-8',errors='ignore') as f:
		lines = f.readlines()
	for line in lines:
		splitline = re.split('\s', line)
		
		word = splitline[0]
		freq = (int(splitline[1])/13414371)*1000000

		words[word] = freq
	

fwords= get_function_words()
getFrequency('sw.txt')
f2 = open('SwahiliEnrichmentData.csv', 'w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','word type','frequency'])


for k,v in words.items():
	if k in fwords:
		wordtype = 'function'
	else:
		wordtype = 'content'
	f2CW.writerow([k,wordtype, v])
