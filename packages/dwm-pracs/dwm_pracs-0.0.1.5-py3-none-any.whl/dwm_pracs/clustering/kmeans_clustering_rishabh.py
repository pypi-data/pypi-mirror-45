class Point(complex): pass


class Kmeans:
    def __init__(self, points, k=2):
        self.points = [Point(*tup) for tup in points]
        self.k = k
        self.clusters = [self.points[i:i+k] for i in range(0, len(points), k)]
        self.cluster()
    def which_cluster(self, pt):
        return self.ctroids.index(min(self.ctroids, key=lambda c:abs(c-pt)))

    def cluster(self):
        new_cluster = []
        while new_cluster != self.clusters:
            self.ctroids = [sum(c)/len(c) if c else 0+0j for c in self.clusters]
            new_cluster = [[] for i in range(self.k)]
            for pt in self.points:
                cluster_idx = self.which_cluster(pt)
                new_cluster[cluster_idx].append(pt)
            self.clusters = new_cluster
    
    def predict(self, pt):
        if not isinstance(pt, Point): pt = Point(*pt)
        idx = self.which_cluster(pt)
        return idx, self.clusters[idx]

if __name__ == "__main__":
    dataset = [(2, 2), (5, 5), (1, 1), (4, 4)]
    obj = Kmeans(dataset)
    pt = (0, 0)
    idx, cluster = obj.predict(pt)
    print("Point {} belongs to cluster {} i.e.".format(pt, idx), cluster)
