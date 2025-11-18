import numpy as np, LinRegLearner as lrl, DTLearner as dtl, RTLearner as rtl, BagLearner as bl
class InsaneLearner(object):
    def __init__(self,verbose = False):
        self.learners = []
        bags = 20
        self.verbose = verbose
        for i in range(bags):
            self.learners.append(bl.BagLearner(lrl.LinRegLearner, {}, False, 20, False))
    def author(self):
        return "sebelt3"
    def add_evidence(self, data_x, data_y):
        for i in self.learners:
            i.add_evidence(data_x, data_y)
        return
    def query(self, points):
        result = [learner.query(points) for learner in self.learners]
        result_final = np.mean(result, axis=0)
        return result_final
if __name__ == "__main__":
    print("InsaneLearner")