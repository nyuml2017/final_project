from sklearn.ensemble import RandomForestClassifier  # RF
from sklearn.svm import SVC, LinearSVC, NuSVC        # SVM
from sklearn import linear_model                     # LR


model_list = {
    "Linear-SVM": LinearSVC(penalty='l2', dual=False, multi_class='ovr', class_weight='balanced'),
    "RBF-SVM": SVC(kernel='rbf', decision_function_shape='ovr'),
    "RandomForest": RandomForestClassifier(),
}

params_list = {
    "Linear-SVM": {'C': [10**i for i in range(-5,5)]},
    "RBF-SVM": {'C': [10**i for i in range(-5,5)]},
    "RandomForest":  {'max_depth': range(15,20)},
}
