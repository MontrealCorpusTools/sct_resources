import csv


"""
list is incomplete, needs stress
possibly more fleshed out as well, potentially look to wiktionary

Frequency info from: Russian National Corpus (http://www.ruscorpora.ru/en/)

output format:
word, frequency, word type

Prepositions, conjunctions, and pronouns are function words
all others are content words
"""


def parseFile(path,writepath):

	with open(path, errors='ignore') as f1:
		lines = f1.readlines()

	f2 = open(writepath,'w') 
	f2cw = csv.writer(f2)
	f2cw.writerow(['word','frequency','word_type'])
	for line in lines:
		splitline = line.split("\t")
		string=splitline[0]
		pos = splitline[1]
		freq = splitline[2]

		word_type = 'Content'
		if pos in ['pr','conj','spro']:
			word_type='Function'
		f2cw.writerow([string,freq,word_type])




parseFile('freqrnc2011.csv','RussianEnrichmentData.csv')