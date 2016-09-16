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
		lines = f1.readlines()
	f2 = open(dest, 'w') 
	f2CW = csv.writer(f2)
	
	q = Queue()
	q.put(words)

	with open('words.txt') as f2:
		lines = f2.readlines()
	"""

	q1 = Process(target = get_words, args = (lines[0:math.floor(10949/4)], 0))#(0, 20, 0, q)) #(0,math.floor(10949/4),0))
	

	q2 = Process(target = get_words, args = (lines[math.ceil(10949/4):math.floor(2*10949/4)], 1)) #(21, 40, 1, q))#(math.ceil(10949/4),math.floor(2*10949/4),1))
	

	q3 = Process(target = get_words, args = (lines[math.ceil(2*10949/4):math.floor(3*10949/4)], 2))#(41, 60, 2, q))#(math.ceil(2*10949/4),math.floor(3*10949/4),2))
	

	q4 = Process(target = get_words, args = (lines[math.ceil(3*10949/4):], 3))#(61, 80, 3, q)) # (math.ceil(3*10949/4),0,3))
	


	q1.start()
	q2.start()
	q3.start()
	q4.start()

	q1.join()
	q2.join()
	q3.join()
	q4.join()
	"""

	#res = Pool(4).apply(get_words, args=[0,math.floor(10949/40),0])#,[math.ceil(10949/4),math.floor(2*10949/4),1],[math.ceil(2*10949/4),math.floor(3*10949/4),2],[math.ceil(3*10949/4),0,3])
	#get_words(0,math.floor(10949/40),0)
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


def get_words(lines, writenum=0):#(start=0,end=0, writenum = 0, queue = None):
	#print("start is ",start)
	#words = queue.get()
	#print("starting from {} going to {}".format(start,end))
	iparegex = re.compile("<li><a href=\"/wiki/Wiktionary:International_Phonetic_Alphabet\".*?Polish.*?</li>")
	splitregex = re.compile("lang=.*?>")
	vowelregex = re.compile('[aɛɛ̃iɨɔɔ̃u]')
	
	f3 = open("stresses{}.txt".format(writenum), 'w')
	#i = start
	for i in range(len(lines)):
		print(lines[i])
		line = lines[i]
		#if i == start:
		#	print("starting line is ",line)
		#if i>end:
		#	break
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
			line = line.strip()
		#	print("{},{}".format(line,stresspattern))
			words[line] = stresspattern
			f3.write("{},{}\n".format(line,stresspattern))
			if i%10 == 0:
				print("{} percent done".format((i/len(lines))*100))
	f3.close()
	return words

parsefile('subtlex-pl.csv', 'PolishEnrichmentData.csv')

