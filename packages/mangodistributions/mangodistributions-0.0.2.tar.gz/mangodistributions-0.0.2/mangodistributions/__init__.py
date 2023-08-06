import numpy as np

class Distribution:
    def __init__(self,n):
        self.n = n

    def summarise(self):
        self.min = self.sample.min()
        self.max = self.sample.max()
        self.avg = self.sample.mean()
        self.std = self.sample.std()
        print('min: ' +  str(self.min))
        print('max: ' + str(self.max))
        print('mean: ' + str(self.avg))
        print('std: ' + str(self.std))


class Binomial(Distribution):
    def __init__(self,prob,trials,n):
        Distribution.__init__(self,n)
        self.prob = prob
        self.trials = trials

    def draw(self):
        if (self.prob == None) or (self.prob > 1) or (self.prob < 0) or (self.trials == None) or (self.trials < 0):
            raise Exception('Binomial distribution must have a valid probability, and a non zero number of trials')
        else:
            self.sample = np.random.binomial(n=self.trials, p=self.prob, size=self.n) 
            return self.sample

class Poisson(Distribution):
    def __init__(self,lam,n):
        Distribution.__init__(self,n)
        self.lam = lam

    def draw(self):
        if (self.lam == None) or (self.lam < 0):
            raise Exception('Poission distribution must have a non-zero value of lambda')
        else:
            self.sample = np.random.poisson(lam=self.lam, size=self.n)  
            return self.sample


class Normal(Distribution):
    def __init__(self,mean,sd,n):
        Distribution.__init__(self,n)
        self.mean = mean
        self.sd = sd

    def draw(self):
        if (self.mean == None) or (self.sd == None):
            raise Exception('Normal distribution must have a mean and a standard deviation')
        else:
            self.sample = np.random.normal(loc=self.mean, scale=self.sd, size=self.n) 
            return self.sample


