# coding: utf-8
# !/usr/bin/python

"""
Project: Page Rank
Mon Jun 11 11:15:31 2018
"""

import logging
import numpy as np
import time

from sklearn.preprocessing import normalize
from scipy.sparse import csc_matrix

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'jason.xing.zhang@gmail.com'


def page_rank(row, col, data, size, a=0.85, tol=1e-5, itermax=1000, logger=None):
    """
    Calculate PageRank scores

    Args:
        row (np.array): row indices
        col (np.array): column indices
        data (np.array): data
        size (int): size of matrix
        a (float): rate alpha
        tol (float): tolerance
        itermax (int): max iteration number
        logger (logger): logger

    Returns:
        x_star (np.array): scores
    """
    if logger is None:
        formatter = logging.Formatter('%(filename)s > %(funcName)s() > line:%(lineno)d @ %(asctime)s : %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger = logging.getLogger(__name__)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    A = normalize(csc_matrix((data, (row, col)), shape=(size, size)), axis=0, norm='l1')
    n = np.size(A, 0)
    e = np.ones([n, 1])
    x = e/n

    if logger is not False:
        logger.info("Start......................................")
        starttime = time.time()

    for iteration in range(itermax):
        temp = a*A.dot(x)
        norm_temp = e.T.dot(temp)[0]
        x_star = temp + (1 - norm_temp)/n*e
        ctol = np.linalg.norm((x_star - x)/x, np.inf)
        x = x_star
        if logger is not False:
            logger.info("Iteration {}: tolerance = {}".format(iteration+1, ctol))
        if ctol <= tol:
            break

    if logger is not False:
        timeused = time.time() - starttime
        logger.info("Finished {} iterations in {} seconds.".format(iteration+1, timeused))
        logger.info("Final error is {}".format(ctol))

    return x_star
