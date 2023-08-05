# univariate linear regression:

class  LinearRegressor:
    def __init__(self, x, y):
        # Y = b1*X + b0 is the hypothesis space.
        print(len(x), len(y))
        if len(x) ^ len(y):
            print("inside")
            raise ValueError("Number of target and features should match")
        self.x = x
        self.y = y
        self.m = len(x)  # m is the number of rows in dataset.
        self.b1 = self.b0 = None
        self.func = lambda x: self.b1*x + self.b0

    def cov(self, x, y):
        # covariance.
        assert not len(x) ^ len(y), "return expected same sized vectors"
        mean = lambda lst: sum(lst)/len(lst)
        mx, my = mean(x), mean(y)
        return sum((xi-mx)*(yi-my) for xi, yi in zip(x, y)) / (len(x)-1)
        
    def fit(self):
        x, y = self.x, self.y
        b1, b0 = self.b0, self.b1
        m = self.m
        self.b1 = self.cov(x, y) / self.cov(x, x)
        self.b0 = ( sum(y) - self.b1 * sum(x) ) / m
    
    def predict(self, x):
        if self.b1 is None:
            raise ValueError("Parameters not defined. Fit the model first.")
        if isinstance(x, list) or isinstance(x, tuple):
            return [self.predict(xi) for xi in x]
        try:
            return self.func(x)
        except TypeError as e:
            raise TypeError(e)

if __name__ == "__main__":
    dataset = {
        "feature": [1, 2, 3, 4, 5, 6],
        "target": [2, 4, 6, 8, 10, 12]
    }
    model = LinearRegressor(dataset['feature'], dataset['target'])
    model.fit()
    print(model.predict([1, 2, 3, 4]))

