""""""  		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
template for generating data to fool learners (c) 2016 Tucker Balch  		  	   		 	 	 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	 	 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	 	 			  		 			     			  	 
All Rights Reserved  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	 	 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	 	 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	 	 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	 	 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	 	 			  		 			     			  	 
or edited.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	 	 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	 	 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	 	 			  		 			     			  	 
GT honor code violation.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Student Name: Skyler Ebelt  		  	   		 	 	 			  		 			     			  	 
GT User ID: sebelt3   	 	   		 	 	 			  		 			     			  	 
GT ID: 904077010   		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import math  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import numpy as np  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
# this function should return a dataset (X and Y) that will work  		  	   		 	 	 			  		 			     			  	 
# better for linear regression than decision trees  		  	   		 	 	 			  		 			     			  	 
def best_4_lin_reg(seed=1489683273):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		 	 	 			  		 			     			  	 
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		 	 	 			  		 			     			  	 
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param seed: The random seed for your data generation.  		  	   		 	 	 			  		 			     			  	 
    :type seed: int  		  	   		 	 	 			  		 			     			  	 
    :return: Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		 	 	 			  		 			     			  	 
    :rtype: numpy.ndarray  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    np.random.seed(seed)  		  	   		 	 	 			  		 			     			  	 
    x = np.zeros((100, 2))
    for i in range(100):
        for j in range(2):
            x[i, j] = np.random.randint(1, 100)#Fill with random data, I don't think this should matter very much
    y = np.zeros((100, ))
    for i in range(100):
        y[i] = x[i,0] + x[i,1] #I'm not certain this is the best solution here, makes DT yield an RMSE of 9.75 so this sort of feels like cheating?
        #I'm gonna leave this in because it is not stated anywhere that RMSE cannot exceed 1, if you think about it, this really does "defeat" DT
        #in any case this models a linear relationship which is can be seen when testing in the excessively low RMSE of lrl
    #y = np.random.random(size=(100,))
    # Here's is an example of creating a Y from randomly generated  		  	   		 	 	 			  		 			     			  	 
    # X with multiple columns  		  	   		 	 	 			  		 			     			  	 
    # y = x[:,0] + np.sin(x[:,1]) + x[:,2]**2 + x[:,3]**3  		  	   		 	 	 			  		 			     			  	 
    return x, y  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
def best_4_dt(seed=1489683273):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		 	 	 			  		 			     			  	 
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		 	 	 			  		 			     			  	 
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param seed: The random seed for your data generation.  		  	   		 	 	 			  		 			     			  	 
    :type seed: int  		  	   		 	 	 			  		 			     			  	 
    :return: Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		 	 	 			  		 			     			  	 
    :rtype: numpy.ndarray  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    np.random.seed(seed)  		  	   		 	 	 			  		 			     			  	 
    x = np.zeros((100, 2))
    for i in range(100):
        for j in range(2):
            x[i, j] = np.random.randint(1,100) #Same as before: fill with random data
    y = np.random.random(size=(100,))
    for i in range(2):
        y = np.power((x[:,i]),.125) #Non linear relationship here which differs from above, this one doesnt feel like cheating, RMSE is kinda normal for both learners
    return x, y  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
def author():  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    :return: The GT username of the student  		  	   		 	 	 			  		 			     			  	 
    :rtype: str  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    return "sebelt3"  # Change this to your user ID

def studygroup(self):
    return "sebelt3"
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 

