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
	a = a.replace('\\u2019','\'')
	a = a.lower().split('\n')
	res = []
	for i in a :
		if len(i) < 3 :
			break
		d = {}	
		i = i.split()
		i = [w for w in i if w not in getstopwords()]
		d['twitid'] = i[0]
		d['category'] = i[1]
		del(i[0])
		del(i[0])
		j = 0
		while j < len(i):
			i[j] = i[j].strip(r"!\$%\^&\*();:'\"\.,-_")
			if re.match(r"(http://)|(rt)",i[j]):
				del(i[j])
			j += 1
		#i = re.findall("[a-z#@\\d]+",' '.join(i))
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
def validate(w):
	f = open("features.txt","a")
	global features
	pc = 0
	sc = 0
	w = w.lower().split()
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
						pc += 999*p
						sc += 999*s
					ser += 'Pol : %s\t\tSports: %s\n'%(p,s)
					print word, p ,s
	f.write(ser)
	f.close()
	if pc > sc :
		return 'politics'
	else:
		return 'sports'
trdata = proc(open('training.txt','r').read())
a = len(trdata)*49/50
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