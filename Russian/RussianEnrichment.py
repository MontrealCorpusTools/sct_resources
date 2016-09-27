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

words = {}
def parseFile(path,writepath):

	with open(path, errors='ignore') as f1:
		lines = f1.readlines()

	with open('stresses10.txt') as f3:
		lines3 = f3.readlines()

	# for line in lines3:
	# 	split = line.split(",")
	# 	words[split[0].strip()] = split[1].strip()	



	f2 = open(writepath,'w') 
	f2cw = csv.writer(f2)
	f2cw.writerow(['word','frequency','word_type', 'stress'])

	for l in lines3:
		splitline = l.split(",")
		words[splitline[0].strip()] = [None,None,splitline[1].replace('"',"").strip()]


	for line in lines:
		splitline = line.split("\t")
		string=splitline[0]
		pos = splitline[1]
		freq = splitline[2]

		word_type = 'Content'
		if pos in ['pr','conj','spro']:
			word_type='Function'

		try:
			words[string][0] = freq
			words[string][1] = word_type
		except KeyError:
			words[string] = [freq, word_type,None]


	for k,v in words.items():

		f2cw.writerow([k,v[0],v[1],v[2]])


parseFile('freqrnc2011.csv','RussianEnrichmentData.csv')