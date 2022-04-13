#!/usr/bin/env python
"""
Created on Tuesday, April 12, 2022 at 09:01:37 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 09:02:02 wcobb>
 
"""
import math
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
from tqdm import tqdm
import dill

def scaled_rgba_v2(this_value:float, dpower:int = 0, min_value:float = 0.0, max_value:float = 1.0):
    if (dpower >= 5):
        color = "red"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 4):
        color = "orange"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 3):
        color = "yellow"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 2):
        color = "green"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 1):
        color = "blue"
        alpha = (this_value - min_value)/(max_value - min_value)
    else:
        color = "indigo"
        alpha = (this_value - min_value)/(max_value - min_value)
    return (color, alpha)

def scaled_rgba(mea, mea_min = 0.05, mea_mid = 2.5, mea_max = 5.0):
    """
    Produces an rgba color based on the range of the data and some
    properties of the distribution...

    """
    R = (1 - (mea_max - mea)/(mea_max - mea_min))
    if (R > 1):
        R = 1
    elif (R < 0):
        R = 0
    G = (1-abs(mea_mid - mea)/mea_mid)
    if (G > 1):
        G = 1
    elif (G < 0):
        G = 0
    B = (mea_max - mea)/(mea_max - mea_min)
    if (B > 1):
        B = 1
    elif (B < 0):
        B = 0
    A = R
    return (R, G, B, A)

