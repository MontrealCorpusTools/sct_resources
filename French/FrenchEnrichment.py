"""
All info from LEXIQUE (http://lexique.org/)


output format:
word, frequency, word type, neighborhood density

Prepositions, conjunctions, auxiliary verbs, and pronouns are function words
all others are content words
"""
words = {}



def parseFile(path,writepath):
	with open(path,'r') as f1:
		lines = f1.readlines()

	with open(writepath,'w') as f2:	
		f2.write('word,frequency,word type\n')
		for line in lines:
			splitline = line.split('\t')
			word = splitline[0]
			freq = splitline[6]
			cgram = splitline[3]
			neighbors = splitline[19]
			word_class = 'Content'
			if cgram[:3] in ['PRE','CON','PRO','AUX']:
				word_class = 'Function'
			

			f2.write('{},{},{},{}\n'.format(word,freq,word_class,neighbors))




parseFile('Lexique381.txt',"FrenchEnrichmentData.csv")