import numpy as np
from scipy.stats import norm
from sklearn.feature_extraction.text import CountVectorizer

class FeatureSelection:
    """
    The class provides implementation of major discriminative feature metrics
    
    :param vectorizer: A vectorizer fit on the complete dataset
    :param dataframe postive_df: A dataframe containing all the postive examples
    :param dataframe negative_df: A dataframe containing all the negative examples
    """

    def preprocess(self, X, y):
    
        classes = list(np.unique(y))

        positive = X[y==classes[0]].copy()
        negative = X[y==classes[1]].copy()

        self.tp = positive.sum(axis=0)
        self.tp = np.asarray(self.tp).reshape(-1)
        self.tpr = self.tp / positive.shape[0]

        self.fp = negative.sum(axis=0)
        self.fp = np.asarray(self.fp).reshape(-1)
        self.fpr = self.fp / negative.shape[0]


        fn = positive.shape[0] - self.tp
        tn = negative.shape[0] - self.fp
        
        self.fn = np.asarray(fn).reshape(-1)
        self.tn = np.asarray(tn).reshape(-1)


    def acc2(self, X, y):

        self.preprocess(X, y)

        return np.abs(self.tpr - self.fpr)

    def ndm(self, X, y):

        self.preprocess(X, y)

        tprfpr = [self.tpr, self.fpr]

        min_val = np.min(tprfpr, axis=0)
        min_val = np.where(min_val == 0 , 0.1, min_val)

        return np.abs(self.tpr - self.fpr) / min_val


    def bns(self, X, y):

        self.preprocess(X, y)

        # cover the edge cases
        tpr = np.where(self.tpr == 0 , 0.0005, self.tpr)
        tpr = np.where(tpr == 1 , 0.99, tpr)

        fpr = np.where(self.fpr == 0 , 0.0005, self.fpr)
        fpr = np.where(fpr == 1 , 0.99, fpr)

        return np.abs(norm.ppf(tpr) - norm.ppf(fpr))

    def odds_ratio(self, X, y):

        self.preprocess(X, y)
        
        den = self.fp * self.fn
        den = np.where(den == 0 , 0.01, den)

        return self.tp * self.tn / den

    def gini(self, X, y):

        self.preprocess(X, y)

        return self.tpr**2 * (self.tp/(self.tp+self.fp))**2 + self.fpr**2 * (self.fp/(self.tp+self.fp))**2

    def dfs(self, X, y):

        self.preprocess(X, y)
        
        classes = list(np.unique(y))
        total_pos, total_neg = np.count_nonzero(y == classes[0]), np.count_nonzero(y == classes[1])

        positive = (self.tp / (self.tp + self.fp)) / (self.fn / total_pos + self.fp / total_neg + 1)
        negative = (self.fp / (self.tp + self.fp)) / (self.tn / total_neg + self.tp / total_pos + 1)

        return positive + negative

    def IG(self, X, y):
        
        self.preprocess(X, y)

        classes = list(np.unique(y))
        total_pos, total_neg = np.count_nonzero(y == classes[0]), np.count_nonzero(y == classes[1])
        
        e1 = total_pos / (total_neg + total_pos)
        e2 = total_neg / (total_neg + total_pos)

        Epn = - e1 * np.log2(e1) - e2 * np.log2(e2)

        Pw = (self.tp + self.fp) / len(y)
        PwBar = 1 - Pw

        tp = self.tp / (self.tp + self.fp)
        tp = np.where(tp == 0 , 1e-10, tp)
        fp = self.fp / (self.tp + self.fp)
        fp = np.where(fp == 0 , 1e-10, fp)

        eTpFp = -tp * np.log2(tp) - fp * np.log2(fp)

        tn = self.tn / (self.tn + self.fn)
        tn = np.where(tn == 0 , 1e-10, tn)
        fn = self.fn / (self.tn + self.fn)
        fn = np.where(fn == 0 , 1e-10, fn)

        eTnFn = -tn * np.log2(tn) - fn * np.log2(fn)

        return Epn - (Pw * eTpFp + PwBar * eTnFn)

    def ChiSquare(self, X, y):
        self.preprocess(X, y)
        
        den = (self.tp + self.fp) * (self.fn + self.tn) * (self.tp + self.fn) * (self.fp + self.tn)
        
        return (self.tp * self.tn - self.fn * self.fp)**2 / den

