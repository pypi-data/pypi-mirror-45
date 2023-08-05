from itertools import product
import math


class Feature:
    def __init__(self, data):
        self.data = data
        self.n = len(self.data)
    def __sub__(self, other):
        return math.sqrt(sum((x1-x2)**2 for x1, x2 in zip(self.data, other.data)))
    def __repr__(self):
        return str(self.data)


class Cluster:
    def __init__(self, features=None):
        if features is None:
            self.features = []
        else:
            self.features = features
    def extract_min_dist(self, feature):
        return min(feat_i-feature for feat_i in self.features)
    def add(self, feat):
        if not isinstance(feat, Feature):
            self.features.append(Feature(feat))
        else:
            self.features.append(feat)
    def merge_cluster(self, cluster):
        return Cluster(cluster.features + self.features)
    def __repr__(self):
        return str(self.features)



class Agglomerative:
    def __init__(self, dataset):
        self.dataset = dataset
        self.level_cluster = {}

    def get_dist_matrix(self, clusters):
        matrix = {}
        for c_i, c_j in product(clusters, clusters):
            if c_i == c_j: continue
            matrix[(c_i, c_j)] = min([c_i.extract_min_dist(feat) for feat in c_j.features])
        return matrix
    def remove_from_cluster(self, clusters, del_cluster):
        clusters.pop(clusters.index(del_cluster))
        return clusters

    def build(self):
        clusters = [Cluster([Feature(pt)]) for pt in dataset]
        self.level_cluster[len(clusters)] = clusters.copy()
        while len(clusters) > 1:
            self.level_cluster[len(clusters)-1] = clusters
            dist_matrix = self.get_dist_matrix(clusters)
            c1, c2 = min(dist_matrix.items(), key=lambda x: x[1])[0]
            clusters = self.remove_from_cluster(clusters, c1)
            clusters = self.remove_from_cluster(clusters, c2)
            clusters.append(c2.merge_cluster(c1))
            clusters = clusters.copy()


class KMeans(Agglomerative):
    def __init__(self, dataset, k):
        super().__init__(dataset)
        self.k = k
        self.build()

    def get_clusters(self):
        return self.level_cluster[self.k]


if __name__ == "__main__":
    dataset = [(x, x) for x in [0, 1, 2, 5, 6, 7]]
    kmeans = Agglomerative(dataset)
    kmeans = KMeans(dataset, k=2)
    print(kmeans.get_clusters())
