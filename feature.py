"""
Input:
    data_id/train.p and data_id/valid.p which are list of business idx

Output:
    data/train_f.p and data/valid_f.p which are pairs in format (a list of features, ans)
    X = [name_size, name_polar, name_clarity, category, city, state, stars, review_count, popularity, pos_score, neg_score, elite_user]
    y = [SI]
"""
import pickle
import time
import datetime
import math
import gensim
from sentiment import *
# dicts = ["user", "store", "reviews", "store_review", "store_user", "meta", "pair_d"]

with open("dicts/user.p", "r") as f:
    user = pickle.load(f)
with open("dicts/store.p", "r") as f:
    store = pickle.load(f)
with open("dicts/reviews.p", "r") as f:
    reviews = pickle.load(f)
with open("dicts/store_review.p", "r") as f:
    store_review = pickle.load(f)
with open("dicts/store_user.p", "r") as f:
    store_user = pickle.load(f)
with open("dicts/store_pair.p", "r") as f:
    store_pair = pickle.load(f)
# with open("dicts/meta.p") as f:
    # meta = pickle.load(f)

<<<<<<< HEAD
#word2vec model
model = gensim.models.KeyedVectors.load_word2vec_format('word2vec/GoogleNews-vectors-negative300.bin', binary=True) 
curr_time = datetime.datetime(2014, 06, 01)
=======
>>>>>>> refs/remotes/origin/develop

def getPosNeg_score(b_id):
    pos = 0.0
    neg = 0.0
    pos_len = 0.0
    neg_len = 0.0

    for review_id in store_review[b_id]:
        if reviews[review_id]["pol"] >= 0:
            pos += reviews[review_id]["pol"]
            pos_len += 1
        else:
            neg += reviews[review_id]["pol"]
            neg_len += 1

    if pos_len:
        pos /= pos_len
    if neg_len:
        neg /= neg_len
    return pos, neg

def name_size(b_id):
    return len(store[b_id]["name"].split())

def name_polar(b_id):
    return sentimentAnalizer(store[b_id]["name"])[0][0]
	
def Name_ClarityAndMissing(b_id):      
    tmp_sum=0.0
    count=0.0
    
	if not store[b_id]['categories']:
		return 0.5, 1
	else:		
		for each in store[b_id]['categories']:
			try:
				tmp_sum += model.similarity(each, store[b_id]['name'])
				count+=1
			except:
				
		if count:
			return tmp_sum/count, 0
		else:
			return 0.5, 1
					
def get_shutdown_index(b_id, alpha=0.0001):
    delta = store[b_id]["end_t"] - curr_time
    return delta.days

def category(b_id):
    return store[b_id]["categories"]

def city(b_id):
    return store[b_id]["city"]

def state(b_id):
    return store[b_id]["state"]

def stars(b_id):
    return store[b_id]["stars"]

def review_cnt(b_id):
    return store[b_id]["review_cnt"]

def popularity(b_id):
    return age(b_id)/review_cnt(b_id)

def elite_user(b_id):
    cnt = 0
    for user_id in store_user[b_id]:
        if user[user_id]['elite_year_cnt'] > 0:
            cnt = cnt + 1
    return cnts

def feature(ids):
    # Making Features
    data_f = []
    y = []
    for i in range(len(ids)):
        business_id = ids[i]
        row = []
        if business_id not in store_review:
            print business_id
            continue
        row.append(name_size(business_id))
        row.append(name_polar(business_id))
        row.extend(Name_ClarityAndMissing(business_id))
        row.append(category(business_id))
        row.append(city(business_id))
        row.append(state(business_id))
        row.append(stars(business_id))
        row.append(review_cnt(business_id))
        row.append(popularity(business_id))
        row.append(getPosNeg_score(business_id))
        row.append(elite_user(business_id))

        data_f.append(row)
        y.append(get_shutdown_index(business_id))

    return data_f, y


def run():

    # Making Features for Training
    with open("data_id/train.p", "r") as f:
        train_id = pickle.load(f)
    with open("data/train_f.p", "w") as f:
        pickle.dump(feature(train_id), f)

    # Making Features for Validation
    with open("data_id/valid.p", "r") as f:
        valid_id = pickle.load(f)
    with open("data/valid_f.p", "w") as f:
        pickle.dump(feature(valid_id), f)


if __name__ == "__main__":
    run()
