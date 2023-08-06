"""Functions to create graph and matrixes from ortholog tables."""
import os
import sys
import numpy as np
#import multiprocessing as mp
#from shutil import move, rmtree, copy
from typing import Dict, List, Deque, Any, Tuple, Set
#from collections import OrderedDict, deque
from sonicparanoid import sys_tools as systools
#from subprocess import Popen, PIPE
import pickle

#### IMPORT TO GENERATE PyPi package
#from sonicparanoid import seq_tools as seqtools
#from sonicparanoid import workers



__module_name__ = 'Graph'
__source__ = 'graph.py'
__author__ = 'Salvatore Cosentino'
__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'Cosentino Salvatore'
__email__ = 'salvo981@gmail.com'



""" FUNCTIONS """
def info() -> None:
    """Functions to create a graph from ortholog tables."""
    print('MODULE NAME:\t%s'%__module_name__)
    print('SOURCE FILE NAME:\t%s'%__source__)
    print('MODULE VERSION:\t%s'%__version__)
    print('LICENSE:\t%s'%__license__)
    print('AUTHOR:\t%s'%__author__)
    print('EMAIL:\t%s'%__email__)



def pairwise_tbl2tpl_dict(inTbl: str, debug: bool=False) -> str:
    """Extract ortholog relationships from ortholog table and store those in
    dictionaries of tuples"""
    if debug:
        print('\npairwise_tbl2tpl_dict :: START')
        print('Input table:\t{:d}'.format(inTbl))
    if not os.path.isdir(inTbl):
        sys.stderr.write("\nERROR: the ortholog table was not found.")
        sys.exit(-2)

    # output dictionary (a digest for each file name)
    relDict: Dict[Dict, Tuple[str, str, float]] = {}
    # start parsing the table
    ifd = open(inTbl, "r")
    # example of line to be parsed
    # 334	64	1.1110 0.051 1.943 1.0	2.16 1.0 2.653 0.18
    # skip the header
    ifd.readline()
    clstrId: int = 0
    for ln in ifd:
        clstrId += 1
        d1, lx, rx = ln.rstrip("\n").rsplit("\t", 2)
        # extract left part and put in dict
        lxDict: [str, float] = {}
        for i, ortho in enumerate(lx.split(" ")):
            if i%2 == 0: # then it is the ID name
                lxDict[ortho] = float(lx[i])
            else:
                continue

        print(lxDict)
        sys.exit("DEBUG :: pairwise_tbl2tpl_dict")


    ifd.close()
