"""
Input:
    data_id/train.p and data_id/test.p which are list of business idx

Output:
    data/train_f.p and data/test_f.p which are pairs in format (a list of features, ans)
    X = [name_size, name_polar, name_clarity, category, city, state, stars, review_count, popularity, pos_score, neg_score, elite_user]
    y = [is_closed]
"""
import utils
import time
import datetime
# import gensim
from sentiment import *
# dicts = ["user", "store", "reviews", "store_review", "store_user", "meta", "pair_d"]

user = utils.load("dicts/user.p")
store = utils.load("dicts/store.p")
reviews = utils.load("dicts/reviews.p")
store_review = utils.load("dicts/store_review.p")
store_user = utils.load("dicts/store_user.p")
# store_pair = utils.load("dicts/store_pair.p")

# model = gensim.models.KeyedVectors.load_word2vec_format('word2vec/GoogleNews-vectors-negative300.bin', binary=True)

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

def get_y(b_id, observe_t = 12):
    life_time = store[b_id]["end_t"] - store[b_id]["start_t"]
    longer = life_time.days/30 - observe_t
    if longer > 0:
        return store[b_id]["is_open"]
    else:
        if store[b_id]["is_open"]:
            return -1
        else:
            return 0

def category(b_id):
    return store[b_id]["categories"]

def city(b_id):
    return store[b_id]["city"]

def state(b_id):
    return store[b_id]["state"]

def stars(b_id):
    return store[b_id]["stars"]

# def review_cnt(b_id):
#     return store[b_id]["review_cnt"]

def popularity(b_id):
    return len(store_review[b_id])

def elite_user(b_id, observe_t=12):
    cnt = 0
    for user_id in store_user[b_id]:
        if user[user_id]["elite"][0] == "None":
            continue
        for yr in user[user_id]["elite"]:
            eli_date = datetime.datetime(int(yr), 1, 1)
            diff = eli_date - store[b_id]["start_t"]
            if diff.days/30 < observe_t:
                cnt = cnt + 1
                break
    return cnt


def feature(ids):
    # Making Features
    data_f = []
    y = []
    for i in range(len(ids)):
        business_id = ids[i]
        label = get_y(business_id)
        if label == -1:
            continue
        row = []
        row.append(name_size(business_id))
        row.append(name_polar(business_id))
        # row.append(name_clarity(business_id))
        row.append(category(business_id))
        row.append(city(business_id))
        row.append(state(business_id))
        row.append(stars(business_id))
        # row.append(review_cnt(business_id))
        row.append(popularity(business_id))
        row.append(getPosNeg_score(business_id))
        row.append(elite_user(business_id))
        data_f.append(row)
        y.append(label)

    return data_f, y


def run():

    # Making Features for Training
    t1 = time.time()
    train_id = utils.load("data_id/train.p")
    utils.dump(feature(train_id), "data/train_f.p")
    print ("train:", time.time()-t1)

    # Making Features for Testing
    t1 = time.time()
    test_id = utils.load("data_id/test.p")
    utils.dump(feature(test_id), "data/test_f.p")
    print ("test:", time.time()-t1)


if __name__ == "__main__":
    run()
