#!/usr/bin/env python
import re
from collections import defaultdict
from nltk.corpus import stopwords 
from random import shuffle
from nltk.tag import pos_tag
import multiprocessing

def getstopwords():
	a = stopwords.words('english') + ['one','two','amp','best','the']
	return a 
def proc(a,flag=0):
	a = a.replace('\\u2019','\'')
	a = a.lower().split('\n')
	res = []
	pool = multiprocessing.Pool()
	for i in a :
		pool.apply_async(func=process(i),callback=res.append)
	pool.close()
	pool.join()
	return res

def process(i):
	if len(i) < 3 :
		return 
	d = {}	
	i = i.split()
	i = [w for w in i if w not in getstopwords()]
	d['twitid'] = i[0]
	if flag == 0:
		d['category'] = i[1]
		del(i[0])
		del(i[0])
	else:
		del(i[0])
	j = 0
	while j < len(i):
		i[j] = i[j].strip(r"!\$%\^&\*();:'\"\.,-_\?")
		if re.match(r"(http://)|(rt)",i[j]):
			del(i[j])
		j += 1
	d['data'] = i
	d['word2'] = [(a,b) for a in i for b in i if a!=b and pos_tag([a])[0][1] in ['NN','NNP'] and pos_tag([b])[0][1] in ['NN','NNP']]
	res.append(d)
	print d
	return d


def train(data):
	r = []
	for d in data:
		for a in d.get('data',None):
			f = {}
			g = {}		
			for temp in r:
				if temp['word'] == a:
					if temp['count'].get(d['category'],None):
						temp['count'][d['category']] += 1
					else:
						temp['count'][d['category']] = 1
					break
			else:
				f['word'] = a 
				if g.get(d['category'],None):
					g[d['category']] += 1
				else:
					g[d['category']] = 1   
				f['count'] = g
				r.append(f)
	r2 = []
	for a,b in d['word2']:
		f = {}
		g = {}
		flag1 = 0
		for temp in r:
			if temp.get('word2',None) == (a,b):
				if temp['count2'].get(d['category'],None):
					temp['count2'][d['category']] += 1
				else:
					temp['count2'][d['category']] = 1
				flag1 = 1
		if flag1 == 0:
			f['word2'] = (a,b)
			if g.get(d['category'],None):
				g[d['category']] += 1
			else:
				g[d['category']] = 1
			f['count2'] = g
			r2.append(f)
	return (r,r2)			

def validate(w):
	global features1,features2
	pc = 0
	sc = 0
	w = w.lower().split()
	w = [word for word in w if word not in getstopwords()]
	ser = ''
	for feature in features1:
		for word in w:
			flag = 0 
			if feature.get('word','') == word:
				if re.match(r"(#)|(@)",word):
					flag = 1
				c = feature.get('count',None)
				if c:
					p = c.get('politics',0)
					s = c.get('sports',0)
					pc += p
					sc += s
					if flag == 1 :
						pc += p**2
						sc += s**2
	word2 = [(a,b) for a in w for b in w if a!=b]
	for feature in features2:
		for a,b in word2:
			if feature.get('word2',None) == (a,b):
				c = feature.get('count2',None)
				if c:
					pc += c.get('politics',0)**5
					sc += c.get('sports',0)**5
	if pc > sc :
		return 'Politics'
	else:
		return 'Sports'

trdata = proc(open('training.txt','r').read())
a = len(trdata)
features1,features2 = train(trdata)
print features1
print features2
c = 0
nc = 0

#print validate("With four quality bowlers who can hurl the ball consistently at 140+kph Australia need not really worry about the nature of the pitch...")
'''
print '#'*80
print 'Word \t\tPolitics\t\tSports'
print '#'*80
features.sort()
for f in features:
	p = f['count']
	print "%s\t\t%s\t\t%s\t\t"%(f['word'],p.get('politics',0),p.get('sports',0))

st = ''
for i in trdata[a:]:
	if validate(' '.join(i['data'])) == i['category']:
		c += 1
	else:
		nc += 1
		st += '%s\t\t::%s\n'%(i['category'],' '.join(i['data']))
		print i
print c, nc
cr = float(100*c)/float(c+nc)
print 'correctness = %s' %(cr)
f = open("notcorrect.txt","w")
f.write(st)
f.close()
'''
valdata = proc(open('validation.txt','r').read())
f = open('output.txt','w')
for v in valdata:
	st = v['twitid'] +'\t'+ validate(' '.join(v['data']))+'\n'
	f.write(st)
f.close()
