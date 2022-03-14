#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 12:34:30 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-14 14:19:15 wcobb>
 
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

def excluding(some_list:[str], droppit:[str] = None, debug = False, logger = None):
    """
    """
    if (len(some_list) == 0) or (some_list == []) or (type(some_list) != type([""])) :
        raise RuntimeError(f"null list 'some_list' sent to excluding(...)")
    
    if (len(droppit) == 0) or (droppit == []) or (type(droppit) != type([""])):
        raise RuntimeError(f"bad list 'droppit' send to excluding(...)")

    # still here so we're good..
    keeper = []
    for this_item in some_list:
        keep_this = True
        for drop_this in droppit:
            if (drop_this in this_item):
                keep_this = False
        if (keep_this):
            keeper.append(this_item)
    
    return keeper


    
