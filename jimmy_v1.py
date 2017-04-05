import pandas as pd
import numpy as np
import json
import pickle

result = []
for line in open('yelp_dataset/yelp_academic_dataset_business.json', 'r'):
    result.append(json.loads(line))
    
tmp = []
for each in result:
    tmp.append(each['business_id'])
    
store_review = dict.fromkeys(tmp)

review = []
for line in open('yelp_dataset/yelp_academic_dataset_review.json', 'r'):
    review.append(json.loads(line))

for each in review:
    if (store_review[each['business_id']] is None):
        store_review[each['business_id']]=[each['text']]
    else:
        store_review[each['business_id']].append(each['text'])    

pickle.dump( store_review, open( 'store_review.p', 'w+b' ) )