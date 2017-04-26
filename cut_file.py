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
