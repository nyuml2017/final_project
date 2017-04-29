<<<<<<< Updated upstream
import utils
import json
import time
from datetime import datetime
# from textblob import TextBlob
# from geopy.distance import vincenty


def store(observe_t=12, target_t=6):

    thresh_t = observe_t + target_t

    all_store = {}
    store = {}

    # 1. Get start_t/end_t for each store
    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            date = datetime.strptime(line["date"], "%Y-%m-%d")
            if business_id not in all_store:
                all_store[business_id] = {}
                all_store[business_id]["start_t"] = date
                all_store[business_id]["end_t"] = date
            else:
                if date > all_store[business_id]["end_t"]:
                    all_store[business_id]["end_t"] = date
                if date < all_store[business_id]["start_t"]:
                    all_store[business_id]["start_t"] = date

    # 2. Filter store with store_age < (observe_t + target_t)
    for business_id in all_store:
        store_age = int((all_store[business_id]["end_t"] - all_store[business_id]["start_t"]).days/30)
        if store_age < thresh_t:
            continue
        store[business_id] = {}
        store[business_id]["start_t"] = all_store[business_id]["start_t"]
        store[business_id]["end_t"] = all_store[business_id]["end_t"]
        store[business_id]["stars"] = 0
        store[business_id]["review_cnt"] = 0

    # 3. Get sum of stars and review_cnt for each store
    user = utils.load("dicts/user.p") # load user dict to compute stars

    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            if business_id not in store:
                continue
            user_id = line["user_id"]
            date = datetime.strptime(line["date"], "%Y-%m-%d")
            if int((date-store[business_id]["start_t"]).days/30) <= observe_t:
                store[business_id]["review_cnt"] += 1
                store[business_id]["stars"] += (line["stars"]-user[user_id]["avg_stars"])

    # 4. Complete information for each store
    with open("dataset/yelp_academic_dataset_business.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            if business_id not in store:
                continue
            store[business_id]["name"] = line["name"]
            store[business_id]["city"] = line["city"]
            store[business_id]["state"] = line["state"]
            store[business_id]["latitude"] = line["latitude"]
            store[business_id]["longitude"] = line["longitude"]
            store[business_id]["stars"] /= store[business_id]["review_cnt"]
            store[business_id]["is_open"] = line["is_open"]
            store[business_id]["categories"] = line["categories"]

    utils.dump(store, "dicts/store.p")
    print (len(store))


def store_pair():
    store_pair = {}

    store = utils.load("dicts/store.p")

    ob_max = 0
    ob_min = 999999
    i = 0
    d = 1
    for business_id_1 in store:
        # t1 = time.time()
        i += 1
        store_pair[business_id_1] = []
        for business_id_2 in store:
            if business_id_2 == business_id_1:
                continue
            if store[business_id_1]["city"] != store[business_id_2]["city"]:
                continue
            if store[business_id_2]["start_t"] < store[business_id_1]["end_t"] and store[business_id_2]["end_t"] > store[business_id_1]["start_t"]:
                store_pair[business_id_1].append(business_id_2)
        # t2 = time.time()
        # print (t2-t1)
        # len_pair = len(store_pair[business_id_1])
        # print len_pair
        # if len_pair < ob_min:
        #     ob_min = len_pair
        # if len_pair > ob_max:
        #     ob_max = len_pair
        if i%10000 == 0:
            path = "dicts/store_pair_" + str(d) + ".p"
            utils.dump(store_pair, path)
            store_pair = {}
            d += 1
            i = 0
    path = "dicts/store_pair" + str(d) + ".p"
    utils.dump(store_pair, path)
    # print (ob_min)
    # print (ob_max)


def store_user_review(observe_t=12):
    store_user = {}
    store_review = {}

    store = utils.load("dicts/store.p")

    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            if business_id not in store:
                continue
            review_id = line["review_id"]
            user_id = line["user_id"]
            date = datetime.strptime(line["date"], "%Y-%m-%d")
            if int((date-store[business_id]["start_t"]).days/30) <= observe_t:
                if business_id in store_review:
                    store_review[business_id].append(review_id)
                else:
                    store_review[business_id] = [review_id]
                if business_id in store_user:
                    store_user[business_id].append(user_id)
                else:
                    store_user[business_id] = [user_id]

    utils.dump(store_user, "dicts/store_user.p")
    utils.dump(store_review, "dicts/store_review.p")

# Filter reviews using curr_time
# def store_review():
#     with open("dicts/store.p", "r") as f:
#         store = pickle.load(f)
#     store_review = {}
#     with open("dataset/yelp_academic_dataset_review.json", "r") as f:
#         for line in f:
#             line = json.loads(line)
#             business_id = line["business_id"]
#             review_id = line["review_id"]
#             date = datetime.strptime(line["date"], "%Y-%m-%d")
#             if date <= curr_time:
#                 if business_id in store_review:
#                     store_review[business_id].append(review_id)
#                 else:
#                     store_review[business_id] = [review_id]
#     with open("dicts/store_review.p", "wb") as f:
#         pickle.dump(store_review, f)


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

    utils.dump(meta, "dicts/meta.p")


def reviews():
    reviews = {}
    i = 0
    d = 1
    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            i += 1
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

            if i%10000 == 0:
                path = "dicts/reviews_" + str(d) + ".p"
                utils.dump(reviews, path)
                reviews = {}
                d += 1
                i = 0
    path = "dicts/reviews_" + str(d) + ".p"
    utils.dump(reviews, path)


def user():
    user = {}
    with open("dataset/yelp_academic_dataset_user.json", "r") as f:
        for line in f:
            line = json.loads(line)
            user_id = line['user_id']
            user[user_id] = {}
            # user[user_id]['review_cnt'] = line['review_count']
            user[user_id]['yelp_since'] = line['yelping_since']
            # user[user_id]['friends_cnt'] = len(line['friends'])
            # user[user_id]['fans'] = line['fans']
            # user[user_id]['elite_year_cnt'] = len(line['elite'])
            user[user_id]['elite'] = line['elite']
            user[user_id]['avg_stars'] = line['average_stars']
    utils.dump(user, "dicts/user.p")


def pair_dist():
    temp = []
    with open("dataset/yelp_academic_dataset_business.json", "r") as f:
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
    utils.dump(tmp, "dicts/pair_dist.p")


if __name__ == "__main__":
    # user()
    # store()
    store_pair()
    # store_user_review()
    # store_review()
    # meta()
    # reviews()
    # pair_dist()

=======
import pickle
import json
from datetime import datetime
from textblob import TextBlob
from geopy.distance import vincenty

curr_time = datetime(2014, 06, 01)

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

def store_review():
    with open("dicts/store.p", "r") as f:
        store = pickle.load(f)
    store_review = {}
    with open("dataset/yelp_academic_dataset_review.json", "r") as f:
        for line in f:
            line = json.loads(line)
            business_id = line["business_id"]
            review_id = line["review_id"]
            date = datetime.strptime(line["date"], "%Y-%m-%d")
            if date <= curr_time:
                if business_id in store_review:
                    store_review[business_id].append(review_id)
                else:
                    store_review[business_id] = [review_id]

    with open("dicts/store_review.p", "wb") as f:
        pickle.dump(store_review, f)

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
            i += 1
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

            if i%10000 == 0:
                filename = "dicts/reviews_" + str(d) + ".p"
                with open(filename, 'wb') as f:
                    pickle.dump(reviews, f)
                reviews = {}
                d += 1
                i = 0
    filename = "dicts/reviews_" + str(d) + ".p"
    with open(filename, 'wb') as f:
        pickle.dump(reviews, f)


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


# user()
# store()
# store_review()
# meta()
reviews()
# pair_dist()

>>>>>>> Stashed changes
