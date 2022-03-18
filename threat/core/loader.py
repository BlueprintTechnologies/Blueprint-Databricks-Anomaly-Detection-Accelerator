#!/usr/bin/env python
"""
Created on Friday, March 18, 2022 at 09:31:55 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-18 14:17:30 wcobb>
 
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

def loader(name:str = "Dataset-Unicauca-Version2-87Atts.csv",
           verbose:bool = False,
          ) -> pd.DataFrame:
    """
    Function which fetches the traffic data...

    """
    path = os.path.join(places("datasets"), name)
    if (not os.path.exists(path)):
        raise RuntimeError(f"could not find {path}")
    #
    # okay so we have the data, let's read it..
    #
    if (verbose):
        bt = time.time()
    df = pd.read_csv(path)
    if (verbose):
        et = time.time()
        print(f"read dataframe with shape {df.shape} in {round(et - bt, 3)} secs")
    return df
