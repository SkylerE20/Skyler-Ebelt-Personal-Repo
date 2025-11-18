""""""
"""  		  	   		 	 	 			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
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
"""  		  	   		 	 	 			  		 			     			  	 
import util
import math  		  	   		 	 	 			  		 			     			  	 
import sys  		  	   		 	 	 			  		 			     			  	 

import matplotlib.pyplot as plt
import numpy as np  		  	   		 	 	 			  		 			     			  	 
import time

import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as il
  		  	   		 	 	 			  		 			     			  	 
if __name__ == "__main__":
    datafile = sys.argv[1]
    with util.get_learner_data_file(datafile) as f:
        data = np.genfromtxt(f, delimiter=",")
        # Skip the date column and header row if we're working on Istanbul data
        if datafile == "Istanbul.csv":
            data = data[1:, 1:]

    #if len(sys.argv) != 2:
    #    print("Usage: python testlearner.py <filename>")
    #    sys.exit(1)
    #inf = open(sys.argv[1])
    #data = np.array(
    #    [list(map(float, s.strip().split(","))) for s in inf.readlines()]
    #)

    #print(data[0,0].dtype)

    # compute how much of the data is training and testing  		  	   		 	 	 			  		 			     			  	 
    train_rows = int(0.6 * data.shape[0])  		  	   		 	 	 			  		 			     			  	 
    test_rows = data.shape[0] - train_rows  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    # separate out training and testing data  		  	   		 	 	 			  		 			     			  	 
    train_x = data[:train_rows, 0:-1]  		  	   		 	 	 			  		 			     			  	 
    train_y = data[:train_rows, -1]  		  	   		 	 	 			  		 			     			  	 
    test_x = data[train_rows:, 0:-1]  		  	   		 	 	 			  		 			     			  	 
    test_y = data[train_rows:, -1]  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    #print(f"{test_x.shape}")
    #print(f"{test_y.shape}")
  		  	   		 	 	 			  		 			     			  	 
    # create a learner and train it  		  	   		 	 	 			  		 			     			  	 
    learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner  		  	   		 	 	 			  		 			     			  	 
    learner.add_evidence(train_x, train_y)  # train it  		  	   		 	 	 			  		 			     			  	 
    #print(learner.author())
  		  	   		 	 	 			  		 			     			  	 
    # evaluate in sample  		  	   		 	 	 			  		 			     			  	 
    pred_y = learner.query(train_x)  # get the predictions  		  	   		 	 	 			  		 			     			  	 
    rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])  		  	   		 	 	 			  		 			     			  	 
    #print()
    #print("In sample results")
    #print(f"RMSE: {rmse}")
    c = np.corrcoef(pred_y, y=train_y)  		  	   		 	 	 			  		 			     			  	 
    #print(f"corr: {c[0,1]}")
  		  	   		 	 	 			  		 			     			  	 
    # evaluate out of sample  		  	   		 	 	 			  		 			     			  	 
    pred_y = learner.query(test_x)  # get the predictions  		  	   		 	 	 			  		 			     			  	 
    rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])  		  	   		 	 	 			  		 			     			  	 
    #print()
    #print("Out of sample results")
    #print(f"RMSE: {rmse}")
    c = np.corrcoef(pred_y, y=test_y)  		  	   		 	 	 			  		 			     			  	 
    #print(f"corr: {c[0,1]}")
    """
    TEST DTLEARNER
    """

    #DTlearner = dtl.DTLearner(leaf_size = 1)  # create a DTLearner
    #DTlearner.add_evidence(train_x, train_y) # train it
    #print(DTlearner.best_split(data))
    #print(DTlearner.query(test_x))

    """
    TEST RTLEARNER
    """
    #RTlearner = rtl.RTLearner(leaf_size = 1, verbose = False)
    #RTlearner.add_evidence(train_x, train_y)  # train it
    #print(RTlearner.best_split(data))
    #print(RTlearner.query(test_x))
    """
    TEST BAGLEARNER
    """
    #Blearner = bl.BagLearner(dtl.DTLearner, {"leaf_size":1}, False, 5)
    #Blearner.add_evidence(train_x, train_y)
    #print(learner.query(test_x))
    """
    TEST INSANELEARNER
    """
    #learner2 = il.InsaneLearner(True)
    #learner2.add_evidence(train_x, train_y)
    #print(learner2.query(test_x))
    """
    Experiment 1:
    """
    leaf_vals = 50

    exp_temp_in = []
    exp_temp_out = []
    leaf_vals = 50
    for i in range(leaf_vals + 1):
        DTlearner = dtl.DTLearner(leaf_size=i,verbose=False)
        DTlearner.add_evidence(train_x, train_y)
        in_pred_y = DTlearner.query(train_x)  # get the predictions
        in_rmse = math.sqrt(((train_y - in_pred_y) ** 2).sum() / train_y.shape[0])
        exp_temp_in.append(in_rmse)
        DTlearner2 = dtl.DTLearner(leaf_size=i, verbose=False)
        DTlearner2.add_evidence(train_x, train_y)
        out_pred_y = DTlearner2.query(test_x)  # get the predictions
        out_rmse = math.sqrt(((test_y - out_pred_y) ** 2).sum() / test_y.shape[0])
        exp_temp_out.append(out_rmse)

    #Experiment 2:

    plt.clf()
    bag_exp_temp_in = []
    bag_exp_temp_out = []
    for i in range(leaf_vals + 1):
        Blearner = bl.BagLearner(learner = dtl.DTLearner,bags = 20,kwargs = {"leaf_size":i}, verbose=False)
        Blearner.add_evidence(train_x, train_y)
        in_pred_y = Blearner.query(train_x)  # get the predictions
        in_rmse = math.sqrt(((train_y - in_pred_y) ** 2).sum() / train_y.shape[0])
        bag_exp_temp_in.append(in_rmse)
        out_pred_y = Blearner.query(test_x)  # get the predictions
        out_rmse = math.sqrt(((test_y - out_pred_y) ** 2).sum() / test_y.shape[0])
        bag_exp_temp_out.append(out_rmse)

    """
    Experiment 3:
    """

    dt_err = []
    dt_time = []
    rt_err = []
    rt_time = []
    leaf_vals = 50
    for i in range(leaf_vals + 1):
        dt_t_start = time.time()
        Blearner2 = bl.BagLearner(learner = dtl.DTLearner,bags = 20,kwargs = {"leaf_size":i}, verbose=False)
        Blearner2.add_evidence(train_x, train_y)
        dt_t_end = time.time()
        dt_train_time = dt_t_end - dt_t_start
        dt_time.append(dt_train_time)
        dt_pred_y = Blearner2.query(train_x)  # get the predictions
        error = (float(abs(train_y - dt_pred_y).sum()) /test_y.shape[0])
        dt_err.append(error)

    for i in range(leaf_vals + 1):
        rt_t_start = time.time()
        Blearner3 = bl.BagLearner(learner = rtl.RTLearner,bags = 20,kwargs = {"leaf_size":i}, verbose=False)
        Blearner3.add_evidence(train_x, train_y)
        rt_t_end = time.time()
        rt_train_time = rt_t_end - rt_t_start
        rt_time.append(rt_train_time)
        rt_pred_y = Blearner3.query(train_x)  # get the predictions
        error = (float(abs(train_y - rt_pred_y).sum()) /test_y.shape[0])
        rt_err.append(error)

    plt.plot(exp_temp_in, label="Out of sample results")
    plt.plot(exp_temp_out, label="In sample RMSE")
    plt.axis([0, leaf_vals, 0, 0.01])
    plt.xlabel('RMSE')
    plt.ylabel('Number of Leaves')
    plt.title('Experiment 1, DT In Sample vs Out of Sample RMSE')
    plt.legend()
    plt.savefig("figure1.png")

    plt.clf()
    plt.plot(bag_exp_temp_in, label="Out of sample results")
    plt.plot(bag_exp_temp_out, label="In sample RMSE")
    plt.axis([0, leaf_vals, 0, 0.01])
    plt.xlabel('RMSE')
    plt.ylabel('Number of Leaves')
    plt.title('Experiment 2, DT In Sample vs Out of Sample RMSE Using 20 Bags')
    plt.legend()
    plt.savefig("figure2.png")

    plt.clf()
    plt.plot(dt_err, label="DT MAE")
    plt.plot(rt_err, label="RT MAE")
    plt.xlabel('Number of Leaves (20 Bags)')
    plt.ylabel('MAE')
    plt.title('Experiment 3, DT Vs RT Absolute Error')
    plt.legend()
    plt.savefig("figure3.png")

    plt.clf()
    plt.plot(dt_time, label="DT Time to Train")
    plt.plot(rt_time, label="RT Time to Train")
    plt.xlabel('Number of Leaves (20 Bags)')
    plt.ylabel('Time to Train')
    plt.title('Experiment 3, DT Vs RT Train Times')
    plt.legend()
    plt.savefig("figure4.png")