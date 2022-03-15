#!/usr/bin/env python
"""
Created on Tuesday, March 15, 2022 at 13:34:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-15 16:43:39 wcobb>
 
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
import numpy as np
#
# threat specific imports...
#
import threat
from threat.core import places
from threat.core import excluding

class MapCoordinateError(Exception):
    pass

class MapCoordinate:

    def __init__(self,
                 kind:str,
                 hemi:str,
                 degs:int,
                 mins:int,
                 secs:float,
                 verbose:bool = False,
                ):
        """

        @TODO please improve this documentation

        """
        VALID_KINDS     = ["lat", "lon"]
        VALID_LAT_HEMIS = ["N", "S"]
        VALID_LON_HEMIS = ["E", "W"]
        VALID_LAT_DEGS  = [0.0, 90.0]
        VALID_LON_DEGS  = [0.0, 180.0]
        VALID_MINS      = [0, 60]
        VALID_SECS      = [0, 60]
        #
        #
        #
        self.verbose = verbose
        #
        # sanity check kinds of MapCoordinate
        #
        if (kind not in VALID_KINDS):
            raise MapCoordinateError(f"bad argument 'kind' = '{kind}'")
        self.kind = kind
        #
        # sanity check hemisphere values
        #
        if ((len(hemi) != 1) or
            ((hemi not in VALID_LAT_HEMIS) and (hemi not in VALID_LON_HEMIS))):
            raise MapCoordinateError(f"bad argument 'hemi' = '{hemi}'")
        self.hemi = hemi
        #
        # sanity check the combination...
        #
        if (((kind == "lat") and (hemi not in VALID_LAT_HEMIS)) or
            ((kind == "lon") and (hemi not in VALID_LON_HEMIS))):
            raise MapCoordinateError(f"inconsistent 'kind' and 'hemi' values")
        #
        # check numerical value for degs...
        #
        if ((self.kind == "lat") and
            ((degs < VALID_LAT_DEGS[0]) or (degs > VALID_LAT_DEGS[1]))):
            raise MapCoordinateError(f"bad argument 'degs' = '{degs}'")
        if ((self.kind == "lon") and
            ((degs < VALID_LON_DEGS[0]) or (degs > VALID_LON_DEGS[1]))):
            raise MapCoordinateError(f"bad argument 'degs' = '{degs}'")
        self.degs = degs
        #
        # check numerical value for mins...
        #
        if ((mins < VALID_MINS[0]) or (mins > VALID_MINS[1])):
            raise MapCoordinateError(f"bad argument 'mins' = '{mins}'")
        self.mins = mins
        #
        # check numerical value for secs...
        #
        if ((secs < VALID_SECS[0]) or (secs > VALID_SECS[1])):
            raise MapCoordinateError(f"bad argument 'secs' = '{secs}'")
        self.secs = secs
        #
        # when chatty then show what we have...
        #
        if (verbose):
            print(f"{self.__str__()}")

    def asfloat(self):
        """
        """
        factor = 1
        if (self.kind == "lat"):
            if (self.hemi == "S"):
                factor = -1
        elif (self.kind == "lon"):
            if (self.hemi == "W"):
                factor = -1
        result = factor * (self.degs + (60 * self.mins + self.secs)/3600)
        return round(result, 6)
                
    def __str__(self):
        """
        @TODO: please improve this documentation

        """
        test = (f"{self.hemi}"+
                f"{self.degs}d"+
                f"{self.mins}m"+
                f"{round(self.secs, 2)}s")
        return test

    def __repr__(self):
        """
        @TODO: please improve this documentation

        """
        return self.__str__()

class Latitude(MapCoordinate):
    def __init__(self, hemi, degs, mins, secs, verbose = False):
        super().__init__("lat", hemi, degs, mins, secs, verbose = verbose)

class Longitude(MapCoordinate):
    def __init__(self, hemi, degs, mins, secs, verbose = False):
        super().__init__("lon", hemi, degs, mins, secs, verbose = verbose)

