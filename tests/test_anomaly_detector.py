#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-13 15:45:35 wcobb>
 
"""
#
# standard imports
#
import gzip, os, time
import math
from math import log10
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
from tqdm import tqdm
import dill

import threat
from threat.core import AnomalyDetector

if (__name__ == "__main__"):
    """
    """
    print("\nfunctional test for AnomalyDetector")
    metrics = AnomalyDetector(internal_threshold = 1000, external_threshold = 100, verbose = True)

