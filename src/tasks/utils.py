import multiprocessing
from multiprocessing import Pool

import numpy as np
import pandas as pd
import scipy
from scipy import spatial


def calc(args):
    return args[0] @ args[1]


def cos_calc(args):
    return (
        1
        - scipy.spatial.distance.cdist(
            args[0].reshape(1, -1), args[1].reshape(1, -1), "cosine"
        )[0][0]
    )


def euc_calc(args):
    return -np.sum((args[0] - args[1]) ** 2)


def euc_norm_calc(args):
    one = args[0] / np.sqrt(np.sum(args[0] ** 2))
    second = args[1] / np.sqrt(np.sum(args[1] ** 2))
    return -np.sum((one - second) ** 2)


def avg_calc(pairs):
    """
    pairs: word pairs
    
    return: average score
    """
    if len(pairs) != 0:
        pairs = [calc(pair) for pair in pairs]
        return (np.average(pairs), np.std(pairs))


def max_calc(pairs):
    """
    pairs: word pairs
    
    return: max score
    """
    if len(pairs) != 0:
        pairs = [calc(pair) for pair in pairs]
        return (np.max(pairs), np.std(pairs))


def avg_cos_calc(pairs):
    """
    pairs: word pairs
    
    return: average score
    """
    if len(pairs) != 0:
        pairs = [cos_calc(pair) for pair in pairs]
        return (np.average(pairs), np.std(pairs))


def max_cos_calc(pairs):
    """
    pairs: word pairs
    
    return: max score
    """
    if len(pairs) != 0:
        pairs = [cos_calc(pair) for pair in pairs]
        return (np.max(pairs), np.std(pairs))


def avg_euclid_dis(pairs):
    """
    pairs: word pairs
    
    return: euclid distance
    """
    if len(pairs) != 0:
        pairs = [euc_calc(pair) for pair in pairs]
        return (np.average(pairs), np.std(pairs))


def max_euclid_dis(pairs):
    """
    pairs: word pairs
    
    return: euclid distance
    """
    if len(pairs) != 0:
        pairs = [euc_calc(pair) for pair in pairs]
        return (np.max(pairs), np.std(pairs))


def avg_euclid_norm_dis(pairs):
    """
    pairs: word pairs
    
    return: euclid distance
    """
    if len(pairs) != 0:
        pairs = [euc_norm_calc(pair) for pair in pairs]
        return (np.average(pairs), np.std(pairs))


def max_euclid_norm_dis(pairs):
    """
    pairs: word pairs
    
    return: euclid distance
    """
    if len(pairs) != 0:
        pairs = [euc_norm_calc(pair) for pair in pairs]
        return (np.max(pairs), np.std(pairs))


class dict2obj(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                setattr(self, key, dict2obj(value))
            elif (
                isinstance(value, list)
                and len(value) != 0
                and isinstance(value[0], dict)
            ):
                setattr(self, key, [dict2obj(val) for val in value])
            else:
                setattr(self, key, value)
