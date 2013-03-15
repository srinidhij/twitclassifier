#!/usr/bin/env python
import re
from collections import defaultdict
from nltk.corpus import stopwords 
from random import shuffle
from nltk.tag import pos_tag
import multiprocessing

swords = []
def getstopwords():
	global swords
	swords = stopwords.words('english') + ['one','two','amp','best','the']
getstopwords()

def proc(twitdat,flag=0):
	twitdat = twitdat.replace('\\u2019','\'')
	twitdat = twitdat.lower().split('\n')
	result = []
	for dat in twitdat :
		if len(dat) < 3 :
			return 
		tempdict = {}	
		dat = dat.split()
		dat = [w for w in dat if w not in swords]
		tempdict['twitid'] = dat[0]
		if flag == 0:
			tempdict['category'] = dat[1]
			del(dat[0])
			del(dat[0])
		else:
			del(dat[0])
		j = 0
		while j < len(dat):
			dat[j] = dat[j].strip(r"!\$%\^&\*();:'\"\.,-_\?")
			if re.match(r"(http://)|(rt)",dat[j]):
				del(dat[j])
			j += 1
		tempdict['data'] = dat
		result.append(tempdict)
		return tempdict
	return result

def train(data):
	result = []
	for tdat in data:
		for a in tdat.get('data',None):
			fdict = {}
			gdict = {}		
			for temp in r:
				if temp['word'] == a:
					if temp['count'].get(tdat['category'],None):
						temp['count'][tdat['category']] += 1
					else:
						temp['count'][tdat['category']] = 1
					break
			else:
				fdict['word'] = a 
				if gdict.get(tdat['category'],None):
					gdict[tdat['category']] += 1
				else:
					gdict[tdat['category']] = 1   
				fdict['count'] = gdict
				result.append(f)
	return result			

def validate(twit):
	global features
	polc = 0
	spoc = 0
	twit = twit.lower().split()
	for feature in features1:
		for word in twit:
			flag = 0 
			if feature.get('word','') == word:
				if re.match(r"(#)|(@)",word):
					flag = 1
				count = feature.get('count',None)
				if c:
					p = c.get('politics',0)
					s = c.get('sports',0)
					polc += p
					spoc += s
					if flag == 1 :
						polc += p**10
						spoc += s**10
	if polc > spoc :
		return 'Politics'
	else:
		return 'Sports'

trdata = proc(open('training.txt','r').read())
a = len(trdata)
features1= train(trdata)
print features1
valdata = proc(open('validation.txt','r').read())
f = open('output.txt','w')
for v in valdata:
	st = v['twitid'] +'\t'+ validate(' '.join(v['data']))+'\n'
	f.write(st)
f.close()
