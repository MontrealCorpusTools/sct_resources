import random
import webbrowser
def openpage():
	with open('RussianEnrichmentData.csv') as f1:
		lines = f1.readlines()

	chrome_path = 'open -a /Applications/Google\ Chrome.app %s'


	l = lines[random.randint(0,len(lines))]

	word = l.split(',')[0]
	print(l)
	url ='https://en.wiktionary.org/wiki/{}'.format(word)
	webbrowser.get(chrome_path).open(url)



for x in range(5):
	openpage()