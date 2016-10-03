import csv
import re
"""
Frequency info from Subtlex-PR (http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-pt-br)
Stress/wordtype/neighborhood density info from PSC (http://www.guilherme.ca/psc.html)

output format: word,frequency,word type, stress pattern, neighborhood density
"""

words = {}
def getFreq(path):
	with open(path,errors='ignore') as f1:
		lines = f1.readlines()
	total = 0
	for line in lines:
		splitline = re.split('\s', line)

		total += int(splitline[1])
	for i,line in enumerate(lines,1):
		splitline = re.split('\s', line)
		word = splitline[0]
		freq = (int(splitline[1])/total)*1000000

		try:
			words[word][0]=freq
		except KeyError:
			words[word] = [freq,'','','']

def getWordType(path):
	with open(path,errors='ignore') as f1:
		lines = f1.readlines()
	for line in lines:
		splitline = re.split(',', line)
		pos = splitline[33].replace('\"',"")
		word = splitline[0].replace('\"',"")
		word_type = "Content"
		if pos in ['pro','prep' ]:
			word_type = 'Function'
		try:
			words[word][1] = word_type
		except KeyError:
			words[word] = ['',word_type,'','']
		

def getStress(path):
	with open(path,errors='ignore') as f1:
		lines = f1.readlines()
	for line in lines:
		splitline = re.split(',', line)
		fullsyls = splitline[1]
		brokensyls = fullsyls.split('-')
		pattern = ""
		for syl in brokensyls:
			if '\'' in syl:
				pattern+='1'
			else:
				pattern+='0'
		word = splitline[0].replace('\"', "")
		try:
			words[word][2] = pattern
		except KeyError:
			words[word] = ['','',pattern, '']

def getND(path):
	with open(path,errors='ignore') as f1:
		lines = f1.readlines()
	for line in lines:
		splitline = re.split(',', line)
		word = splitline[0].replace('\"',"")
		nD = splitline[52].replace('\"',"")
		try:
			words[word][3] = nD
		except KeyError:
			words[word] = ['','', '',nD]
	

getFreq('portlex.csv')
getWordType('psc.csv')
getStress('psc.csv')
getND('psc.csv')

f2 = open('PortugueseEnrichmentData.csv', 'w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','frequency','word type', 'stress pattern', 'neighborhood density'])
for k,v in words.items():
	f2CW.writerow([k, v[0],v[1],v[2],v[3]])