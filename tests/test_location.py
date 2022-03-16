#!/usr/bin/env python
"""
Created on Tuesday, March 15, 2022 at 13:34:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-16 14:25:59 wcobb>
 
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
from threat.core import find_location
from threat.core import find_country, find_region, find_city, find_latlon 

if (__name__ == "__main__"):
    print("")
    ip_address = "184.62.211.87"
    print(f"{ip_address}:")
    #
    # to find the country... note the difference in the
    #
    country = find_country(ip_address)
    print(f" * is in country '{country}'")
    #
    # to find the region...
    #
    region = find_region(ip_address)
    print(f" * is in region '{region}'")
    #
    # to find the city...
    #
    city = find_city(ip_address)
    print(f" * is in city '{city}'")
    #
    # to find the lat-lon...
    #
    lat, lon = find_latlon(ip_address)
    print(f" * is at lat: '{lat}', lon: '{lon}'")
    #
    # when we are interested in lots of things...
    #
    location = find_location(ip_address)
    print(f"\n{ip_address}:\n {location}")
