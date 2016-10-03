import re
import csv
import urllib.request

"""

word type information gotten from wiktionary (https://en.wiktionary.org/wiki/Category:Hausa_lemmas)

pronouns, prepositions, and conjunctions are function words, all others are content
"""

words = {}
def getHTML(page):
    """ get raw html from page"""
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html

def get_function_words():
	f1 = open('HausaEnrichmentData.csv','w')
	f1cw = csv.writer(f1)
	f1cw.writerow(['word', 'word type'])
	functionwords = []
	conjhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Hausa_conjunctions'))
	prephtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Hausa_prepositions'))
	pronhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Hausa_pronouns'))

	regex = re.compile('<li><a href="\/wiki\/.*?" title=".*?">.*?<\/a><\/li>')

	conjmatches = regex.findall(conjhtml)
	prepmatches = regex.findall(prephtml)
	pronmatches = regex.findall(pronhtml)

	wordregex = re.compile("\">.+?<")

	for match in (conjmatches+pronmatches+prepmatches):
		rmatch = wordregex.search(match).group(0)
		functionwords.append(rmatch[2:-1])

	functionwords= set(functionwords)
	functionwords = list(functionwords)

	for word in functionwords:
		if 'Hausa' in word or word == 'Prepositions by language':
			functionwords.remove(word)
		else:
			f1cw.writerow([word, 'function'])


get_function_words()