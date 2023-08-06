"""Functions to create and matrixes of ortholog relationships."""
import os
import sys
'''
import numpy as np
import multiprocessing as mp
from shutil import move, rmtree, copy
from typing import Dict, List, Deque, Any, Tuple, Set
from collections import OrderedDict, deque
from sonicparanoid import sys_tools as systools
from subprocess import Popen, PIPE
import pickle
import hashlib
from functools import partial
'''

#### IMPORT TO GENERATE PyPi package
from sonicparanoid import sys_tools as systools
#from sonicparanoid import seq_tools as seqtools
#from sonicparanoid import workers



__module_name__ = 'Matrix'
__source__ = 'matrix.py'
__author__ = 'Salvatore Cosentino'
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Cosentino Salvatore'
__email__ = 'salvo981@gmail.com'



### FUNCTIONS ####
def info() -> None:
    """Functions to create a graph from ortholog tables."""
    print('MODULE NAME:\t%s'%__module_name__)
    print('SOURCE FILE NAME:\t%s'%__source__)
    print('MODULE VERSION:\t%s'%__version__)
    print('LICENSE:\t%s'%__license__)
    print('AUTHOR:\t%s'%__author__)
    print('EMAIL:\t%s'%__email__)
