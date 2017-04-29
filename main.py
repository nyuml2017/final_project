<<<<<<< Updated upstream
import numpy as np
from cv import *
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix

import utils
import model  # model_list, params_list


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
        with open("data/train_" + str(k) + ".p", "r") as f:
            tr_features, tr_ans = pickle.load(f)
        with open("data/test_" + str(k) + ".p", "r") as f:
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
    with open("data/train_f.p", "r") as f:
        tr_features, tr_ans = pickle.load(f)
    with open("data/valid_f.p", "r") as f:
        valid_features, valid_ans = pickle.load(f)
    clf = svm.SVR()
    clf.fit(tr_features, tr_ans)

    tr_predict = clf.predict(tr_features)
    valid_predict = clf.predict(valid_features)

    # Validation
    print "Training Error:", np.power(tr_predict - tr_ans,2).sum()
    print "Validation Error:", np.power(valid_predict - valid_ans,2).sum()


def grid_search(X, Y, m, cs, K=5):
    clf = GridSearchCV(m, cs, cv=K)
    clf.fit(X,Y)
    print (clf.cv_results_)
    return clf.cv_results_['mean_test_score']


def main_sklearn():
    # 0. Parameter settings
    K = 5

    print "Start training models with', K, '-fold cross validation..."

    # 1. Load training data
    X_train, Y_train = utils.load("data/train_f.p")

    # 2. Grid search for best params and model
    scores = {}
    for m in model_list:
        print ('run', m)
        scores[m] = grid_search(X_train, Y_train, model_list[m], params_list[m], K)

    print (scores)
    max_score = 0
    for model_name, score in scores.items():
        if np.max(score) > max_score:
            max_score = np.max(score)
            param_key = list(params_list[model_name])[0]
            optimal_params = { param_key: params_list[model_name][param_key][np.argmax(score)]}
            optimal_model = model_list[model_name]

    # 3. Build Model (with whole data)
    optimal_model.set_params(**optimal_params)
    optimal_model.fit(X_train, Y_train)

    # 4. Load test data
    X_test, Y_test = utils.load("data/test_f.p")

    # 5. Evaluation
    Y_pred = optimal_model.predict(X_test)
    print scores
    print (confusion_matrix(Y_test, Y_pred))


if __name__ == "__main__":
    main_sklearn()
=======
import numpy as np
from cv import *
from sklearn import svm, model_selection

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
        with open("data/train_" + str(k) + ".p", "r") as f:
            tr_features, tr_ans = pickle.load(f)
        with open("data/test_" + str(k) + ".p", "r") as f:
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
    with open("data/train_f.p", "r") as f:
        tr_features, tr_ans = pickle.load(f)
    with open("data/valid_f.p", "r") as f:
        valid_features, valid_ans = pickle.load(f)
    clf = svm.SVR()
    clf.fit(tr_features, tr_ans)

    tr_predict = clf.predict(tr_features)
    valid_predict = clf.predict(valid_features)

    # Validation
    print "Training Error:", np.power(tr_predict - tr_ans,2).sum()
    print "Validation Error:", np.power(valid_predict - valid_ans,2).sum()

def main_sklearn():
    # Parameter settings
    K = 5

    print "Start training models with', K, '-fold cross validation..."

    with open("data/train_f.p", "r") as f:
        tr_features, tr_ans = pickle.load(f)

    clf = svm.SVR()
    scores = model_selection.cross_val_score(clf, tr_features, tr_ans, cv=K)

    # Score in MSE
    print scores
    print "Testing Error:", np.sum(scores)/len(scores)

    # Build Model (with whole data)
    with open("data/valid_f.p", "r") as f:
        valid_features, valid_ans = pickle.load(f)

    clf.fit(tr_features, tr_ans)
    # Validation
    print "Training Error:", clf.score(tr_features, tr_ans)
    print "Validation Error:", clf.score(valid_features, valid_ans)

if __name__ == "__main__":
    main_sklearn()
>>>>>>> Stashed changes
