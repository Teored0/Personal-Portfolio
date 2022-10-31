import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

train_filepath = "./data/train.csv"
test_filepath = "./data/test.csv"

if __name__ == '__main__':
    train = pd.read_csv(train_filepath, delimiter=',')
    test = pd.read_csv(test_filepath, delimiter=',')

    for df in [train, test]:
        df.drop("Name", axis=1, inplace=True)  # Drop column Name
        df.drop("Cabin", axis=1, inplace=True)  # Drop Cabin, few rows -> important column
        df.drop("Ticket", axis=1, inplace=True)

        # one hot encoding on Sex
        df["male"] = (df["Sex"] == "male") * 1
        df["female"] = (df["Sex"] == "female") * 1
        df.drop("Sex", axis=1, inplace=True)

        # drop rows where there are a few na values
        na_indexes = df[df['Embarked'].isnull()].index.tolist()
        df.drop(na_indexes, axis=0, inplace=True)

        df["Fare"].fillna(df["Fare"].median(), inplace=True)

        # replace na ages with the median ages
        df["Age"].fillna(df["Age"].median(), inplace=True)

        for item in np.unique(df["Embarked"]):
            df[item] = (df["Embarked"] == item) * 1
        df.drop("Embarked", axis=1, inplace=True)

        submission = pd.DataFrame({
            "Passenger_Id": df.pop("PassengerId")
        })

    # print("*" * 20 + " Train Info " + "*" * 20)
    # print(train)
    # print(train.info())
    # print("*" * 20 + " Test Info " + "*" * 20)
    # print(test)
    # print(test.info())

    # define x_train, x_test and y_train
    y_train = train.pop("Survived").to_numpy()
    x_train = train.to_numpy()
    x_test = test.to_numpy()

    # defining models
    models = [KNeighborsClassifier(n_neighbors=7),
              SVC(kernel='rbf', gamma=10, C=1),
              RandomForestClassifier(criterion="gini", n_estimators=1000),
              DecisionTreeClassifier(criterion="gini"),
              LogisticRegression()]

    accuracies = {"KNeighborsClassifier(n_neighbors=7)": [],
                  "SVC(C=1, gamma=10)": [],
                  "RandomForestClassifier(n_estimators=1000)": [],
                  "DecisionTreeClassifier()": [],
                  "LogisticRegression()": []}
    ones = {"KNeighborsClassifier(n_neighbors=7)": [],
            "SVC(C=1, gamma=10)": [],
            "RandomForestClassifier(n_estimators=1000)": [],
            "DecisionTreeClassifier()": [],
            "LogisticRegression()": []}

    # scaling with MinMax Scaler
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(X=train)
    x_test = scaler.fit_transform(X=test)

    kf = KFold(n_splits=10)

    # K-fold cross validation for find the best model, use only train and split it in train and test every time
    for train_index, test_index in kf.split(x_train):
        # print("TRAIN:", train_index, "TEST:", test_index)
        xx_train, xx_test = x_train[train_index], x_train[test_index]
        yy_train, yy_test = y_train[train_index], y_train[test_index]
        # print(f"Train percentage of 1's: {(np.count_nonzero(yy_test) / len(yy_test)) * 100:.2f} %")
        # print(yy_test)

        for clf in models:
            clf.fit(xx_train, yy_train)
            # scores = cross_val_score(clf, X=xx_train, y=yy_train, cv=10)
            yy_pred = clf.predict(xx_test)
            score = round(clf.score(xx_test, yy_test) * 100, 2)
            accuracies[str(clf)].append(np.mean(yy_test == yy_pred))
            ones[str(clf)].append((np.count_nonzero(yy_pred) / len(x_test)))
            # print(scores)
            # print(f"{clf} Cross Validation Score: {np.mean(scores) * 100:.2f} %")
            # print(f"{clf} Score: {score}")
            # print(f"{clf} y pred: {y_pred}")
            # print(f"{clf} Accuracy: {np.mean(yy_test == yy_pred) * 100:.2f} %")
            # print(f"{clf} Test percentage of 1's: {(np.count_nonzero(yy_pred) / len(x_test)) * 100:.2f} %")
            # print(yy_pred)

        # print("*" * 100)

    final_accuracy = {}
    for model_accuracy in accuracies:
        # final_accuracy[model_accuracy] = np.mean(accuracies[model_accuracy])
        print(f"{model_accuracy} Final Accuracy: {np.mean(accuracies[model_accuracy]) * 100:.2f} %")
        print(f"{model_accuracy} Final Ones Rate: {np.mean(ones[model_accuracy]) * 100:.2f} %")

    print(f"Train percentage of 1's: {(np.count_nonzero(y_train) / len(y_train)) * 100:.2f} %")

    clf = RandomForestClassifier(criterion="entropy", n_estimators=1000)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    score = round(clf.score(x_train, y_train) * 100, 2)
    print(y_pred)
    print(f"{clf} Score: {score}")
    print(f"{clf} Test percentage of 1's: {(np.count_nonzero(y_pred) / len(x_test)) * 100:.2f} %")

    submission["Survived"] = y_pred
    submission.to_csv('./Output/submission.csv', index=False)
