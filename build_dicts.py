import pickle
import json
from datetime import datetime
from textblob import TextBlob
from geopy.distance import vincenty

def store():
    store = {}
    store_review = {}
    store_user = {}
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

    with open("dicts/user.p", "r") as f: # load user dict to compute stars
        user = pickle.load(f)

    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            user_id = line["user_id"]
            date = datetime.strptime(line["date"], "%Y-%m-%d")
            store[business_id]["stars"] += (line["stars"]-user[user_id]["avg_stars"])
            if "start_t" in store[business_id]:
                if date > store[business_id]["end_t"]:
                    store[business_id]["end_t"] = date
                if date < store[business_id]["start_t"]:
                    store[business_id]["start_t"] = date
            else:
                store[business_id]["start_t"] = date
                store[business_id]["end_t"] = date
            if business_id in store_review:
                store_review[business_id].append(line["review_id"])
            else:
                store_review[business_id] = [line["review_id"]]
            if business_id in store_user:
                store_user[business_id].append(user_id)
            else:
                store_user[business_id] = [user_id]
    for k in store.keys():
        store[k]["stars"] /= store[k]["review_cnt"]

    with open("dicts/store.p", "wb") as f:
        pickle.dump(store, f)
    with open("dicts/store_review.p", "wb") as f:
        pickle.dump(store_review, f)
    with open("dicts/store_user.p", "wb") as f:
        pickle.dump(store_user, f)

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

    with open("dicts/meta.p", "wb") as f:
        pickle.dump(meta, f)

def reviews():
    reviews = {}
    i = 0
    d = 1
    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            pattern = TextBlob(line['text'])
            pol = pattern.sentiment[0]
            sub = pattern.sentiment[1]

            sentences = line['text'].split('.')
            s1 = 0
            s2 = 0
            valid_sen = 0

            for sen in sentences:
                if not sen: # empty string
                    continue
                pattern = TextBlob(sen)
                s1 += pattern.sentiment[0]
                s2 += pattern.sentiment[1]
                valid_sen += 1
            if valid_sen:
                pol_avg = s1/valid_sen
                sub_avg = s2/valid_sen

            tmpDict = {'user_id': line['user_id'], 'stars': line['stars'], 'date': line['date'],
                       'pol': pol, 'sub': sub,
                       'pol_avg': pol_avg, 'sub_avg': sub_avg}
            reviews[line['review_id']] = tmpDict
            i += 1
            if i%10000 == 0:
                filename = "dicts/reviews_" + str(d) + ".p"
                with open(filename, 'wb') as f:
                    pickle.dump(reviews, f)
                reviews = {}
                d += 1
                i = 0

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
    with open("dicts/user.p", "wb") as f:
        pickle.dump(temp, f)

def pair_dist():
    temp = []
    with open("dataset/yelp_academic_dataset_business.json", "r") as f:
            #with open("test_busi.json", "r") as f:
        for line in f:
            line = json.loads(line)
            temp.append(line)
    leng = len(temp)
    pair_d = {}
    for i in range(leng):
        for j in range(i+1, leng):
            busi_1 = temp[i]['business_id']
            busi_2 = temp[j]['business_id']
            x1 = temp[i]['latitude']
            y1 = temp[i]['longitude']
            x2 = temp[j]['latitude']
            y2 = temp[j]['longitude']
            first = (x1, y1)
            second = (x2, y2)
            if busi_1 < busi_2:
                small = busi_1
                large = busi_2
            else:
                small = busi_2
                large = busi_1
            tup = (small, large)
            pair_d[tup] = vincenty(first, second).miles
    with open("dicts/pair_dist.p", "wb") as f:
        pickle.dump(temp, f)


user()
store()
# meta()
# reviews()
# pair_dist()
