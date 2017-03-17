from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def sentimentAnalizer(text):
    pattern = TextBlob(text)
    bayes = TextBlob(text, analyzer=NaiveBayesAnalyzer())

    return pattern.sentiment, bayes.sentiment
//patternTuple(polarity[-1.0, 1.0], subjectivity[0.0, 1.0])
//NaiveBayesTuple(classification['pos', 'neg'], p_pos[0.0, 1.0], p_neg[0.0, 1.0])


//find out text with differnt classiciation

sentimentResult = [] //[text, polarity, classified, [0, 1]] 同號為1, 異號為0
for t in result[:100]:
    tmp = []
    tmp.append(t['text'])
    polarity = sentimentAnalizer(t['text'])[0][0]
    classified = sentimentAnalizer(t['text'])[1][0]
    tmp.append(polarity)
    tmp.append(classified)
    if(polarity > 0 and classified == 'pos'):
        tmp.append(1)
    elif(polarity < 0 and classified == 'neg'):
        tmp.append(1)
    else:
        tmp.append(0)
    sentimentResult.append(tmp)

for each in sentimentResult:
    if(each[3]==0):
        print("{0}\n".format(each))
