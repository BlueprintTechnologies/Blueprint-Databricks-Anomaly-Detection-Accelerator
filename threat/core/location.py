#!/usr/bin/env python
"""
Created on Tuesday, March 15, 2022 at 13:34:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-16 14:24:19 wcobb>
 
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

def find_location(ipaddr:str) -> {}:
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
    location = json.loads(response.decode("utf-8"))
    #
    # the information in from ip-api.com *can* be quite good
    # but if the ORG is the same as the ISP then it's probably
    # only giving us the ISP's physical location information...
    #
    if (location["isp"] != location["org"]):
        location["trust"] = True
    else:
        location["trust"] = False
    return location

def find_country(ipaddr:str) -> str:
    # country determinations are > 99.8% reliable
    location = find_location(ipaddr)
    return location["countryCode"]

def find_region(ipaddr:str) -> str:
    location = find_location(ipaddr)
    return location["region"]

def find_city(ipaddr:str) -> str:
    location = find_location(ipaddr)
    return location["city"]

def find_latlon(ipaddr:str) -> (float, float):
    location = find_location(ipaddr)
    return (location["lat"], location["lon"])


