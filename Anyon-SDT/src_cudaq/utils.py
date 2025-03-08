"""
functions: 
    nth_largest
    check_first_five_bits
"""

import heapq
import numpy as np


def nth_largest(lst, n):
    """
    Finds the nth largest element from a list
    """
    return heapq.nlargest(n, lst)[-1]


def check_first_five_bits(num, total_bits=11, ref=0b11110):
    """ 
    Equivalence check of the first_five_bits of a bitstring. As a key argument, ref is the optimal solution
    """
    first_five = (num >> (total_bits - 5))
    return first_five == ref