import re
import csv
"""
All info from LEXESP
"""

word_count = 5020930


word_dict = {}



def getFrequency(path):
	with open(path, 'r', errors= 'ignore') as f1:
		lines = f1.readlines()

		for line in lines:
			splitline = line.split("\t")

			freq = (int(splitline[1])/word_count)*1000000
			try:
				word_dict[splitline[0]][0] = freq
			except KeyError:
				word_dict[splitline[0]] = [freq, "",""]

def getStress(path):
	with open(path, 'r',errors= 'ignore') as f1:
		lines = f1.readlines()

		for line in lines:
			splitline = line.split("\t")

			try:
				word_dict[splitline[0]][1] = splitline[1].strip()
			except KeyError:
				word_dict[splitline[0]] = ["", splitline[1].strip(),""]

def getWordType(path):
	with open(path, 'r',errors= 'ignore') as f1:
		lines = f1.readlines()

		for line in lines:
			splitline = line.split("\t")
			word_type = 'Content'

			if splitline[1][1:3].upper() in ['TD','TI','DD','DP','DT','DE','DI','VA','PP','PD','PX','PI','PT','PR','CC','CS']:
				word_type = 'Function'

			try:
				word_dict[splitline[0]][2] = word_type
			except KeyError:
				word_dict[splitline[0]] = ["", "",word_type]




getStress('acento.TXT')
getFrequency('frec.TXT')
getWordType('categ.TXT')

f2 = open('SpanishEnrichmentData.csv','w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','frequency','stress','word type'])
for k,v in word_dict.items():

	f2CW.writerow([k,v[0],v[1],v[2]])
