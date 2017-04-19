"""
Input:
    data_id/train.p and data_id/valid.p which are list of business idx

Output:
    data/train_f.p and data/valid_f.p which are pairs in format (a list of features, ans)
    X = [name_size, name_polar, name_clarity, category, city, state, stars, review_count, popularity, age, pos_score, neg_score, elite_user]
    y = [SI]
"""
import pickle
import time
import datetime
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
# with open("dicts/meta.p") as f:
    # meta = pickle.load(f)

curr_time = datetime.datetime(2014, 06, 01)

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
            neg += reviews[reivew_id]["pol"]
            neg_len += 1

    if(pos == 0):
        return 0, neg/neg_len
    elif(neg == 0):
        return pos/pos_len, 0
    else:
        return pos/pos_len, neg/neg_len

def name_size(b_id):
    return len(store[b_id]["name"].split())

def name_polar(b_id):
    return sentimentAnalizer(store[b_id]["name"])[0][0]

def get_shutdown_index(alpha=0.0001):
    #d1 = datetime.date(curr_time)
    delta = store[b_id]["end_t"] - curr_time
    return 1/(math.log(delta.days)+alpha)

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

def age(b_id):
    return (curr_time - store[b_id]["start_t"]).days

def elite_user(b_id):
    cnt = 0
    for user_id in store_user[b_id]:
        if user[user_id]['elite_year_cnt'] > 0:
            cnt = cnt + 1
    return cnt

def feature(ids):
    # Making Features
    data_f = []
    y = []

    for i in range(len(ids)):
        business_id = ids[i]
        row = []

        row.append(name_size(business_id))
        row.append(name_polar(business_id))
        #row.append(name_clarity(business_id))
        row.append(category(business_id))
        row.append(city(business_id))
        row.append(state(business_id))
        row.append(stars(business_id))
        row.append(review_cnt(business_id))
        row.append(popularity(business_id))
        row.append(age(business_id))
        row.append(getPosNeg_score(business_id))
        row.append(elite_user(business_id))

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
