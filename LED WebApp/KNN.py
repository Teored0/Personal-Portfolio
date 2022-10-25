import datetime
from statistics import mode

class KNN:  # K nearest neighbours
    def __init__(self, k: int):

        if not isinstance(k, int):
            raise TypeError("k in not an integer")
        if not (k > 0 and k % 2):
            raise ValueError("k is not positive and odd")

        self.k = k
        self.x_train = None
        self.y_train = None
        self.buttons = {"red": 0, "yellow": 1, "blue": 2}

    def clean(self, data):
        x = []
        y = []
        for row in data:
            for col in row.values():
                if type(col) == datetime.datetime:
                    x.append(int(col.timestamp()))
                else:
                    for bt in self.buttons:
                        if bt == col:
                            y.append(self.buttons[bt])
        return x, y

    def fit(self, x_train: list, y_train: list) -> None:
        self.x_train = x_train
        self.y_train = y_train

    def predict(self) -> list:
        x_test = int(datetime.datetime.now().timestamp())
        distances = []
        for sample in self.x_train:
            distances.append(self.__manhattan_distance(x_test, sample))

        nearest_neighbors = sorted(distances)
        y_sort = [y_sorted for _, y_sorted in sorted(zip(distances, self.y_train))]
        classes = y_sort[:self.k]
        return mode(classes)

    def __manhattan_distance(self, ar_1, ar_2):
        return abs(ar_1 - ar_2)
