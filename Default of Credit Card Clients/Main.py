import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
import keras
from keras.layers import Dense

path = "./data/default of credit card clients.csv"

if __name__ == '__main__':
    df = pd.read_csv(path, delimiter=';')

    # ******************** Preprocessing ********************
    # Drop the ID column
    df.drop("ID", axis=1, inplace=True)

    # One hot encoding on the Sex, Education, Married columns
    df["MALE"] = (df["SEX"] == 1) * 1
    df["FEMALE"] = (df["SEX"] == 2) * 1
    df.drop("SEX", axis=1, inplace=True)

    df["GRADUATE_SCHOOL"] = (df["EDUCATION"] == 1) * 1
    df["UNIVERSITY"] = (df["EDUCATION"] == 2) * 1
    df["HIGH_SCHOOL"] = (df["EDUCATION"] == 3) * 1
    df["EDU_OTHERS"] = (df["EDUCATION"] == 4) * 1
    df.drop("EDUCATION", axis=1, inplace=True)

    df["MARRIED"] = (df["MARRIAGE"] == 1) * 1
    df["SINGLE"] = (df["MARRIAGE"] == 2) * 1
    df["MAR_OTHERS"] = (df["MARRIAGE"] == 3) * 1
    df.drop("MARRIAGE", axis=1, inplace=True)

    # one hot encoding on all the Pay columns
    pay = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']

    for item in pay:
        for i in range(df[item].min(), df[item].max() + 1):
            df[item + "_" + str(i)] = (df[item] == i) * 1
        df.drop(item, axis=1, inplace=True)

    # Extract the label column and convert to Numpy array
    y = df.pop('default payment next month')
    y = y.to_numpy()

    # Convert the Dataframe to Numpy 2-D array
    dataset = df.to_numpy()
    x = dataset[:, :-1]

    final_accuracies = {"SVM Classifier": [], "Random Forest Classifier": [], "Neural Network": [], "KNN": []}

    # Repeated K-fold
    for repetitions in range(10):
        # Split the dataset as 70% train and 30% test
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
        K = 5
        L = x_train.shape[0] // K
        indexes = np.arange(x_train.shape[0])
        accuracies = {"SVM Classifier": [], "Random Forest Classifier": [], "Neural Network": [], "KNN": []}

        # K-fold
        for i in range(K):
            test_mask = indexes[i * L: (i + 1) * L]
            xx_test, yy_test = x_train[test_mask], y_train[test_mask]
            xx_train, yy_train = x_train[~test_mask], y_train[~test_mask]

            # ******************** SVM ********************

            classifier = SVC(kernel='rbf', C=100, gamma=1000)

            classifier.fit(xx_train, yy_train)
            y_pred = classifier.predict(xx_test)
            accuracy = np.mean(yy_test == y_pred)
            accuracies["SVM Classifier"].append(accuracy)

            # ******************** Random Forest ********************

            clf = sklearn.ensemble.RandomForestClassifier(criterion="entropy", n_estimators=1000)
            clf.fit(xx_train, yy_train)
            y_pred = clf.predict(xx_test)
            accuracy = np.mean(yy_test == y_pred)
            accuracies["Random Forest Classifier"].append(accuracy)

            # ******************** Neural Network ********************
            # label's one hot encoding
            yy_train_en = np.zeros((yy_train.shape[0], 2))
            yy_train_en[:, 0] = yy_train == 0
            yy_train_en[:, 1] = yy_train == 1

            yy_test_en = np.zeros((yy_test.shape[0], 2))
            yy_test_en[:, 0] = yy_test == 0
            yy_test_en[:, 1] = yy_test == 1

            scaler = MinMaxScaler()
            xx_train = scaler.fit_transform(X=xx_train)
            xx_test = scaler.fit_transform(X=xx_test)

            N = 150
            model = keras.Sequential(
                layers=[Dense(units=N, activation='relu', input_dim=x_train.shape[1]),
                        Dense(units=N, activation='relu'),
                        Dense(units=N, activation='relu'),
                        Dense(units=N, activation='relu'),
                        Dense(units=2, activation='softmax')])

            model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
            model.fit(xx_train, yy_train_en, batch_size=16, epochs=30, verbose=0)

            y_pred = model.predict(xx_test)
            y_pred = np.argmax(y_pred, axis=1)
            yy_test_en = np.argmax(yy_test_en, axis=1)

            accuracy = np.mean(yy_test_en == y_pred)
            accuracies["Neural Network"].append(accuracy)
            # ****************** KNN ************************
            clf = sklearn.neighbors.KNeighborsClassifier(n_neighbors=5)
            clf.fit(xx_train, yy_train)
            y_pred = clf.predict(xx_test)
            accuracy = np.mean(yy_test == y_pred)
            accuracies["KNN"].append(accuracy)

        for k in accuracies.keys():
            final_accuracies[k].append(np.mean(accuracies[k]))

    for item in final_accuracies.keys():
        print(f"{item} Accuracy: {np.mean(final_accuracies[item]) * 100:.2f}%")
