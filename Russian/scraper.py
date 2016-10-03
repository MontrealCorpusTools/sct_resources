import re
import math
import urllib.request, urllib.parse
from multiprocessing import Process, Pool, Queue
import time
def start_processes():
	
	lines = []

	with open('words.csv') as f2:
		originallines = f2.readlines()
	for line in originallines:
		word = line.split(',')[1].replace("\"","")
		lines.append(word)
	"""	
	q1 = Process(target = get_words, args = (lines[0:math.floor(320955/4)], 0))
	

	q2 = Process(target = get_words, args = (lines[math.ceil(320955/4):math.floor(2*320955/4)], 1)) 
	

	q3 = Process(target = get_words, args = (lines[math.ceil(2*320955/4):math.floor(3*320955/4)], 2))
	

	q4 = Process(target = get_words, args = (lines[math.ceil(3*320955/4):], 3))
	


	q1.start()
	q2.start()
	q3.start()
	q4.start()

	q1.join()
	q2.join()
	q3.join()
	q4.join()
	"""
	get_words(lines, 10)
def getHTML(page):
    """ get raw html from page"""
    page = urllib.parse.urlsplit(page)
    page = list(page)
    page[2] = urllib.parse.quote(page[2])
    page = urllib.parse.urlunsplit(page)
    html = None
    try:
    	with urllib.request.urlopen(page) as response:
        	html = response.read().decode('utf-8')
    except:
    	pass
    return html


def get_words(lines, writenum=0):#(start=0,end=0, writenum = 0, queue = None):
	#print("start is ",start)
	#words = queue.get()
	#print("starting from {} going to {}".format(start,end))
	iparegex = re.compile("<li><a href=\"/wiki/Wiktionary:International_Phonetic_Alphabet\".*?Russian.*?</li>")
	splitregex = re.compile("lang=.*?>")
	vowelregex = re.compile('[aæɑeɛiɨoɵuʉɐəɪɨʉʊ̃u]')
	
	f3 = open("stresses{}.txt".format(writenum), 'w')
	#i = start
	for i in range(len(lines)):
		line = lines[i]

		html = getHTML('https://en.wiktionary.org/wiki/{}#Russian'.format(line.strip().replace(' ','_')))
		if html == None:
			continue
		all_ipa = iparegex.findall(str(html))
		for string in all_ipa:
			split = splitregex.split(string)
			ipa = split[1][1:split[1].index('<')-1]
			just_vs = re.sub('[^ˌˈaæɑeɛiɨoɵuʉɐəɪɨʉʊ̃u]',"",ipa)
			#get just vowels and stress marks
			stresspattern = ""

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
