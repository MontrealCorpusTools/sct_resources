import csv
import re


"""
stress information from Wiktionary (word list gotten from https://petscan.wmflabs.org/)

All info from Subtlex-PL (http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-pl)

output format: word, frequency, word type, stress pattern
conjuctions, prepositions, and pronouns are Function words
all others are content
"""
words = {}
def parsefile(path,dest):
	words = {}
	with open(path) as f1:
		lines1 = f1.readlines()
	f2 = open(dest, 'w') 
	f2CW = csv.writer(f2)

	with open('stresses.txt') as f2:
		lines2 = f2.readlines()

	for line in lines2:
		split = line.split(",")
		try:
			words[split[0].strip()] = split[1].strip()
		except IndexError:
			print(line)
	#res = Pool(4).apply(get_words, args=[0,math.floor(10949/40),0])#,[math.ceil(10949/4),math.floor(2*10949/4),1],[math.ceil(2*10949/4),math.floor(3*10949/4),2],[math.ceil(3*10949/4),0,3])
	#get_words(0,math.floor(10949/40),0)
	f2CW.writerow(['word','freq','word type','stress pattern'])
	for line in lines1:
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

				stresspattern = ''
			f2CW.writerow([word,freq,word_type, stresspattern])




parsefile('subtlex-pl.csv', 'PolishEnrichmentData.csv')

