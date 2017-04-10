import pickle

def cv(K):
    # K-FOLD CROSS-VALIDATION
    with open("data/train_f.p", "r") as f:
        data = pickle.load(f)
    N = len(data)
    for k in range(K):
        train = []
        test = []
        for i in range(N):
            if i%K == k:
                test.append(data[i])
            else:
                train.append(data[i])
        with open("data/train_" + str(k+1) + ".p", "w") as f:
            pickle.dump(train, f)
        with open("data/test_" + str(k+1) + ".p", "w") as f:
            pickle.dump(test, f)
