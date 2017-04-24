import pickle
import random


def cut_file():
    with open("dicts/store.p", "r") as f:
        store = pickle.load(f)
    biz_ids = store.keys()
    N = len(biz_ids)
    random.shuffle(biz_ids)

    train_ids = biz_ids[:int(N*0.8)]
    valid_ids = biz_ids[int(N*0.8):]

    with open("data_id/train.p", "wb") as f:
        pickle.dump(train_ids, f)
    with open("data_id/valid.p", "wb") as f:
        pickle.dump(valid_ids, f)


if __name__ == "__main__":
    cut_file()
