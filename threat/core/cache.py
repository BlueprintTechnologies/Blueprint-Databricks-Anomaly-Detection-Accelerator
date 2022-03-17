#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 16:07:38 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-16 21:15:17 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip
import numpy as np

import threat
from threat.core import places
from threat.core import excluding
from threat.core import find_location

class CacheError(Exception):
    pass

class Cache:
    def __init__(self,
                 cache_name:str = "cache.dill",
                 overwrite:bool = False,
                 verbose:bool = False,
                 debug:bool = False,
                 threshold:int = 100,
                ):
        """
        """
        self.overwrite = overwrite
        self.verbose = verbose
        self.debug = debug
        self.threshold = threshold
        self.record_count = 0
        self.data_path = os.path.join(places("datasets"), cache_name)

        if (os.path.exists(self.data_path)) and (not self.overwrite):
            self.load()
            
        if (not os.path.exists(self.data_path)) or (self.overwrite):
            if (os.path.exists(self.data_path)):
                os.remove(self.data_path)
            self.data = {}

    def search(self, ipaddr:str):
        if (not ipaddr in self.data.keys()):
            if (self.verbose) or (self.debug):
                print(f"we haven't seen {ipaddr} before, looking for it...")
            #
            # well we haven't seen this one before so look it up...
            #
            self.data[ipaddr] = find_location(ipaddr)
            #
            # ...initialize a reference counter...
            #
            self.data[ipaddr]["references"] = 0
        elif ((ipaddr in self.data.keys()) and (self.data[ipaddr]["status"] == "success")):
            if (self.debug):
                print(f"we HAVE seen {ipaddr} before and read it successfully...")
            #
            # just increment the reference counter if we already
            # have a trusted valid read...
            #
            self.data[ipaddr]["references"] += 1
        elif ((ipaddr in self.data.keys()) and (self.data[ipaddr]["status"] != "success")):
            if (self.debug):
                print(f"we HAVE seen {ipaddr} before and but FAILED to read it successfully...")
            #
            # we have seen it before but we have NOT read it successfully, so let's try
            # to read it again...
            #
            test_data = find_location(ipaddr)
            if (test_data["status"] == "success"):
                if (self.debug):
                    print(f"we now have valid data for {ipaddr}, updating")
                #
                # when we get valid data overwrite what was there before...
                #
                for key in test_data.keys():
                    self.data[ipaddr][key] = test_data[key]
        #
        # by now there definitely is a record in hand...
        #
        target = self.data[ipaddr]
        #
        # regardless, update the reference counter...
        #
        self.record_count += 1
        if (self.record_count == self.threshold):
            if (self.debug):
                print(f"have read {self.record_count} addresses, updating cache")
            #
            # save cache to disk every 'self.threshold' records...
            #
            self.record_count = 0
            self.dump()
            self.load()
        #
        # so return it...
        #
        if (self.verbose) or (self.debug):
            message = (f"ipaddr {ipaddr} is from " +
                       f"{target['city']}, " +
                       f"{target['region']}, " +
                       f"{target['countryCode']}")
            print(message)
        return target

    def load(self):
        """
        @TODO: please improve this documentation

        """
        self.data = dill.load(open(self.data_path, "rb"))
        return None

    def dump(self):
        """
        @TODO: please improve this documentation

        """
        dill.dump(self.data, open(self.data_path, "wb"))
        return None

    def __str__(self):
        """
        @TODO: please improve this documentation

        """
        nkeys = len(list(self.data.keys()))
        nobs = np.sum([self.data[key]["references"] for key in self.data.keys()])
        strrep = ("<Cache " +
                  f"\n\tdata_path = {self.data_path}," + 
                  f"\n\toverwrite = {self.overwrite}," + 
                  f"\n\tverbose = {self.verbose}," + 
                  f"\n\tdebug = {self.debug}," + 
                  f"\n\tthreshold = {self.threshold}," + 
                  f"\n\tdata = <dict with {nkeys} unique addresses and {nobs} observations of same>" +
                  f"\n\t\>")
        return strrep

    def __repr__(self):
        """
        @TODO: please improve this documentation

        """
        return __str__()

    


