from __future__ import division
from nltk.stem import PorterStemmer
import sys
import os
from math import log, exp

#get parameters lr = logarithmic regression (naive bayes otherwise), stop = use stop words, fs = use feature selector
stop = True
lr = False
fs = False
if sys.argv[2] == "yes":
	stop = False
if sys.argv[1] == "lr":
	lr = True
if sys.argv[3] == "yes":
	fs = True

#get all spam and ham file names
stemmer = PorterStemmer()
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
spamWords = []
hamWords = []
for fileName in spamFiles:
	infile = open(spamPath+fileName, "r")
	for line in infile:
		nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
		lineWords = nLine.split()
		lineWords = [stemmer.stem(w.lower()) for w in lineWords]
		if stop:
			spamWords.extend(lineWords)
			words.extend(w for w in lineWords if w not in words)
		else:
			spamWords.extend(w for w in lineWords if w not in stopWords)
			words.extend(w for w in lineWords if w not in words and w not in stopWords)
	infile.close()
for fileName in hamFiles:
	infile = open(hamPath+fileName, "r")
	for line in infile:
		nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
		lineWords = nLine.split()
		lineWords = [stemmer.stem(w.lower()) for w in lineWords]
		if stop:
			hamWords.extend(lineWords)
			words.extend(w for w in lineWords if w not in words)
		else:
			hamWords.extend(w for w in lineWords if w not in stopWords)
			words.extend(w for w in lineWords if w not in words and w not in stopWords)
	infile.close()

#Simple feature selector that eliminates words that were only found once
if fs:
	words = [words[i] for i in range(len(words)) if hamWords.count(words[i])+spamWords.count(words[i]) > 1]
	hamWords = [w for w in hamWords if w in words]
	spamWords = [w for w in spamWords if w in words]

#Run data using Naive Bayes
if not lr:
	#Populate prob with probabilities of each word being in spam and ham
	prob = [[0 for j in range(len(words))] for i in range(2)]
	nums = [[0 for j in range(len(words))] for i in range(2)]
	for i in range(len(words)):
		nums[0][i] = spamWords.count(words[i])+1
		nums[1][i] = hamWords.count(words[i])+1
	ssum = sum(nums[0])
	hsum = sum(nums[1])
	for i in range(len(words)):
		prob[0][i] = nums[0][i]/ssum
		prob[1][i] = nums[1][i]/hsum

	#For each spam and ham test file, find probability of it being a spam and ham file and choose the larger one
	tSpamPath = "test/spam/"
	tSpamFiles = os.listdir(tSpamPath)
	tHamPath = "test/ham/"
	tHamFiles = os.listdir(tHamPath)
	nTotal = len(tSpamFiles) + len(tHamFiles)
	nCorrect = 0
	for fileName in tSpamFiles:
		hScore = log(pHam)
		sScore = log(pSpam)
		infile = open(tSpamPath+fileName, "r")
		for line in infile:
			nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
			lineWords = nLine.split()
			lineWords = [stemmer.stem(w.lower()) for w in lineWords]
			for w in lineWords:
				if w in words:
					ind = words.index(w)
					hScore += log(prob[1][ind])
					sScore += log(prob[0][ind])
		infile.close()
		if sScore > hScore:
			nCorrect += 1
	for fileName in tHamFiles:
		hScore = log(pHam)
		sScore = log(pSpam)
		infile = open(tHamPath+fileName, "r")
		for line in infile:
			nLine = ''.join(l for l in line if l.isalpha() or l.isspace())
			lineWords = nLine.split()
			lineWords = [stemmer.stem(w.lower()) for w in lineWords]
			for w in lineWords:
				if w in words:
					ind = words.index(w)
					hScore += log(prob[1][ind])
					sScore += log(prob[0][ind])
		infile.close()
		if hScore > sScore:
			nCorrect += 1
	print nCorrect/nTotal

#Run data using logarithmic regression
else:
	#Use logarithmic regression to set values to each word for both possible outcomes.  Repeated 100 times for convergence with lambda = .01
	nums = [[0 for j in range(len(words)+1)] for i in range(2)]
	nums[0][0] = 1
	nums[1][0] = 1
	for i in range(len(words)):
		nums[1][i+1] = spamWords.count(words[i])
		nums[0][i+1] = hamWords.count(words[i])
	pr = [0.0, 0.0]
	w = [0.0 for i in range(len(words)+1)]
	for p in range(100):
		for i in range(2):
			n = 0
			for j in range(len(nums[i])):
				n += w[j]*nums[i][j]
			try:
				pr[i] = exp(n)/(1+exp(n))
			except:
				pr[i] = .999999
		dw = [0.0 for i in range(len(words)+1)]
		for i in range(len(dw)):
			for j in range(2):
				dw[i] += nums[j][i]*(j-pr[j])
		for i in range(len(w)):
			w[i] += .01*(dw[i]-.01*w[i])

	#For each spam and ham test file, find probability of it being a spam and ham file and choose the larger one
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
		n = 0.0
		for w1 in twords:
			n += w[words.index(w1)+1]*awords.count(w1)
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
		n = 0.0
		for w1 in twords:
			n += w[words.index(w1)+1]*awords.count(w1)
		if n <= 0:
			nCorrect += 1
	print nCorrect/nTotal
