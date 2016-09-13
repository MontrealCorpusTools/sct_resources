import csv
import re
import urllib.request, urllib.parse

"""
stress information from Wiktionary

All info from Subtlex-PL (http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-pl)

output format: word, frequency, word type, stress pattern
conjuctions, prepositions, and pronouns are Function words
all others are content
"""
words = {}
def parsefile(path,dest):
	with open(path) as f1:
		lines = f1.readlines()
	f2 = open(dest, 'w') 
	f2CW = csv.writer(f2)
	get_words()
	f2CW.writerow(['word','freq','word type','stress pattern'])
	for line in lines:
			splitline = line.split("\t")	
			word = splitline[0]
			freq = splitline[6]
			pos = splitline[8]
			word_type = 'Content'
			if pos in ['conj', 'qub', 'prep', 'pron']:
				word_type='Function'

			try: 
				stresspattern = words[word]
			except KeyError:
				print(word)
				stresspattern = ''
			f2CW.writerow([word,freq,word_type, stresspattern])


def getHTML(page):
    """ get raw html from page"""
    page = urllib.parse.urlsplit(page)
    page = list(page)
    page[2] = urllib.parse.quote(page[2])
    page = urllib.parse.urlunsplit(page)
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html


def get_words():
	iparegex = re.compile("<li><a href=\"/wiki/Wiktionary:International_Phonetic_Alphabet\".*?Polish.*?</li>")
	splitregex = re.compile("lang=.*?>")
	vowelregex = re.compile('[aɛɛ̃iɨɔɔ̃u]')
	with open('words.txt') as f2:
		lines = f2.readlines()
	for i,line in enumerate(lines):
		html = getHTML('https://en.wiktionary.org/wiki/{}#Polish'.format(line.strip().replace(' ','_')))
		

		all_ipa = iparegex.findall(str(html))
		for string in all_ipa:
			split = splitregex.split(string)
			ipa = split[1][1:split[1].index('<')-1]

			splitipa = vowelregex.split(ipa)
			stresspattern = ""
			for l in splitipa:
				if 'ˌ' in l:
					stresspattern+='2'
				if 'ˈ' in l:
					stresspattern+='1'
				else:
					stresspattern+='0'
			
			words[line] = stresspattern
			if i%10 == 0:
				print("{} percent done".format((i/10949)*100))

parsefile('subtlex-pl.csv', 'PolishEnrichmentData.csv')

