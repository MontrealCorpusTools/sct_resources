import re
import csv
import urllib.request

"""
writes word, frequency and word type to csv file
words and frequencies from Czech National Corpus (Český národní korpus: Srovnávací frekvenční seznamy. Ústav Českého národního korpusu FF UK, Praha 2010. Dostupné z WWW: http://ucnk.ff.cuni.cz/srovnani10.php)
word type information gotten from wiktionary (https://en.wiktionary.org/wiki/Category:Czech_lemmas)

pronouns, prepositions, and conjunctions are function words, all others are content

"""

def getHTML(page):
    """ get raw html from page"""
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html

def get_function_words():
	functionwords = []
	conjhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Czech_conjunctions'))
	prephtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Czech_prepositions'))
	pronhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Czech_pronouns'))

	regex = re.compile('<li><a href="\/wiki\/.*?" title=".*?">.*?<\/a><\/li>')

	conjmatches = regex.findall(conjhtml)
	prepmatches = regex.findall(prephtml)
	pronmatches = regex.findall(pronhtml)

	wordregex = re.compile("\">.+?<")

	for match in (conjmatches+pronmatches+prepmatches):
		rmatch = wordregex.search(match).group(0)
		functionwords.append(rmatch[2:-1])


	for word in functionwords:
		if 'Czech' in word or 'lemmas' in word or 'by' in word or word == 'Prepositions by language':
			functionwords.remove(word)


	return(set(functionwords))

def gettotal():
	total = 0
	with open('syn2010_word', encoding='utf-8', errors='ignore') as f1:
		lines =f1.readlines()
	for line in lines:
		splitline = re.split('\s', line)
		total+=int(splitline[2])
	#print(total)

def parsefile(path, writer):
	fwords = get_function_words()

	with open(path, encoding='utf-8', errors='ignore') as f1:
		lines =f1.readlines()
	for line in lines:
		splitline = re.split('\s', line)
		word = splitline[1].strip()
		freq = int(splitline[2].strip())/97082209*100000
		if word in fwords:
			wordtype = 'function'
		else:
			wordtype = 'content'

		writer.writerow([word,freq,wordtype])




f1 = open('CzechEnrichmentData.csv', 'w')
f1CW = csv.writer(f1)

parsefile('syn2010_word', f1CW)



