#!/usr/bin/env python
import re
from collections import defaultdict
from nltk.corpus import stopwords 
from random import shuffle
def getstopwords():
	a = stopwords.words('english') + ['one','two','amp','best','the','once','twice','nine','it\'s']
	return a 

def proc(a,flag=0):
	'''process text : takes the entire file content as 
	input and returns a list of form [{twitid:'2352514364257',category:'Politics',
	data:['fasd','asdf','g', 'dfg','dsg '}.....]'''
	#flag = 0 only for training data
	a = a.lower().replace('\\u2019','\'')
	a = a.split('\n')
	res = []
	for i in a :
		if len(i) < 3 :
			break
		d = {}	
		i = i.split()
		i = [w for w in i if w not in getstopwords()]
		d['twitid'] = i[0]
		if flag == 0:
			#Training data
			d['category'] = i[1]
			del(i[0])
			del(i[0])
		else:
			del(i[0])
		j = 0
		while j < len(i):
			i[j] = i[j].strip(r"/!\$%\^&\*();:'\"\.,-_")
			i[j] = i[j].replace('\\u2019','\'')
			if re.match(r"(http://)|(rt)|(\\u2013)",i[j]):
				del(i[j])
			j += 1
		d['data'] = i
		res.append(d)
	return res

def train(data):
	'''Creates a list of features of the form [{word:'asdfba',count:{politics:10,sports:0}}]'''
	r = []
	for d in data:
		for a in d['data']:
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
	return r			

def validate(w):
	'''Validates based on word count present in features'''
	f = open("features.txt","a")
	global features
	pc = 0
	sc = 0
	w = w.split()
	w = [word for word in w if word not in getstopwords()]
	ser = ''
	for feature in features:
		for word in w:
			flag = 0 
			if feature['word'] == word:
				if re.match(r"(#)|(@)",word):
					flag = 1
				ser += '%s :: '%(word)
				c = feature.get('count',None)
				if c:
					p = c.get('politics',0)
					s = c.get('sports',0)
					pc += p
					sc += s
					if flag == 1 :
						pc += 999999999999*p
						sc += 999999999999*s
					ser += 'Pol : %s\t\tSports: %s\n'%(p,s)
					print word, p ,s
	f.write(ser)
	f.close()
	if pc > sc :
		return 'Politics'
	else:
		return 'Sports'
trdata = proc(open('training.txt','r').read())
features = train(trdata)
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
valdata = proc(open('validation.txt','r').read(),flag=1)
f = open('output.txt','w')
for v in valdata:
	st = v['twitid'] +'\t'+ validate(' '.join(v['data']))+'\n'
	f.write(st)
f.close()
