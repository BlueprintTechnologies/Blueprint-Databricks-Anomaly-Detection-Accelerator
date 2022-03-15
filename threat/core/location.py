#!/usr/bin/env python
"""
Created on Tuesday, March 15, 2022 at 13:34:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-15 16:43:51 wcobb>
 
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
import requests, json, urllib.request
#
# threat specific imports...
#
import threat
from threat.core import places
from threat.core import excluding
from threat.core import Latitude, Longitude

class LocationError(Exception):
    pass

class Location:
    def __init__(self, verbose = False):
        """
        A class for managing the acquisition of information about
        people's locations based on their IP addresses
        
        @TODO please improve this documentation

        """
        self.verbose = verbose

    def find(self, ipaddr:str) -> {}:
        """
        given an IP address, search for information about the location
        associated with it.

        @TODO please improve this documentation

        """
        #
        # super trivial case: ip-api.com
        #
        search = f"http://ip-api.com/json/{ipaddr}"
        request = urllib.request.Request(search)
        response = urllib.request.urlopen(request).read()
        info = json.loads(response.decode("utf-8"))
        #
        # the information in from ip-api.com is quite sketchy...
        #
        return info

    def __str__(self):
        """
        @TODO: please improve this documentation

        """
        return "<Location />"

    def __repr__(self):
        """
        @TODO: please improve this documentation

        """
        return self.__str__()

