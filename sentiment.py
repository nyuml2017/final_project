from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def sentimentAnalizer(text):
    pattern = TextBlob(text)
    bayes = TextBlob(text, analyzer=NaiveBayesAnalyzer())

    return pattern.sentiment, bayes.sentiment
'''
input: text
output:
patternTuple(polarity[-1.0, 1.0], subjectivity[0.0, 1.0])
NaiveBayesTuple(classification['pos', 'neg'], p_pos[0.0, 1.0], p_neg[0.0, 1.0])
'''

def compareModel(text):

    tmp = [text] #[text, polarity, classified, [0, 1]] if the 2 models prediction is same = 1, otehrwise 0
    polarity = sentimentAnalizer(text)[0][0]
    classified = sentimentAnalizer(text)[1][0]
    tmp.append(polarity)
    tmp.append(classified)
    if(polarity > 0 and classified == 'pos'):
        tmp.append(1)
    elif(polarity < 0 and classified == 'neg'):
        tmp.append(1)
    else:
        tmp.append(0)
    sentimentResult.append(tmp)

    return tmp

'''
Compare result of 2 differnt sentiment model
intput: text
out put: a list of [text, polarity from pattern, classified from bayes, [0, 1]]
if the 2 models prediction is same 1, otehrwise 0
'''