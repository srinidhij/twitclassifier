import re
from collections import defaultdict
from nltk.corpus import stopwords 
from random import shuffle
def getstopwords():
	a = stopwords.words('english')
	a.append('one')
	a.append('two')
	a.append('amp')
	a.append('best')

	return a 
def proc(a):
	a = a.lower().split('\n')
	res = []
	for i in a :
		if len(i) < 3 :
			break
		d = {}	
		i = i.split()
		i = [w for w in i if w not in getstopwords()]
		j = 0
		d['twitid'] = i[0]
		d['category'] = i[1]
		del(i[0])
		del(i[1])
		while j < len(i):
			i[j] = i[j].strip(r'&\'\"-_\.:()!,;')
			if re.match(r"(http://)|(rt)",i[j]):
				del(i[j])
			j +=1
		d['data'] = i
		res.append(d)
	return res
def train(data):
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
def validate(s):
	global features
	pc = 0
	sc = 0
	s = s.lower().split()
	for f in features:
		for word in s:
			if f['word'] == word:
				p = f.get('count',None)
				if p:
					pc += p.get('politics',0)
					sc += p.get('sports',0)
					print word, pc ,sc
	if pc > sc :
		return 'politics'
	else:
		return 'sports'
trdata = proc(open('training.txt','r').read())
a = len(trdata)*5/6
shuffle(trdata)
features = train(trdata[:a])
c = 0
nc = 0
'''
print '#'*80
print 'Word \t\tPolitics\t\tSports'
print '#'*80
features.sort()
for f in features:
	p = f['count']
	print "%s\t\t%s\t\t%s\t\t"%(f['word'],p.get('politics',0),p.get('sports',0))
'''
for i in trdata[a:]:
	if validate(' '.join(i['data'])) == i['category']:
		c += 1
	else:
		nc += 1
		print i
print c, nc
print 'correctness = %s' %((100*c)/(c+nc))