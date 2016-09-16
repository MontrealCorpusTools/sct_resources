import re
import math
import urllib.request, urllib.parse
from multiprocessing import Process, Pool, Queue
testlist = ['komórkową','kolanowy']


s = 'ɔ̃'
top = s.replace("ɔ","")
#print(top)
#for seg in s:
#	print(seg)


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
		line = lines[i]

		html = getHTML('https://en.wiktionary.org/wiki/{}#Polish'.format(line.strip().replace(' ','_')))
		

		all_ipa = iparegex.findall(str(html))
		for string in all_ipa:
			split = splitregex.split(string)
			ipa = split[1][1:split[1].index('<')-1].replace(s, "ɔ")
			just_vs = re.sub('[^ˌˈaɛɛ̃iɨɔɔ̃u]',"",ipa)
			#get just vowels and stress marks
			stresspattern = ""
			viter = iter(just_vs)
			for seg in viter:
				print(seg)
				#for each vowel or stressmark
				if seg == 'ˈ':
					stresspattern+='1'
					next(viter, None)
				elif seg == 'ˌ':
					stresspattern+='2'
					next(viter, None)
				else:
					stresspattern+='0'
			line = line.strip()
			print(stresspattern)
			#print("{},{}".format(line,stresspattern))
			#words[line] = stresspattern
			#f3.write("{},{}\n".format(line,stresspattern))
			#if i%10 == 0:
			#	print("{} percent done".format((i/len(lines))*100))
	f3.close()


get_words(testlist,0)