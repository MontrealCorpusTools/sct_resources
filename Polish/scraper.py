import re
import math
import urllib.request, urllib.parse
from multiprocessing import Process, Pool, Queue
import time
def start_processes():
	


	with open('words.txt') as f2:
		lines = f2.readlines()
	

#	q1 = Process(target = get_words, args = (lines[0:math.floor(10949/4)], 0))
	

#	q2 = Process(target = get_words, args = (lines[math.ceil(10949/4):math.floor(2*10949/4)], 1)) 
	

#	q3 = Process(target = get_words, args = (lines[math.ceil(2*10949/4):math.floor(3*10949/4)], 2))
	

	q4 = Process(target = get_words, args = (lines[math.ceil(3*10949/4):], 3))
	


#	q1.start()
#	q2.start()
#	q3.start()
	q4.start()

#	q1.join()
#	q2.join()
#	q3.join()
	q4.join()

def getHTML(page):
    """ get raw html from page"""
    page = urllib.parse.urlsplit(page)
    page = list(page)
    page[2] = urllib.parse.quote(page[2])
    page = urllib.parse.urlunsplit(page)
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html


def get_words(lines, writenum=0):
	iparegex = re.compile("<li><a href=\"/wiki/Wiktionary:International_Phonetic_Alphabet\".*?Polish.*?</li>")
	splitregex = re.compile("lang=.*?>")
	vowelregex = re.compile('[aɛɛ̃iɨɔɔ̃u]')
	
	f3 = open("stresses{}.txt".format(writenum), 'w')

	for i in range(len(lines)):
		line = lines[i]

		html = getHTML('https://en.wiktionary.org/wiki/{}#Polish'.format(line.strip().replace(' ','_')))
		

		all_ipa = iparegex.findall(str(html))
		for string in all_ipa:
			split = splitregex.split(string)
			ipa = split[1][1:split[1].index('<')-1]
			just_vs = re.sub('[^ˌˈaɛɛ̃iɨɔɔ̃u]',"",ipa)
			#get just vowels and stress marks
			stresspattern = ""
			if line == "komórkową":
				print(just_vs)
			viter = iter(just_vs)
			for seg in viter:
				#for each vowel or stressmark
				if seg == 'ˈ':
					stresspattern+='1'
					try:
						next(viter)
					except StopIteration:
						pass
				elif seg == 'ˌ':
					stresspattern+='2'
					try:
						next(viter)
					except StopIteration:
						pass
				else:
					stresspattern+='0'
			line = line.strip()

			#print("{},{}".format(line,stresspattern))
			#words[line] = stresspattern
			f3.write("{},{}\n".format(line,stresspattern))
			if i%10 == 0:
				print("{} percent done".format((i/len(lines))*100))
			time.sleep(.01)
	f3.close()



if __name__ == "__main__":
	start_processes()
