import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    authorName = str("sebelt3")
    return authorName  # replace tb34 with your Georgia Tech username.


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

    # episodes = 10
    # spinCount = 1000
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
                        betHistoryex1[i, j] = winnings
                        j += 1
                    else:
                        winnings = winnings - wager
                        betHistoryex1[i, j] = winnings
                        wager = wager * 2
                        j += 1

            else:
                winnings = 0
                i += 1
                j = 0

            while j < spinCount and winnings >= 80:
                betHistoryex1[i, j] = winnings
                j += 1
    betHistoryex1 = np.transpose(betHistoryex1)  # transpose to correct errors while plotting

    return betHistoryex1


def experiment2(episodes, spinCount):
    win_prob = 0.474
    #win_prob = 0.2 #Duplicating this line to quickly change win prob to test output for debugging

    episodes = 10
    spinCount = 1000
    i = 0

    maxLoss = -256

    winnings = 0
    betHistoryex2 = np.zeros((episodes, spinCount))

    for j in range(spinCount):
        while i < episodes:
            while 80 > winnings > maxLoss and j <= spinCount:
                won = False
                wager = 1
                while not won:
                    won = get_spin_result(win_prob)
                    if won:
                        winnings = winnings + wager
                        betHistoryex2[i, j] = winnings
                        j += 1
                    else:
                        if winnings - wager < maxLoss:
                            while winnings - wager < maxLoss:
                                wager -= 1
                        else:
                            winnings = winnings - wager
                            betHistoryex2[i, j] = winnings
                            wager = wager * 2
                            j += 1

            while j < spinCount and winnings >= 80:
                betHistoryex2[i, j] = winnings
                j += 1

            while j < spinCount and winnings == maxLoss:
               betHistoryex2[i, j] = -256
               j += 1

            else:
                winnings = 0
                i += 1
                j = 0



    #betHistoryex2 = np.transpose(betHistoryex2)  # transpose to correct errors while plotting
    return (betHistoryex2)
    # print(betHistoryex2)


def test_code():
    """
    Method to test your code
    """
    win_prob = 0.474  # set appropriately to the probability of a win
    # Duplicating this line to quickly change win prob to test output for debugging
    np.random.seed(gtid())  # do this only once
    print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments

    # Start tests and plots using betting strategy 1

    # Figure 1

    exp1 = experiment2(10, 1001)
    print(exp1)

if __name__ == "__main__":
    test_code()
