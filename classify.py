#!/usr/bin/env python
import re
from collections import defaultdict
from nltk.corpus import stopwords 
from random import shuffle
from nltk.stem.snowball import EnglishStemmer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import multiprocessing

stemmer = EnglishStemmer()
def getstopwords():
	a = stopwords.words('english') + ['one','two','amp','best','the','once','twice','nine','it\'s']
	return a 

def proc(a,flag=0):
	'''process text : takes the entire file content as 
	input and returns a list of form [{twitid:'2352514364257',category:'Politics',
	data:['fasd','asdf','g', 'dfg','dsg ']}.....]'''
	#flag = 0 only for training data
	a = a.replace('\\u2019','\'')
	a = a.lower().split('\n') #a is a list of tweets
	res = []
	pool = multiprocessing.Pool()
	for i in a:
		pool.apply_async(processor, (i,), callback=res.append)
	pool.close()
	pool.join()
	if flag ==0 :
		print 'Training done'
	return res

def processor(i,flag=0):
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
		i[j] = i[j].strip(r"!\$%\^&\*();:\?'\"\.,-_")
		i[j] = i[j].replace('\\u2019','\'')
		if re.match(r"(http://)|(rt)|(\\u2013)",i[j]):
			del(i[j])
		j += 1
	d['data'] = [stemmer.stem(word).encode('ascii') for word in i]
	d['word2']= [(a,b) for a in d['data'] for b in d['data'] if a!=b and pos_tag([a])[0][1] == 'NN' and pos_tag([b])[0][1] == 'NN']
	return d

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
	for d in data:
		for a,b in d['word2'] :
			f = {}
			g = {}
			flag = 1
			for temp in r:
				if temp.get('word2',None) == (a,b):
					if temp['count2'].get(d['category'],None):
						temp['count2'][d['category']] += 1
						flag = 0
					else:
						temp['count2'][d['category']] = 1
						flag = 0 
						break
			if flag == 1:
				f['word2'] = (a,b)
				if g.get(d['category'],None) :
					g[d['category']] += 1
				else :
					g[d['category']] = 1
				f['count2'] = g
				r.append(f)
	return r			

def validate(w):
	'''Validates based on word count present in features'''
	f = open("features.txt","a")
	global features
	pc = 0
	sc = 0
	w = w.lower().split()
	w = [word for word in w if word not in getstopwords()]
	ser = ''
	something = [word for word in w if word in features.keys()]
	for word in something:
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
				pc += p*p
				sc += s*s
			print pc,sc,word
	w2 = [(a,b) for a in w for b in w if a!=b and pos_tag([a])[0][1] == 'NN' and pos_tag([b])[0][1] == 'NN']
	for feature in features :
		for a,b in w2:
			if (a,b) in feature['word2']:
				c = feature.get('count2',None)
				if c:
					p = c.get('politics',0)
					s = c.get('sports',0)
					pc += p**5
					sc += s**5
					print pc,sc,word 
	lis= [value for feature, value in features if featue=='word2' and value==(a,b)]
	f.write(ser)
	f.close()
	if pc > sc :
		return 'Politics'
	else:
		return 'Sports'
trdata = proc(open('training.txt','r').read())
a = len(trdata)*19/20
shuffle(trdata)
features = train(trdata[:a])
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
