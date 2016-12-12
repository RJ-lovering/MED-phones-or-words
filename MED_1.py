##!/usr/bin/python
##

import string
from nltk.corpus import cmudict

# slightly prettier printing than basic print of a matrix.
def printMatrix(distance):
	for row in distance:
		print row

# calculates adjusted cost for substitution based on closeness 
# across four dimensions of pronunciation/letter identity
def substCost(character1, character2, input_type):

	phones = {"AO":[0,0,4,4],"AA":[0,0,0,6],"IY":[0,0,0,0],\
	"UW":[0,0,4,0],"EH":[0,0,0,4],"IH":[0,0,1,1],"UH":[0,0,3,1],"AH":[0,0,2,3],\
	"AX":[0,0,2,3],"AE":[0,0,0,5],"EY":[1,0,0,4],"AY":[1,0,2,3],"OW":[1,0,4,4],\
	"AW":[1,0,2,0],"OY":[1,0,4,0],"ER":[2,0,0,5],"AXR":[2,0,2,3],"EH R":[2,0,0,4],\
	"UH R":[2,0,3,1],"AO R":[2,0,4,4],"AA R":[2,0,0,6],"IH R":[2,0,1,1],\
	"IY R":[2,0,0,0],"AW R":[2,0,2,0], "Y":[3,0,0,0], "W":[3,0,4,0], \
	"Q":[3,0,4,6],"L":[4,0,1,5], "EL":[4,0,2,3], "R":[4,0,2,5],"DX":[4,0,1,2],\
	"NX":[4,0,1,5],"M":[5,0,0,0],"EM":[5,0,0,0],"N":[5,0,1,1],"EN":[5,0,1,1],\
	"NG":[5,0,4,0],"ENG":[5,0,4,0],"F":[6,1,1,0],"V":[6,0,1,0],"TH":[6,1,0,0],\
	"DH":[6,0,0,0],"S":[6,1,1,1],"Z":[6,0,1,1],"SH":[6,1,2,2],"ZH":[6,0,2,2],\
	"HH":[6,1,5,6], "CH":[7,1,2,2],"JH":[7,0,2,2],"P":[8,1,0,0],"B":[8,0,0,0],\
	"T":[8,1,1,0],"D":[8,0,1,0],"K":[8,1,4,0],"G":[8,0,4,0]}

	letters = {"a":[0,0,1],"e":[0,0,1],"i":[0,0,1],"o":[0,0,1],\
	"u":[0,0,1],"b":[1,0,1],"c":[1,1,1],"d":[1,0,1],"f":[1,1,1],\
	"g":[1,0,1],"h":[1,1,1],"j":[1,0,1],"k":[1,1,1],"l":[1,0,1],\
	"m":[1,0,0],"n":[1,0,0],"p":[1,1,1],"q":[1,1,1],"r":[1,0,1],\
	"s":[1,1,1],"t":[1,1,1],"v":[1,0,1],"w":[1,0,1],"x":[1,1,1],\
	"z":[1,0,1]}

	if input_type=="word":

		if character1 == character2:
			cost = 0
		else:
			cost = .5

	else:

		quals_p1 = phones[character1]
		quals_p2 = phones[character2]

		if character1 == character2:
			cost = 0
		else:
			diff = [quals_p1[i]-quals_p2[i]for i in range(len(quals_p1))]
			cost = float(abs(sum(diff))*0.75)

	return cost

# this function is from Figure 3.25 in the NLTK book (page 76)
def minEditDist(target, source, input_type):

	len_target = len(target)
	len_source = len(source)

	distance = [[0 for i in range(len_source+1)] for j in range(len_target+1)]

	for i in range (1,len_target+1):
		distance[i][0] = distance[i-1][0] + 1

	for j in range(1, len_source+1):
		distance[0][j] = distance[0][j-1] + 1

	for i in range (1,len_target+1):
		for j in range(1, len_source+1):
			distance[i][j] = min(distance[i-1][j]+1,distance[i][j-1]+1, distance[i-1][j-1]+substCost(source[j-1],target[i-1], input_type))

	#printMatrix(distance)

	return distance[len_target][len_source]

# get all phones for all words starting with a given letter in CMUdict
def findCandidates(letter):

 	candidates = {}

	CMU_dict = cmudict.dict()
	CMU_keys = CMU_dict.keys()
	for key in CMU_keys:
		if key[0]==letter:
			candidates[key]=CMU_dict[key]

	return candidates

# removes stress markings from CMUdict results
def getSounds(sounds):

	sounds2 = []
	for sound in sounds:
		if sound[-1] in ['0','1','2','3','4','5','6','7','8','9']:
			sound = sound[:-1]
			sounds2.append(sound)
		else:
			sounds2.append(sound)
			
	return sounds2


test_pairs_sounds = [("MONETARY","COMMENTARY"),("MONETARY","MONOTONE")]
test_pairs_words = [("drive","divers"),("drive","brief")]

# for pair in test_pairs_sounds:

# 	target, source = cmudict.dict()[pair[0].lower()][0], cmudict.dict()[pair[1].lower()][0]
# 	target, source = getSounds(target), getSounds(source)
# 	print "The minimum edit distance between %s and %s is %i."%(pair[0], pair[1], minEditDist(target, source, "sound"))

for pair in test_pairs_words:
	target, source = pair[0],pair[1]
	print "The minimum edit distance between %s and %s is %i."%(target, source, minEditDist(target, source, "word"))


# format input for MED fn.
metric = "KRYPTON"	
word = string.lower(metric)
sounds = cmudict.dict()[word][0]
metric_sounds = getSounds(sounds)

# get all c-words in CMUdict for comparison
c_words_dict = findCandidates("c")
c_keys = c_words_dict.keys()

# high initialization for comparison, immediately supplanted by first result.
distance = 100
closest = ""
count = 0
candidates = []

# go through all candidates, compare to requested input
# for key in c_keys:

# 	candidate = getSounds(c_words_dict[key][0])

# 	distance = minEditDist(metric_sounds,candidate,"sounds")

# 	candidates.append((distance, key))

# sort results, pick top one
candidates.sort()

closest = candidates[0][1]
distance = candidates[0][0]

if candidates[0][0] == candidates[1][0]:
	print "There was a tie for closest word to %s between %s and %s, with a minimum edit distance of %.2f."%(metric,candidates[1][1],closest,distance)
else:
	print "The closest sounding word to 'KRYPTON' is '%s,' with a minimum edit distance of %.2f."%(closest,distance)


