#!/usr/bin/env python
"""
Created on Tuesday, March 15, 2022 at 13:34:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-16 13:14:09 wcobb>
 
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

if (__name__ == "__main__"):
    print("")
    address  = "184.62.211.87"
    answer   = find_location(address)
    countryCode = info["countryCode"]
    print(f"ip-addr '{address}' comes from country-code '{countryCode}' (greater than 90% confidence)")
    isp      = info["isp"]
    org      = info["org"]
    f32lat   = info["lat"]
    f32lon   = info["lon"]
    city     = info["city"]
    region   = info["region"]
    zipcode  = info["zip"]
    timezone = info["timezone"]
    if (isp == org):
        #
        # then this is probably an ISP (which means the
        # other information is probably valid only for the
        # provider itself and not the end user)
        #
        print(f" * block owned by ISP '{isp}' based in {city}, {region} {zipcode}")
        print(f" * the ISP has lat: '{f32lat}', lon: '{f32lon}' and is in timezone '{timezone}'")
    else:
        #
        # provider != company so there is a good chance that this is a legit address
        #
        print(f" * the ip-address appears to be located in {city}, {region} {zip}")
        print(f" * the addr has lat: {f32lat}, lon: {f32lon} and is in timezone '{timezone}'")
        
