#!/usr/bin/env python
"""
Created on Friday, March 18, 2022 at 09:31:55 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-31 09:21:05 wcobb>
 
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

def loader(parq_name:str = "Dataset-Unicauca-Version2-87Atts.csv.parq",
           verbose:bool = False,
          ) -> pd.DataFrame:
    """
    Function which fetches the traffic data...

    """
    if (verbose):
        bt = time.time()
    parq_path = os.path.join(places("datasets"), parq_name)
    if (not os.path.exists(parq_path)):
        print(f"could not find {name}, searching for alternatives")
        bare_name = parq_name.replace(".parq", "")
        bare_path = os.path.join(places("datasets", bare_name))
        if (not os.path.exists(bare_path)):
            raise RuntimeError(f"could not find {bare_name} or {name}")
        else:
            if (verbose):
                print(f"found {bare_name}, loading...")
            df = pd.read_csv(bare_path)
    else:
        if (verbose):
            print(f"found {parq_name}, loading...")
        df = pd.read_parquet(parq_path)
    #
    # okay so we have the data, let's read it..
    #
    if (verbose):
        et = time.time()
        print(f"read dataframe with shape {df.shape} in {round(et - bt, 3)} secs")
    return df
