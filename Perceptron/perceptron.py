from __future__ import division
from nltk.stem import PorterStemmer
import sys
import os
from math import log, exp

stop = True
if sys.argv[1] == "yes":
	stop = False
stemmer = PorterStemmer()

#get all spam and ham file names
spamPath = "train/spam/"
spamFiles = os.listdir(spamPath)
hamPath = "train/ham/"
hamFiles = os.listdir(hamPath)

#import all stop words
stopFile = open("stop.txt", "r")
stopWords = []
for l in stopFile:
	stopWords = l.split()
sn = len(spamFiles)
hn = len(hamFiles)
pSpam = sn/(sn+hn)
pHam = hn/(sn+hn)

#populate spamWords with all words from spam files, hamWords with all words from ham files, and words with all unique words from ham and spam files
words = []
spamWords = [[] for i in range(sn)]
hamWords = [[] for i in range(hn)]
i = 0
for fileName in spamFiles:
	infile = open(spamPath+fileName, "r")
	for line in infile:
		nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
		lineWords = nLine.split()
		lineWords = [stemmer.stem(w.lower()) for w in lineWords]
		if stop:
			spamWords[i].extend(lineWords)
			words.extend(w for w in lineWords if w not in words)
		else:
			spamWords[i].extend(w for w in lineWords if w not in stopWords)
			words.extend(w for w in lineWords if w not in words and w not in stopWords)
	infile.close()
	i += 1
i = 0
for fileName in hamFiles:
	infile = open(hamPath+fileName, "r")
	for line in infile:
		nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
		lineWords = nLine.split()
		lineWords = [stemmer.stem(w.lower()) for w in lineWords]
		if stop:
			hamWords[i].extend(lineWords)
			words.extend(w for w in lineWords if w not in words)
		else:
			hamWords[i].extend(w for w in lineWords if w not in stopWords)
			words.extend(w for w in lineWords if w not in words and w not in stopWords)
	infile.close()
	i += 1
spamNums = [[0 for j in range(len(words))] for i in range(sn)]
hamNums = [[0 for j in range(len(words))] for i in range(hn)]
for j in range(sn):
	for i in range(len(words)):
		spamNums[j][i] = spamWords[j].count(words[i])
for j in range(hn):
	for i in range(len(words)):
		hamNums[j][i] = hamWords[j].count(words[i])

#Calculate the weight for each word.  Repeated 20 times for convergence with lambda = .05
weights = [0.0 for i in range(len(words)+1)]
for i in range(20):
	for j in range(sn):
		tres = weights[0]
		for k in range(len(words)):
			tres += spamNums[j][k]*weights[k+1]
		pout = 0.0
		if tres > 0:
			pout = 1.0
		for k in range(len(words)):
			weights[k+1] += .05 * (1.0-pout) * spamNums[j][k]
	for j in range(hn):
		tres = weights[0]
		for k in range(len(words)):
			tres += hamNums[j][k]*weights[k+1]
		pout = 0.0
		if tres > 0:
			pout = 1.0
		for k in range(len(words)):
			weights[k+1] += .05 * (0-pout) * hamNums[j][k]

#Use the weights to calculate the sum of all weights for each spam and ham files.  If the sum is greater then 0 it is predicted to be a spam file.
tSpamPath = "test/spam/"
tSpamFiles = os.listdir(tSpamPath)
tHamPath = "test/ham/"
tHamFiles = os.listdir(tHamPath)
nTotal = len(tSpamFiles) + len(tHamFiles)
nCorrect = 0
for fileName in tSpamFiles:
	twords = []
	awords = []
	infile = open(tSpamPath+fileName, "r")
	for line in infile:
		nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
		lineWords = nLine.split()
		lineWords = [stemmer.stem(w1.lower()) for w1 in lineWords]
		awords.extend(w1 for w1 in lineWords if w1 in words)
		twords.extend(w1 for w1 in lineWords if w1 not in twords and w1 in words)
	infile.close()
	n = weights[0]
	for w1 in twords:
		n += weights[words.index(w1)+1]*awords.count(w1)
	if n > 0:
		nCorrect += 1
for fileName in tHamFiles:
	twords = []
	awords = []
	infile = open(tHamPath+fileName, "r")
	for line in infile:
		nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
		lineWords = nLine.split()
		lineWords = [stemmer.stem(w1.lower()) for w1 in lineWords]
		awords.extend(w1 for w1 in lineWords if w1 in words)
		twords.extend(w1 for w1 in lineWords if w1 not in twords and w1 in words)
	infile.close()
	n = weights[0]
	for w1 in twords:
		n += weights[words.index(w1)+1]*awords.count(w1)
	if n <= 0:
		nCorrect += 1
print nCorrect/nTotal
