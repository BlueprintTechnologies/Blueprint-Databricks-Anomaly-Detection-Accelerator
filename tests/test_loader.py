#!/usr/bin/env python
"""
Created on Friday, March 18, 2022 at 09:31:55 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-18 14:46:34 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip

import pandas as pd
import numpy as np

from threat.core import places
from threat.core import loader

if (__name__ == "__main__"):
    """
    Trivial smoke test for the loader

    """
    print("")
    df = loader(verbose = True)
    print("")
    print(f"dataframe contains columns {list(df.columns)}")
    print("")
    print(f"transaction protocals: {list(np.unique(df['ProtocolName']))}")
    
