#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-13 09:59:38 wcobb>
 
"""
#
# standard imports
#
import os
import time
import gzip
import math
import dill
import pandas as pd
import numpy as np
from scipy.stats import mode

from threat.core import places

class AnomalyDetectorError(Exception):
    """A custom exception type for the anomaly detector
    """
    pass

class AnomalyDetector():
    """A class for managing the detection of anomalies
    """
    def __init__(self,
                 stats_file_name:str = "updated_population_metrics.dill.gz",
                 anomaly_threshold_internal:int = 1000,
                 anomaly_threshold_external:int = 100,
                 overwrite:bool = False,
                 verbose:bool = True,
                 debug:bool = False,
                ):
        """
        """
        self.overwrite = overwrite
        self.verbose = verbose
        self.debug = debug
        #
        # sanity check the anomaly thresholds...
        #
        if (self.debug):
            print(f"...checking relative sizes of "
                  +f"anomaly_threshold_internal and anomaly_threshold_external)")
        if (anomaly_threshold_external >= anomaly_threshold_internal):
            raise AnomalyDetectorError(
                f"the 'internal' threshold {anomaly_threshold_internal}"
                + f" must logically be less than the 'external' threshold"
                + f" {anomaly_threshold_external}, yet it is not...")
        if (self.debug):
            print(f"...checking absolute size of anomaly_threshold_external)")
        if (anomaly_threshold_external <= 0):
            raise AnomalyDetectorError(
                f"the 'external' threshold {anomaly_threshold_external}"
                + f" just logically be > 0, yet it is not...")
        if (self.debug):
            print(f"...checking absolute size of anomaly_threshold_internal)")
        if (anomaly_threshold_internal <= 0):
            raise AnomalyDetectorError(
                f"the 'internal' threshold {anomaly_threshold_internal}"
                + f" just logically be > 0, yet it is not...")
        self.anomaly_threshold_internal = anomaly_threshold_internal
        self.anomaly_threshold_external = anomaly_threshold_external
        #
        # the path the where the anomaly statistics data lives...
        #
        if (self.debug):
            print(f"...creating stats_file_path")
        self.stats_file_path = os.path.join(places("datasets"), stats_file_name)
        #
        # make sure that we can find it...
        #
        if (self.debug):
            print(f"...making sure stats_file_path exists")
        if (not os.path.exists(self.stats_file_path)):
            #
            # oops! apparently the data file isn't there, we'll have to
            # deal with that. for now just raise and exception and punt...
            #
            raise AnomalyDetectorError(f"can not find {stats_file_path}")
        #
        # the data was found so we'll load a copy of it...
        #
        if (self.debug):
            print(f"...loading stats_file_path")
        self.load()
        if (debug):
            print(self)

    def __repr__(self):
        """Returns the string representation that appears in the REPL
        """
        self.context = "repl"
        return (
            "<AnomalyDetector"
            + f"\n    context = '{self.context}',"
            + f"\n    stats_file_path = '{self.stats_file_path}',"
            + f"\n    verbose = '{self.verbose}',"
            + f"\n    debug = '{self.debug}',"
            + f"\n    metrics = '{type(self.metrics)}',"
            + f"\n    anomaly_threshold_internal = '{self.anomaly_threshold_internal}',"
            + f"\n    anomaly_threshold_external = '{self.anomaly_threshold_external}',"
            + f"\n/>"
        )

    def __str__(self):
        """Returns the string representation that appears in print(...) 
        statements
        """
        self.context = "print"
        return (
            "<AnomalyDetector"
            + f" context = '{self.context}',"
            + f" stats_file_path = '{self.stats_file_path}',"
            + f" verbose = '{self.verbose}',"
            + f" debug = '{self.debug}',"
            + f" metrics = '{type(self.metrics)}',"
            + f" anomaly_threshold_internal = '{self.anomaly_threshold_internal}',"
            + f" anomaly_threshold_external = '{self.anomaly_threshold_external}'"
            + " />"
        )
    
    def load(self):
        """Load the anomaly metrics
        """
        if (self.debug):
            print(f"...self.load()")
        if (self.verbose or self.debug):
            bt = time.time()
        try:
            #
            # attempt to load the file...
            #
            self.metrics = dill.load(gzip.open(self.stats_file_path, "rb"))
        except Exception as oops:
            #
            # some problem occurred
            #
            raise AnomalyDetectorError(
                (f"{stats_file_path} exists, but we couldn't load it"
                 + f" -- the error was {oops}"))
        if (self.verbose or self.debug):
            et = time.time()
            print(f"...loaded {self.stats_file_path} in {round(et - bt, 3)} secs")
        return None

    def dump(self):
        """Save the anomaly metrics
        """
        if (self.debug):
            print(f"...self.dump()")
        if (self.verbose or self.debug):
            bt = time.time()
        try:
            #
            # attempt to save the file (use a temporary name until we have
            # confirmed that the attempt succeeded)...
            #
            new_path = self.stats_file_path + "_new"
            dill.dump(self.metrics, gzip.open(tmp_path, "wb"))
        except Exception as oops1:
            #
            # some problem occurred...
            #
            raise AnomalyDetectorError(
                (f"in attempting to save {self.stats_file_path}, we failed"
                 + f" -- the error was {oops1}"))
        try:
            #
            # we succeeded, so rename the file and we keep a backup copy
            # of the last known good metrics file...
            backup = self.stats_file_path + "_backup"
            if (os.path.exists(backup)):
                os.remove(backup)
            else:
                os.rename(self.stats_file_path, backup)
            os.rename(self.new_path, self.stats_file_path)
        except Exception as oops2:
            raise AnomalyDetectorError(
                (f"in attempting to save {self.stats_file_path} and create"
                 + f" the backup {backup} we failed"
                 + f" -- the error was {oops2}"))
        if (self.verbose or self.debug):
            et = time.time()
            print(f"...saved {self.stats_file_path} in {round(et - bt, 3)} secs")
        return None

    def update(self):
        return None

if (__name__ == "__main__"):
    """
    """
    print("\nsmoke test for AnomalyDetector and AnomalyDetectorError")
    #
    # fetch population data...
    #
    anomaly = AnomalyDetector()
    
