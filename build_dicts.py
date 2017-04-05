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
    yelp_user = []
    for line in open('dataset/yelp_academic_dataset_user.json', 'r'):
        yelp_user.append(json.loads(line))
    
    temp = {}
    for ele in yelp_user:
        a = {}
        #review_cnt yelp_age(yelp_since) friends_cnt fans elite_year_cnt avg_stars
        a['review_cnt'] = ele['review_count']
        a['yelp_since'] = ele['yelping_since']
        a['friends_cnt'] = len(ele['friends'])
        a['fans'] = ele['fans']
        a['elite_year_cnt'] = len(ele['elite'])
        a['avg_stars'] = ele['average_stars']
        temp[ele['user_id']] = a
    pickle.dump(temp, open( "user.p", "wb" ))

