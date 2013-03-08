#!/usr/bin/python
import nltk

def featureset(tweet):
    tweet=tweet.lower()
    words = tweet.split()
    for index in xrange(0, len(words)):
        words[index] = words[index].strip("\".1234567890()!\':\ ")
    
    index = 0
    while index < len(words):
        if(len(words[index]) <=1):
            words.remove(words[index])
        index += 1
    for stopword in nltk.corpus.stopwords.words('english'):
        if stopword in words:
            while True:
                try:
                    words.remove(stopword)
                except ValueError:
                    break
    frequencydict = dict()
    for word in words: 
        frequencydict[word] = frequencydict.get(word,0)+1
    return frequencydict

f=open('training.txt','rb')
tweets = f.readlines()
tweets = [(tweetext[:tweetext.find(' ')], tweetext[tweetext.find(' ')+1:tweetext.find(' ',tweetext.find(' ')+1)], tweetext[tweetext.find("'"):].strip("'\n")) for tweetext in tweets]
sports = open('sports.tweets','wb')
politics = open('politics.tweets', 'wb')
for tweet in tweets:
    if tweet[1] == 'Politics':
        politics.write(tweet[2]+'\n')
    else:
        sports.write(tweet[2]+'\n')
tw = [(tweet[2],tweet[1]) for tweet in tweets]
features = [(featureset(twi), label) for (twi,label) in tw]
train_set, test_set = features[:len(features)/2], features[len(features)/2:]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(100)
print classifier.classify(featureset('president of football association\'s son scored 7 goals'))