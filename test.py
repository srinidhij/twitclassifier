import re
f = open('training.txt','r')
data = f.read().lower()
dl =  data.split('\n')
data = []
for i in dl:
	dd = {}
	i = i.split(' ')
	if len(i) > 2:
		dd['tweedid'] = i[0]
		dd['category'] = i[1]
		temp = ' '.join(i[2:])
		dd['data'] = ' '.join(re.findall('[a-z]+',temp))
		data.append(dd)
print data