
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import csv



def main():
    my_data = np.genfromtxt('Database.csv', delimiter=',', dtype=None)
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

    print "Train the classifier to take the training features and learn how they relate to the training y (the species)"
    clf.fit(train[features], y)

    print "Apply the classifier we trained to the test data (which, remember, it has never seen before)"
    clf.predict(test[features])

    pred_probs = clf.predict_proba(test[features])
    row = []
    for results in pred_probs:
        col = []
        for result in results:
            col.append(float(result))
        row.append(col)

    with open("result_predicted_probabilities.csv", "wb") as file:
        writer = csv.writer(file)
        writer.writerows(row)
    preds = clf.predict(test[features])
    conf_mat = pd.crosstab(test['TL'], preds, rownames=['Actual TL'], colnames=['Predicted TL'])
    conf_mat.to_csv("result_confusion_matrix.csv")
    score = list(zip(train[features], clf.feature_importances_))
    with open("result_features_scores.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(score)
    pass

if __name__ == "__main__":
    main()
