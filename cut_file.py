<<<<<<< Updated upstream
import utils
import random


def cut_file():
    store = utils.load("dicts/store.p")
    biz_ids = store.keys()
    N = len(biz_ids)
    random.shuffle(biz_ids)

    train_ids = biz_ids[:int(N*0.8)]
    test_ids = biz_ids[int(N*0.8):]

    utils.dump(train_ids, "data_id/train.p")
    utils.dump(test_ids, "data_id/test.p")


if __name__ == "__main__":
    cut_file()
=======
import pickle
import random
import json

def cut_file():
    biz_ids = []
    with open("dataset/yelp_academic_dataset_business.json", "r") as f:
        for line in f:
            line = json.loads(line)
            biz_ids.append(line["business_id"])
    N = len(biz_ids)
    random.shuffle(biz_ids)

    train_ids = biz_ids[:int(N*0.8)]
    valid_ids = biz_ids[int(N*0.8):]

    with open("data_id/train.p", "wb") as f:
        pickle.dump(train_ids, f)
    with open("data_id/valid.p", "wb") as f:
        pickle.dump(valid_ids, f)



cut_file()

>>>>>>> Stashed changes
