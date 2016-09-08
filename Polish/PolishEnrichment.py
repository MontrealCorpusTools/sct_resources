import csv

"""
list is incomplete, needs stress
possibly more fleshed out as well, potentially look to wiktionary

All info from Subtlex-PL (http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-pl)

output format: word, frequency, word type
conjuctions, prepositions, and pronouns are Function words
all others are content
"""

def parsefile(path,dest):
	with open(path) as f1:
		lines = f1.readlines()
	f2 = open(dest, 'w') 
	f2CW = csv.writer(f2)
	f2CW.writerow(['word','freq','word type'])
	for line in lines:
			splitline = line.split("\t")	
			word = splitline[0]
			freq = splitline[6]
			pos = splitline[8]
			word_type = 'Content'
			if pos in ['conj', 'qub', 'prep', 'pron']:
				word_type='Function'

			f2CW.writerow([word,freq,word_type])


parsefile('subtlex-pl.csv','PolishEnrichmentData.csv')