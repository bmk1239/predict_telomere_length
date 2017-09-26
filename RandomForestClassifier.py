import matplotlib.pyplot as plt
from collections import OrderedDict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn import metrics
import pandas as pd
import numpy as np
import csv

def randomForestClassifierFunc(X,Y):
    kf = KFold(n_splits=5)
    total = 0
    size = 0
    for train_indices, test_indices in kf.split(X):
        # Get the dataset; this is the way to access values in a pandas DataFrame
        train_X = X.ix[train_indices, :];
        train_Y = Y[train_indices]
        train_Y = map(int, train_Y.values)
        if (1 not in train_Y) or (0 not in train_Y):
            continue
        test_X = X.ix[test_indices, :];
        test_Y = Y[test_indices]
        test_Y = map(int, test_Y.values)
        # Train the model, and evaluate it
        clf = RandomForestClassifier(n_jobs=2)
        clf.fit(train_X, train_Y)
        predictions = clf.predict_proba(test_X)[:, 1]
        fpr, tpr, _ = metrics.roc_curve(test_Y, predictions, pos_label=1)
        if np.isnan(np.sum(fpr)) or np.isnan(np.sum(tpr)):
            continue
        roc_auc = metrics.auc(fpr, tpr)
        print fpr,tpr
        size += 1
        plt.title('Receiver Operating Characteristic')
        plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([-0.1, 1.2])
        plt.ylim([-0.1, 1.2])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
       # plt.show()
        total += roc_auc
    accuracy = total / size
    print "AUC of {0}: {1}".format("RandomForestClassifier", accuracy)

def main():
    my_data = np.genfromtxt('Database_all.csv', delimiter=',', dtype=None)
    print "Create a dataframe with the feature variables"
    df = pd.DataFrame(my_data[1:], columns=my_data[0])
    X = df.drop('TL', axis=1)
    Z = df[['Age','Gender']]
    Y = df['TL']
    randomForestClassifierFunc(X,Y)
    print "***************** only age and gender ********************"
    randomForestClassifierFunc(Z, Y)
    pass

if __name__ == "__main__":
    main()
