import pandas as pd
import numpy as np
import json
import pickle
'''
user = {}
for line in open('yelp_academic_dataset_user.json', 'r'):
    for element in line:
    	if element
'''
yelp_user = []
for line in open('dataset/yelp_academic_dataset_user.json', 'r'):
    yelp_user.append(json.loads(line))

temp = {}
for ele in yelp_user:
	a = []
	a.append(ele['review_count'])
	a.append(ele['yelping_since'])
	a.append(len(ele['friends']))
	a.append(ele['fans'])
	a.append(len(ele['elite']))
	a.append(ele['average_stars'])
	temp[ele['user_id']] = a
#print(temp)
pickle.dump(temp, open( "user.p", "wb" ) )
