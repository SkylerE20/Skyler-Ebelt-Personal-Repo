""""""
from numexpr.expressions import bestConstantType

"""Assess a betting strategy.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
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
import numpy as np
import matplotlib.pyplot as plt

def author():  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    :return: The GT username of the student  		  	   		 	 	 			  		 			     			  	 
    :rtype: str  		  	   		 	 	 			  		 			     			  	 
    """
    authorName = str("sebelt3")
    return authorName# replace tb34 with your Georgia Tech username.

  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
def gtid():  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    :return: The GT ID of the student  		  	   		 	 	 			  		 			     			  	 
    :rtype: int  		  	   		 	 	 			  		 			     			  	 
    """
    authorId = int(900897987)
    return authorId  # replace with your GT ID number
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
def get_spin_result(win_prob):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		 	 	 			  		 			     			  	 
    :type win_prob: float  		  	   		 	 	 			  		 			     			  	 
    :return: The result of the spin.  		  	   		 	 	 			  		 			     			  	 
    :rtype: bool  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    result = False  		  	   		 	 	 			  		 			     			  	 
    if np.random.random() <= win_prob:  		  	   		 	 	 			  		 			     			  	 
        result = True  		  	   		 	 	 			  		 			     			  	 
    return result  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
def experiment1(episodes, spinCount):
    win_prob = 0.474
    # win_prob = 0.9 #Duplicating this line to quickly change win prob to test output for debugging

    #episodes = 10
    #spinCount = 1000 #Ignore these: for debugging
    i = 0

    winnings = 0
    betHistoryex1 = np.zeros((episodes, spinCount))

    for j in range(spinCount):
        while i < episodes:
            if winnings < 80 and j <= spinCount:
                won = False
                wager = 1
                while not won:
                    won = get_spin_result(win_prob)
                    if won:
                        winnings = winnings + wager
                        betHistoryex1[i,j] = winnings
                        j += 1
                    else:
                        winnings = winnings - wager
                        betHistoryex1[i,j] = winnings
                        wager = wager * 2
                        j += 1

            else:
                winnings = 0
                i += 1
                j = 0

            while j < spinCount and winnings >= 80:
                betHistoryex1[i, j] = winnings
                j += 1
    betHistoryex1 = np.transpose(betHistoryex1)#transpose to correct errors while plotting

    return betHistoryex1


def experiment2(episodes2, spinCount2):
    win_prob = 0.474
    #win_prob = 0.2 #Duplicating this line to quickly change win prob to test output for debugging

    #episodes2 = 1000
    #spinCount2 = 1000 #Ignore these: for debugging
    i = 0

    maxLoss = -256

    winnings = 0
    betHistoryex2 = np.zeros((episodes2, spinCount2))

    for j in range(spinCount2):
        while i < episodes2:
            while 80 > winnings > maxLoss and j < spinCount2:
                won = False
                wager = 1
                while not won:
                    won = get_spin_result(win_prob)
                    if won:
                        if j == spinCount2:
                            winnings = 0
                            i += 1
                            j = 0
                        else:
                            winnings = winnings + wager
                            betHistoryex2[i, j] = winnings
                            j += 1
                    else:
                        if winnings - wager < maxLoss:
                            while winnings - wager < maxLoss:
                                wager -= 1
                        else:
                            if j == spinCount2:
                                winnings = 0
                                i += 1
                                j = 0
                            else:
                                winnings = winnings - wager
                                betHistoryex2[i, j] = winnings
                                wager = wager * 2
                                j += 1

            while j < spinCount2 and winnings >= 80:
                betHistoryex2[i, j] = winnings
                j += 1

            while j < spinCount2 and winnings == maxLoss:
                betHistoryex2[i, j] = winnings
                j += 1

            else:
                winnings = 0
                i += 1
                j = 0




    betHistoryex2 = np.transpose(betHistoryex2)#transpose to correct errors while plotting
    return(betHistoryex2)
    #print(betHistoryex2)

def test_code():  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    Method to test your code  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    win_prob = 0.474  # set appropriately to the probability of a win
    #Duplicating this line to quickly change win prob to test output for debugging
    np.random.seed(gtid())  # do this only once  		  	   		 	 	 			  		 			     			  	 
    print(get_spin_result(win_prob))  # test the roulette spin  		  	   		 	 	 			  		 			     			  	 
    # add your code here to implement the experiments

#####Start plots using betting strategy 1

#####Figure 1

    exp1f1 = experiment1(10,1000)
    plt.clf()

    lab1 = []
    for i in range(1, 11):
        lab1.append("Episode: " + str(i))
    plt.plot(exp1f1)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Count')
    plt.ylabel('Winnings (-/+)')
    plt.title('Experiment 1, Figure 1')
    plt.legend(lab1)
    #plt.show()
    plt.savefig("exp1f1plot.png")

    #Figure 2

    exp1f2 = experiment1(1000, 1000)
    plt.clf()
    mean = np.mean(exp1f2, axis=1)
    standev = np.std(exp1f2, axis=1)

    plt.plot(mean, label = 'Mean')
    plt.plot(mean+standev, label = 'Mean + stdev')
    plt.plot(mean-standev, label = 'Mean - stdev')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Count')
    plt.ylabel('Mean Winnings (-/+)')
    plt.title('Experiment 1, Figure 2')
    plt.legend()
    #plt.show()
    plt.savefig("exp1f2plot.png")

#####Figure 3

    exp1f3 = experiment1(1000, 1000)
    plt.clf()
    median = np.median(exp1f3, axis=1)
    standev = np.std(exp1f3, axis=1)

    plt.plot(median, label = 'Median')
    plt.plot(median + standev, label = 'Median + stdev')
    plt.plot(median - standev, label = 'Median - stdev')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Count')
    plt.ylabel('Median Winnings (-/+)')
    plt.title('Experiment 1, Figure 3')
    plt.legend()
    #plt.show()
    plt.savefig("exp1f3plot.png")

#####end plots of strategy 1

##### Start plots using betting strategy 2

#####Figure 1:

    exp2f1 = experiment2(1000, 1000)
    plt.clf()
    mean = np.mean(exp2f1, axis=1)
    standev = np.std(exp2f1, axis=1)

    plt.plot(mean, label = 'Mean')
    plt.plot(mean + standev, label = 'Mean + stdev')
    plt.plot(mean - standev, label = 'Mean - stdev')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Count')
    plt.ylabel('Mean Winnings (-/+)')
    plt.title('Experiment 2, Figure 1')
    plt.legend()
    #plt.show()
    plt.savefig("exp2f1plot.png")


##### Figure 2:

    exp2f2 = experiment2(1000, 1000)
    plt.clf()
    median = np.median(exp2f2, axis=1)
    standev = np.std(exp2f2, axis=1)

    plt.plot(median, label = 'Median')
    plt.plot(median + standev, label = 'Median + stdev')
    plt.plot(median - standev, label = 'Median - stdev')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin Count')
    plt.ylabel('Median Winnings (-/+)')
    plt.title('Experiment 2, Figure 2')
    plt.legend()
    #plt.show()
    plt.savefig("exp2f2plot.png")
# NOTE: THESE FUNCTIONS WILL NOT WORK PROPERLY WHILE BETHISTORYEX1 AND BETHISTORYEX2 ARE TRANSPOSED
####### Begin Calculations For Report:
    #Question set 1:
    wincount = 0

    for i in range(1000):
        if exp1f2[i,-1] == 80:
            wincount += 1
        else:
            wincount = wincount

    #print((wincount/1000)*100)

    exp = np.zeros((1, 1000))

    for i in range(1000):
        exp[0, i] = exp1f2[i,-1]
    #print(exp)

    #print(np.average(exp))

####Question set 2:
    wincount2 = 0

    for i in range(1000):
        if exp2f1[i,-1] == 80:
            wincount2 += 1
        else:
            wincount2 = wincount2

    #print((wincount2/1000)*100)

    exp2 = np.zeros((1, 1000))

    for i in range(1000):
        exp2[0, i] = exp2f1[i,-1]
    #print(exp)

    #print(np.average(exp2))
    #print(np.std(exp2))
if __name__ == "__main__":
    test_code()  		  	   		 	 	 			  		 			     			  	 
