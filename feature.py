"""
Input:
    data_id/train.p and data_id/valid.p which are list of business idx

Output:
    data/train_f.p and data/valid_f.p which are pairs in format (a list of features, ans)
    X = [name_size, name_polar, name_clarity, category, city, state, stars, review_count, popularity, age, pos_score, neg_score, elite_user]
    y = [SI]
"""
import pickle

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
# with open("dicts/meta.p") as f:
    # meta = pickle.load(f)
import pickle
from sentiment import *

def getPosNeg_score(b_id):
    with open("dicts/reviews.p", "r") as f1:
        reviews = pickle.load(f1)

    with open("dicts/store_review.p", "r") as f2:
        store = pickle.load(f2)

    pos=0
    neg=0
    pos_len=0
    neg_len=0

    for review_id in store[b_id]:
        if(reviews[review_id][pol]>=0):
            pos += reviews[review_id][pol]
            pos_len +=1
        else:
            neg += reviews[reivew_id][pol]
            neg_len +=1

    return pos/pos_len, neg/neg_len

def getNameSizePol(b_id):
    with open("dicts/store.p", "r") as f:
        store = pickle.load(f)

    return len(store[b_id].split(" ")), sentimentAnalizer(store[b_id]][name])[0][0]
curr_time =

def feature(ids):
    # Making Features
    data_f = []
    y = []

    for i in range(len(ids)):
        business_id = ids[i]
        row = []
        row.append(getNameSizePol(business_id)[0])
        row.append(getNameSizePol(business_id)[1])
        row.append(getPosNeg_score(business_id)[0])
        row.append(getPosNeg_score(business_id)[1])

        data_f.append(row)
        y.append(get_shutdown_index())

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


run()
