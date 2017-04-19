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

curr_time = date(2014, 06, 01)

def get_shutdown_index(day_of_last_review, alpha = 0.0001):  
    d0 = date(day_of_last_review)
    d1 = date(day_of_observation)
    delta = d0 - d1
    return 1/(math.log(delta).days+alpha)

def category(id):
    return store[id]["categories"]

def city(id):
    return store[id]["city"]

def state(id):
    return store[id]["state"]

def stars(id):
    return store[id]["stars"]

def review_cnt(id):
    return store[id]["review_cnt"]

def popularity(id)
    return review_cnt(id)/ age(id, curr_time)

def age(id):
    return (curr_time - store[id]["start_t"]).days

def elite_user(id):
    cnt = 0
    for user in store_user[id]:
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

        #row.append(name_size(business_id))
        #row.append(name_polar(business_id))
        #row.append(name_clarity(business_id))
        row.append(category(business_id)) 
        row.append(city(business_id))
        row.append(state(business_id))
        row.append(stars(business_id))
        row.append(review_count(business_id))
        row.append(popularity(business_id))
        row.append(age(business_id))
        #pos_score
        #neg_score
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
