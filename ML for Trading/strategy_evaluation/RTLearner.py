import numpy as np

class RTLearner(object):
    """
    This initial code has been copied from LinRegLearners
    """
    def __init__(self,leaf_size, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose


    def author(self):
        return "sebelt3"  # replace tb34 with your Georgia Tech username

    def studygroup(self):
        return "sebelt3" #I did it this time #swag


    def best_split(self,data):
        """
        Modified DTLearner best_split code!
        """
        #second solution attempt: No loop
        lower = 0
        upper = data[:,:-1].shape[1]
        choose_rand =  np.random.randint(lower, upper)

        return int(choose_rand) #Returns just the column index of the best coefficient, should simply return [0] or [1]...[n] where n is any best feature in data

    #First time using recursion, my undergrad program was a waste of $50,000 usd. Thank you GT
    def build_tree(self, data):
        """ Refactored p. 3 code changed to better work with strategy learner"""
        if data.shape[0] <= self.leaf_size or len(np.unique(data[:, -1])) == 1:
            return np.array([[-1, np.mean(data[:, -1]), "NA", "NA"]])

        best_feat = self.best_split(data)
        splitval = np.median(data[:, best_feat])

        left_mask = data[:, best_feat] <= splitval
        right_mask = ~left_mask
        if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
            return np.array([[-1, np.mean(data[:, -1]), "NA", "NA"]])

        lefttree = self.build_tree(data[left_mask])
        righttree = self.build_tree(data[right_mask])

        # Create root node
        root = np.array([[best_feat, splitval, 1, lefttree.shape[0] + 1]])
        tree_final = np.concatenate((root, lefttree, righttree), axis=0)
        return tree_final
    def add_evidence(self, data_x, data_y):
        if len(data_y.shape) == 1:
            data_y = np.reshape(data_y, (
            data_x.shape[0], 1))  # Need to reshape y data to match x data or it throws axis out of bound errors

        data = np.append(data_x, data_y, axis=1)
        self.tree = self.build_tree(data)
        if self.verbose is True: print(self.tree)

    def query(self, points):
        pred_final = []
        tree = self.tree
        for i in range(points.shape[0]):
            pointer = 0
            while tree[pointer, 0] != "-1":
                j = int(float(tree[pointer, 0]))
                if points[i, j] <= float(tree[pointer, 1]):
                    lefttree = int(float(tree[pointer, 2]))
                    pointer = pointer + lefttree
                else:
                    righttree = int(float(tree[pointer, 3]))
                    pointer = pointer + righttree
            pred = tree[pointer, 1]
            pred_final.append(float(pred))
        return np.array(pred_final)


if __name__ == "__main__":
    pass