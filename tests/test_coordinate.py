#!/usr/bin/env python
"""
Created on Tuesday, March 15, 2022 at 13:34:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-16 11:03:23 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip
#
# ds imports...
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
#
# web content imports...
#
import json, hashlib, requests, urllib.request
#
# threat specific imports...
#
import threat
from threat.core import places
from threat.core import excluding
from threat.core import Latitude, Longitude

if (__name__ == "__main__"):
    print("")
    mylat = Latitude("N", 34, 39, 43.31)
    print(f"latitude: {mylat} or {mylat.asfloat()}")
    mylon = Longitude("W", 92, 51, 38.75)
    print(f"longitude: {mylon} or {mylon.asfloat()}")

    
