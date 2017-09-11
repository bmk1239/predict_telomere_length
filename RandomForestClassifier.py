
import matplotlib.pyplot as plt
from collections import OrderedDict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import csv



def main():
    my_data = np.genfromtxt('Database_all.csv', delimiter=',', dtype=None)
    print "Create a dataframe with the feature variables"
    df = pd.DataFrame(my_data[1:], columns=my_data[0])
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .80

    train, test = df[df['is_train'] == True], df[df['is_train'] == False]

    print('Number of observations in the training data:', len(train))
    print('Number of observations in the test data:', len(test))

    features = df.columns[1:]

    print features

    y = train['TL']

    print y

    print "Create a random forest classifier. By convention, clf means 'classifier'"
    clf = RandomForestClassifier(n_jobs=2)

    #
    # RANDOM_STATE = 123
    #
    # # NOTE: Setting the `warm_start` construction parameter to `True` disables
    # # support for parallelized ensembles but is necessary for tracking the OOB
    # # error trajectory during training.
    # ensemble_clfs = [
    #     ("RandomForestClassifier, max_features='sqrt'",
    #      RandomForestClassifier(warm_start=True, oob_score=True,
    #                             max_features="sqrt",
    #                             random_state=RANDOM_STATE)),
    #     ("RandomForestClassifier, max_features='log2'",
    #      RandomForestClassifier(warm_start=True, max_features='log2',
    #                             oob_score=True,
    #                             random_state=RANDOM_STATE)),
    #     ("RandomForestClassifier, max_features=None",
    #      RandomForestClassifier(warm_start=True, max_features=None,
    #                             oob_score=True,
    #                             random_state=RANDOM_STATE))
    # ]
    #
    # # Map a classifier name to a list of (<n_estimators>, <error rate>) pairs.
    # error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)
    #
    #
    # # Range of `n_estimators` values to explore.
    # min_estimators = 15
    # max_estimators = 175
    #
    # for label, clf1 in ensemble_clfs:
    #     for i in range(min_estimators, max_estimators + 1):
    #         clf1.set_params(n_estimators=i)
    #         clf1.fit(train[features], y)
    #
    #         # Record the OOB error for each `n_estimators=i` setting.
    #         oob_error = 1 - clf1.oob_score_
    #         error_rate[label].append((i, oob_error))
    #
    # # Generate the "OOB error rate" vs. "n_estimators" plot.
    # for label, clf_err in error_rate.items():
    #     xs, ys = zip(*clf_err)
    #     plt.plot(xs, ys, label=label)
    #
    # plt.xlim(min_estimators, max_estimators)
    # plt.xlabel("n_estimators")
    # plt.ylabel("OOB error rate")
    # plt.legend(loc="upper right")
    # plt.show()
    #

    print "Train the classifier to take the training features and learn how they relate to the training y (the species)"
    clf.fit(train[features], y)

    print "Apply the classifier we trained to the test data (which, remember, it has never seen before)"
    clf.predict(test[features])
    pred_probs = clf.predict_proba(test[features])
    print "predicted probabilities:"
    print pred_probs
    preds = clf.predict(test[features])
    conf_mat = pd.crosstab(test['TL'], preds, rownames=['Actual TL'], colnames=['Predicted TL'])
    print "confusion matrix:"
    print conf_mat
    # conf_mat.to_csv("result_confusion_matrix.csv")
    compareVals = list(zip(test['TL'], preds))
    with open("compareFile.csv", "wb") as f:
        writer = csv.DictWriter(f, fieldnames=['Actual TL', 'Predicted TL'])
        writer.writeheader()
        for (x1,y1) in compareVals:
            writer.writerow({'Actual TL': x1, 'Predicted TL': y1})
    score = list(zip(train[features], clf.feature_importances_))
    zero_score = list();
    non_zero_score = list();
    for (x1,y1) in score:
        if float(y1) != 0.0:
            non_zero_score.append((x1,y1));
        else:
            zero_score.append((x1, y1));
    with open("result_features_scores.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(non_zero_score)
    with open("zero_result_features_scores.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(zero_score)
    print "MSE: ", mean_squared_error(test['TL'], preds)
    pass

if __name__ == "__main__":
    main()
