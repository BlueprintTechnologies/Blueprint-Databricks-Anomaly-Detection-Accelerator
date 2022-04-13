#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 09:07:00 wcobb>
 
"""
#
# standard imports
#
import gzip
import math
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
from tqdm import tqdm
import dill

import threat
from threat.common import scaled_rgba_v2
from threat.core import loader, places
from threat.core import public_address
from threat.core import Cache
from threat.core import display_protocol_worldmap

if (__name__ == "__main__"):
    """
    """
    print("")
    population = dill.load(gzip.open(os.path.join(places("datasets"), "updated_population_metrics.dill.gz"), "rb"))
    #
    # pass the population data object to the graphics routine...
    #
    display_protocol_worldmap(population, min_count = 1000, anomaly_scaling = "square")
