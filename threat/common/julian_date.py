#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:31:02 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:31:03 wcobb>
 
"""
import time
import numpy as np
import jdcal

def jdd() -> float:
    now = time.gmtime()
    (jdbase, mjd) = jdcal.gcal2jd(now.tm_year, now.tm_mon, now.tm_mday)
    dayfrac = float((now.tm_hour + now.tm_min/60.00 + now.tm_sec/3600.0)/24.0)
    jdate = float(jdbase) + float(mjd) + dayfrac
    return jdate

def jds() -> str:
    jds = ("%.7lf" % jdd())
    return jds

    
