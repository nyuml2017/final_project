"""
Input:
    data_id/train.p and data_id/valid.p which are list of business idx
Output:
    data/train_f.p and data/valid_f.p which are pairs in format (a list of features, ans)
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

def feature(ids):
    # Making Features
    data_f = []

    for i in range(len(ids)):
        business_id = ids[i]
        row = []

    return data_f

def run():

    # Making Features for Training
    with open("data_id/train.p", "r") as f:
        train_id = pickle.load(f)

    train_f = feature(train_id)

    with open("data/train_f.p", "w") as f:
        pickle.dump(train_f, f)

    # Making Features for Validation
    with open("data_id/valid.p", "r") as f:
        valid_id = pickle.load(f)

    valid_f = feature(train_id)

    with open("data/valid_f.p", "w") as f:
        pickle.dump(valid_f, f)


run()
