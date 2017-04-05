import pickle
import json
from datetime import datetime

def store():
    store = {}
    with open("dataset/yelp_academic_dataset_business.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            store[business_id] = {}
            store[business_id]["name"] = line["name"]
            store[business_id]["city"] = line["city"]
            store[business_id]["state"] = line["state"]
            store[business_id]["latitude"] = line["latitude"]
            store[business_id]["longitude"] = line["longitude"]
            store[business_id]["stars"] = 0
            store[business_id]["review_cnt"] = line["review_count"]
            store[business_id]["is_open"] = line["is_open"]
            store[business_id]["categories"] = line["categories"]


    # user = pickle.load("dicts/user.p") # load user dict to compute stars

    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            user_id = line["user_id"]
            date = datetime.strptime(line["date"], "%Y-%m-%d")
            # store[business_id]["stars"] += (line["stars"]-user[user_id]["avg_stars"])
            if "start_t" in store[business_id]:
                if date > store[business_id]["end_t"]:
                    store[business_id]["end_t"] = date
                if date < store[business_id]["start_t"]:
                    store[business_id]["start_t"] = date
            else:
                store[business_id]["start_t"] = date
                store[business_id]["end_t"] = date
    for k in store.keys():
        store[k]["stars"] /= store[k]["review_cnt"]
    pickle.dump(store, open("dicts/store.p", "wb"))

def meta():
    meta = {}
    meta["curr_time"] = None
    meta["city_map"] = {}
    meta["state_map"] = {}
    meta["state_avg_d"] = {}

    with open("dataset/yelp_academic_dataset_business.json", "r") as f:
        for line in f:
            line = json.loads(line)
            if line["city"] in meta["city_map"]:
                meta["city_map"][line["city"]] += 1
            else:
                meta["city_map"][line["city"]] = 1
            if line["state"] in meta["state_map"]:
                meta["state_map"][line["state"]] += 1
            else:
                meta["state_map"][line["state"]] = 1
    meta["city_count"] = len(meta["city_map"])
    meta["state_count"] = len(meta["state_map"])
    pickle.dump(meta, open("dicts/meta.p", "wb"))

def user():
    temp = {}
    with open("dataset/yelp_academic_dataset_user.json", "r") as f:
        for line in f:
            line = json.loads(line)
            user_id = line['user_id']
            temp[user_id] = {}
            temp[user_id]['review_cnt'] = line['review_count']
            temp[user_id]['yelp_since'] = line['yelping_since']
            temp[user_id]['friends_cnt'] = len(line['friends'])
            temp[user_id]['fans'] = line['fans']
            temp[user_id]['elite_year_cnt'] = len(line['elite'])
            temp[user_id]['avg_stars'] = line['average_stars']
    pickle.dump(temp, open( "user.p", "wb" ))

def store_review():
    store_user = {}
        with open("dataset/yelp_academic_dataset_review.json", "r") as f:
            #with open("test_review.json", "r") as f:
            for line in f:
                line = json.loads(line)
                user_id = line['user_id']
                business_id = line['business_id']
                value = store_user.get(business_id)
                if value is None:
                    store_user[business_id] = [user_id]
                else:
                    store_user[business_id].append(user_id)
    pickle.dump(store_user, open( "store_user.p", "wb" ))
