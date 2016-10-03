

#replaces ae, oe, ue with umlauts
def replaceUmlaut(string): 
	string = string.replace("ae", "ä")
	if "euer" not in string:
		string = string.replace("ue", "ü")
	string = string.replace("oe", "ö")
	return string
#replace ss with ß
def replaceSharp(string):
	oldString = string
	string = string.replace("ss", "ß")
	if oldString is string:
		return ""
	return string


words = {}

def getStress(path):
	with open(path , "r") as f1:
		lines = f1.readlines()
	
		for line in lines:
			split = line.split("\\")
			stressed = split[4] #this is the part w ' and -
			ortho = replaceUmlaut(split[1])
			Sortho = replaceSharp(ortho)
			syls = stressed.split("-") #split into syllables
			numString = ""
			numSyls = len(syls)
			index= 0
			for i in range(len(syls)):
				if "'" in syls[i]:
					numString = numString + "1"
					index = i+1
				else:
					numString = numString + "0"
			words[ortho] = (numString, "", "")

			if Sortho is not "":
				words[Sortho] = (numString, "", "")
		
def getWordType(path):
	with open(path, "r") as f1:
		lines = f1.readlines()
		for line in lines:
			split = line.split("\\")
			
			if split[3] in {"3", "5", "6", "8"}:
				split[1] = replaceUmlaut(split[1])
				sharp = replaceSharp(split[1])
				try:
					words[split[1]][2] = "Function"
				except KeyError:
					words[split[1]].update("","","Function")
				
				if sharp is not "":
					try:
						words[sharp][2] = "Function"
					except KeyError:
						words[sharp].update("","","Function")
			else:
				try:
					words[split[1]][2] = "Content"
				except KeyError:
					words[split[1]].update("","","Content")
				
				if sharp is not "":
					try:
						words[sharp][2] = "Content"
					except KeyError:
						words[sharp].update("","","Content")


getStress("/Users/elias/Desktop/SCT enrichment and tests/German/gpw.cd")
getWordType("/Users/elias/Desktop/SCT enrichment and tests/German/gsl.cd")

print(words)