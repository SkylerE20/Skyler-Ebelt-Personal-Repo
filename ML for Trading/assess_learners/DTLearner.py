import numpy as np

class DTLearner(object):
    """
    This initial code has been copied from LinRegLearners
    """
    def __init__(self, leaf_size, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose


    def author(self):
        return "sebelt3"  # replace tb34 with your Georgia Tech username

    def studygroup(self):
        return "sebelt3" #I did it this time #swag


    def best_split(self,data):
        # third and final solution loop ONLY in cor_matrix, loop calculates corcoef for EACH feature then returns index of the feature with max cor
        data_x = data[:, :-1]
        cor_matrix = [abs(np.corrcoef(x, data[:, -1], False)[0,1]) for x in data_x.T]#this took too long to get working
        return cor_matrix.index(np.nanmax(cor_matrix))
        #solution attempt 2: worked for a little bit until I started grading learners
        #cor_matrix = cor_matrix.transpose()
        #best_coef = np.nanmax(cor_matrix)
        #coef_index = np.where(cor_matrix == best_coef)  # I LOVE STACK OVERFLOW https://stackoverflow.com/questions/432112/is-there-a-numpy-function-to-return-the-first-index-of-something-in-an-array
        #print(cor_matrix)
        # Initial solution attempt for loop where i = feature and where i does not include last row of data (aka y)
        # This was the intuitive first step for me but it simply wasnt working, seemed to return a list of coefs when an array was needed
        # coef_final = np.zeros((1,len(self.data_x[0, :])))
        # for i in range(len(self.data[0,:-1])):
        # cor_matrix = abs(np.corrcoef(self.data[:,i], self.data[:,-1], False))
        # print(cor_matrix[0,0])
        # np.append(coef_final, cor_matrix[0])
        # corcoef = np.array(cor_matrix[1,0])
        # print(corcoef)
        # maxcoef = max(corcoef)
        # corcoef = np.where(cor_matrix == max(corcoef))
        # np.append(coef_final, corcoef)
        # print(coef_final)
        #return int(coef_index[0])  # Returns just the column index of the best coefficient, should simply return [0] or [1]...[n] where n is any best feature in data

    #First time using recursion, my undergrad program was a waste of $50,000 usd. Thank you GT
    def build_tree(self, data):
        #if data.shape[0] <= self.leaf_size:
            #y = data[0, -1]
            #return np.array([["Leaf", y, "NA", "NA"]])
        if len(np.unique(data[:, -1])) == 1 or data[:, :-1].shape[0] <= self.leaf_size:
            return np.array([[-1, np.mean(data[:, -1]), "NA", "NA"]])
        else:
            best_feat = self.best_split(data)
            splitval = np.mean(data[:, best_feat])
            lefttree = self.build_tree(data[data[:, best_feat] <= splitval])
            righttree = self.build_tree(data[data[:, best_feat] > splitval])
            root = np.array([[best_feat, splitval, 1, lefttree.shape[0] + 1]])
            tree_final = np.concatenate((root, lefttree, righttree), axis = 0)
            return tree_final

    def add_evidence(self, data_x, data_y):
        if len(data_y.shape) == 1:
            data_y = np.reshape(data_y, (data_x.shape[0],1))#Need to reshape y data to match x data or it throws axis out of bound errors

        data = np.append(data_x, data_y, axis=1)
        self.tree = self.build_tree(data)

    def query(self, points):
        pred_final = []
        tree = self.tree
        for i in range(points.shape[0]):
            pointer = 0
            while tree[pointer, 0] != "-1":
                j = int(float(tree[pointer, 0]))
                if points[i,j] <= float(tree[pointer, 1]):
                        lefttree = int(float(tree[pointer, 2]))
                        pointer = pointer + lefttree
                else:
                    righttree = int(float(tree[pointer, 3]))
                    pointer = pointer + righttree
            pred = tree[pointer, 1]
            pred_final.append(float(pred))
        return np.array(pred_final)


if __name__ == "__main__":
    print("DTLearner")