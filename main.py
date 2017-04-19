import numpy as np
from cv import *
from sklearn import svm

def main():
    # Parameter settings
    K = 5

    # Initialization
    train_err = 0
    test_err = 0

    print "Start training models with', K, '-fold cross validation..."
    cv(K)
    for k in range(1, K+1):
        print k, "-fold"
        with open("data/train_" + str(k) + ".p", "w") as f:
            tr_features, tr_ans = pickle.load(f)
        with open("data/test_" + str(k) + ".p", "w") as f:
            te_features, te_ans = pickle.load(f)

        # Train
        clf = svm.SVR()
        clf.fit(tr_features, tr_ans)

        # Score in MSE
        tr_predict = clf.predict(tr_features)
        te_predict = clf.predict(te_features)

        train_err += np.power(tr_predict - tr_ans,2).sum()
        test_err += np.power(te_predict - te_ans,2).sum()
    print "Training Error:", train_err/K
    print "Testing Error:", test_err/K

    # Build Model (with whole data)
    with open("data/train_f.p", "w") as f:
        tr_features, tr_ans = pickle.load(f)
    with open("data/valid_f.p", "w") as f:
        valid_features, valid_ans = pickle.load(f)
    clf = svm.SVR()
    clf.fit(tr_features, tr_ans)

    tr_predict = clf.predict(tr_features)
    valid_predict = clf.predict(valid_features)

    # Validation
    print "Training Error:", np.power(tr_predict - tr_ans,2).sum()
    print "Validation Error:", np.power(valid_predict - valid_ans,2).sum()

<<<<<<< HEAD
=======
    # build dicts
    user()
    store()
    pair_dist()
>>>>>>> master

    # meta()
if __name__ == "__main__":
    main()
