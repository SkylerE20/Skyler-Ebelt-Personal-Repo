import numpy as np

class BagLearner(object):
    def __init__(self, learner, kwargs, boost = False, bags = 1, verbose = False):
        self.learners = []
        self.kwargs = kwargs
        self.verbose = verbose
        self.boost = boost
        for i in range(bags):
            self.learners.append(learner(**kwargs))
    def author(self):
        return "sebelt3"

    def studygroup(self):
        return "sebelt3"

    def add_evidence(self, data_x, data_y):
        for i in self.learners:
            j = np.random.choice(data_x.shape[0], size = data_x.shape[0])
            i.add_evidence(data_x[j], data_y[j])

    def query(self, points):
        result = [i.query(points) for i in self.learners]#similar solution as found in DT best_feat, Loop through each learner, pull pred vals, append to new array
        result_final = np.array(np.mean(result, axis=0))
        return result_final

if __name__ == "__main__":
    pass