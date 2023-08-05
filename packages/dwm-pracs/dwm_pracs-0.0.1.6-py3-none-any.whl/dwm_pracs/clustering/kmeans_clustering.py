import math

class KMeans:
    def __init__(self, k=3, max_iter=200):
        self.k = k
        self.max_iter = max_iter
        self.clusters = {}
        self.centroids = {}

    def get_distance(self, p1, p2):
        # https://stackoverflow.com/questions/5228383/how-do-i-find-the-distance-between-two-points
        # dist = math.hypot(x2 - x1, y2 - y1)
        return math.hypot( p2[0] - p1[0], p2[1] - p1[1] )

    def fit(self, data):
        # intializing centroids
        for i in range(self.k):
            self.centroids[i] = data[i]

        for _ in range(self.max_iter):

            # refreshing the dictionary of clusters after each iteration
            for i in range(self.k):
                self.clusters[i] = []
            
            for p in data:
                # calculating the distance between coordinate and the centroid
                # and the adding the minimum one in the cluster
                dist = [self.get_distance(p, self.centroids[c]) for c in self.centroids]
                self.clusters[dist.index(min(dist))].append(p)

            prev_centroids = dict(self.centroids)

            print('Iteration {}: '.format(_+1))
            print('Clusters: ', self.clusters)
            print('Centroids: ', self.centroids)
            print('#'*8)

            for c in self.clusters:
                avg_x = sum( p[0] for p in self.clusters[c] ) / len(self.clusters[c])
                avg_y = sum( p[1] for p in self.clusters[c] ) / len(self.clusters[c])
                self.centroids[c] = (avg_x, avg_y)

            if self.centroids == prev_centroids:
                break

    def predict(self, point):
        dist = [self.get_distance(point, self.centroids[c]) for c in self.centroids]
        print("The point is added in cluster: ", dist.index(min(dist)))


if __name__ == '__main__':
    data = [(1, 1), (2, 1), (4, 3), (5, 4)]
    kmeans = KMeans(k=2)
    kmeans.fit(data)
    kmeans.predict((5, 6))
