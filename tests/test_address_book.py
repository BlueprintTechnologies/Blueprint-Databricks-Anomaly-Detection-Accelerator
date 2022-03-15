#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 16:07:38 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-15 14:58:18 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip

import threat
from threat.core import places
from threat.core import excluding
from threat.core import location
from threat.core import Address


class GeoCacheError(Exception):
    """
    @TODO: please improve this documentation
    
    """
    pass

class GeoCache:
    """
    @TODO: please improve this documentation
    
    """
    def __init__(geo_cache_name = "geo_cache.dill",
                 overwrite = False,
                 verbose = False,
                 logger = None,
                 debug = False,
                ):
        """
        Initiator for the GeoCache class.


        @TODO: please improve this documentation

        """
        self.data_path = os.path.join(places("datasets"), locations_name)
        self.overwrite = overwrite
        self.verbose = verbose
        self.logger = logger
        self.debug = debug

        data_exists = os.path.exists(self.data_path)
        if (not data_exists) or (self.overwrite):
            self.ip_data = {}
            self.mac_data = {}
            self.dump()
        else:
            self.load()

    def __get(self, ip):
        """
        Attempts to find the location data for an ip address via various network sources
        and services.

        @TODO: please improve this documentation

        """
        return None

    def __save(self, ip = None, mac = None, country = None, country_code = None,location_data):
        """
        Adds a new record to the geo_cache

        @TODO: please improve this documentation

        """
        self.__update_keys()
        return None

    def __update_keys(self):
        """
        Updates the key information from the cache

        @TODO: please improve this documentation

        """
        self.ip_keys = list(self.ip_data.keys())
        self.mac_keys = list(self.mac_data.keys())
        return None
        
    def find(self, ip = None, mac = None):
        """
        Searches for an IP address in the geo_cache. If the requested ip is not found
        then an attempt will be made to discover the relevant information from network 
        sources.  If data is found, then it will be added to the GeoCache.

        @TODO: please improve this documentation

        """
        if (ip == None) and (mac == None):
            message = f"ip and mac should not both be None"
            raise GeoCacheError(message)
        elif (ip != None):
            # so we search by ip...
            if (self.logger != None):
                logger.debug("searching by ip")
            
        elif (mac != None):
            # so we search by mac...
            if (self.logger != None):
                logger.debug("searching by mac")
                
        return None

    def load(self):
        """
        @TODO: please improve this documentation

        """
        (self.ip_data, self.mac_data) = dill.dump(open(self.data_path, "rb"))
        return None

    def dump(self):
        """
        @TODO: please improve this documentation

        """
        dill.dump((self.ip_data, self.mac_data), open(self.data_path, "wb"))
        return None

    def __str__(self):
        """
        @TODO: please improve this documentation

        """
        return "<GeoCache />"

    def __repr__(self):
        """
        @TODO: please improve this documentation

        """
        return __str__()



    



