import re
from collections import defaultdict
from nltk.corpus import stopwords 
def proc(a):
	a = a.lower().split('\n')
	res = []
	for i in a :
		if len(i) < 3 :
			break
		d = {}	
		i = i.split()
		i = [w for w in i if w not in stopwords.words('english')]
		j = 0
		while j < len(i):
			if re.match(r"http://",i[j]):
				del(i[j])
			j +=1
		d['twitid'] = i[0]
		d['category'] = i[1]
		d['data'] = i[2:]
		res.append(d)
	return res
def train(data):
	r = []
	for d in data:
		for a in d['data']:
			f = {}
			g = {}
			flag = 1
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
	if pc > sc :
		return 'politics'
	else:
		return 'sports'
trdata = proc(open('training.txt','r').read())
a = len(trdata)*7/8
features = train(trdata[:a])
c = 0
nc = 0
for i in trdata[a:]:
	if validate(' '.join(i['data'])) == i['category'].lower():
		c += 1
	else:
		nc += 1
print c, nc