# Load the library with the iris dataset
from sklearn.datasets import load_iris

# Load scikit's random forest classifier library
from sklearn.ensemble import RandomForestClassifier

# Load pandas
import pandas as pd

# Load numpy
import numpy as np



def main():
    my_data = np.genfromtxt('Database.csv', delimiter=',', dtype=None)
    # Create a dataframe with the four feature variables
    df = pd.DataFrame(my_data[1:], columns=my_data[0])
    df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75

    train, test = df[df['is_train'] == True], df[df['is_train'] == False]

    # Show the number of observations for the test and training dataframes
    print('Number of observations in the training data:', len(train))
    print('Number of observations in the test data:', len(test))

    # Create a list of the feature column's names
    features = df.columns[1:]

    print features

    # train['species'] contains the actual species names. Before we can use it,
    # we need to convert each species name into a digit. So, in this case there
    # are three species, which have been coded as 0, 1, or 2.
    y = train['TL']

    print y

    # Create a random forest classifier. By convention, clf means 'classifier'
    clf = RandomForestClassifier(n_jobs=2)

    # Train the classifier to take the training features and learn how they relate
    # to the training y (the species)
    print clf.fit(train[features], y)

    # Apply the classifier we trained to the test data (which, remember, it has never seen before)
    print clf.predict(test[features])

    # View the predicted probabilities of the first 10 observations
    print clf.predict_proba(test[features])[0:10]

    preds = clf.predict(test[features])
    # View the PREDICTED species for the first five observations
    print preds[0:5]
    # View the ACTUAL species for the first five observations
    print test['TL'].head()

    # Create confusion matrix
    print pd.crosstab(test['TL'], preds, rownames=['Actual TL'], colnames=['Predicted TL'])

    # View a list of the features and their importance scores
    print list(zip(train[features], clf.feature_importances_))

    pass

if __name__ == "__main__":
    main()
