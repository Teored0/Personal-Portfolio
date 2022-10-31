import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split


class BabyKMeans:
    def __init__(self, n_clusters: int, max_iterations: int = 30):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations

    def manhattan_distance(self, ar_1: np.array, ar_2: np.array) -> float:
        """
        Manhattan Distance between two arrays
        :param ar_1: np.array
        :param ar_2: np.array
        :return: float
        """

        if len(ar_1) == len(ar_2):
            dist = abs(ar_1 - ar_2)
            dist = np.sum(dist)
        else:
            raise Exception("Arrays haven't the same dimension")
        return dist

    def find_cluster(self, ar: np.ndarray, points: np.ndarray) -> np.ndarray:
        """
        Get the cluster from manhattan distance
        :param ar: np.ndarray
        :param points: np.ndarray
        :return: np.ndarray
        """
        clusters = []
        for i in range(ar.shape[0]):
            distances = []
            for j in range(self.n_clusters):
                distances.append(abs(ar[i][0] - points[j][0]) + abs(ar[i][1] - points[j][1]))
            clusters.append(np.argmin(distances))
        return np.asarray(clusters)

    def random_centroids(self, x: np.ndarray) -> np.ndarray:
        """
        Define a random centroid
        :param x: np.ndarray
        :return: np.ndarray
        """
        random_idx = [np.random.randint(len(x)) for i in range(self.n_clusters)]
        centroids = [x[i] for i in random_idx]
        return np.asarray(centroids)

    def update_centroids(self, x: np.ndarray, clusters: np.ndarray) -> np.ndarray:
        """
        Update the centroid with the mean of all the distance of a cluster
        :param x: np.ndarray
        :param clusters: np.ndarray
        :return: np.ndarray
        """
        centroids = []
        for i in range(self.n_clusters):
            temp = [x[j] for j in range(x.shape[0]) if clusters[j] == i]
            centroids.append(np.mean(temp, axis=0))
        return np.asarray(centroids)

    def fit(self, x: np.ndarray) -> np.ndarray:
        """
        Iterate and update the centroids until are the same for 2 iterations
        :param x: np.ndarray
        :return: np.ndarray, np.ndarray
        """
        centroids_history, n_centroids = [], []
        r_centroids = self.random_centroids(x)
        clusters = self.find_cluster(ar=x, points=r_centroids)
        centroids_history.append(r_centroids)
        for i in range(self.max_iterations):
            n_centroids = self.update_centroids(x=x, clusters=clusters)
            clusters = self.find_cluster(ar=x, points=n_centroids)
            centroids_history.append(n_centroids)
            dist = self.manhattan_distance(centroids_history[len(centroids_history) - 2],
                                           centroids_history[len(centroids_history) - 1])
            if dist == 0:
                break

        return n_centroids, clusters


if __name__ == '__main__':
    x, y = make_moons(n_samples=200)

    for i in range(30):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
        k = 2
        clf = BabyKMeans(k)
        centroids, clusters = clf.fit(x=x)

    plt.scatter(x[:, 0], x[:, 1], c=clusters)
    for n in range(k):
        plt.scatter(centroids[n][0], centroids[n][1], c="r")

    plt.show()
