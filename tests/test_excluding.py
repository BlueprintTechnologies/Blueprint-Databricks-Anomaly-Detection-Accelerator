#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 12:59:56 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-14 14:32:14 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip

import threat
from threat.core import places, excluding

if (__name__ == '__main__'):
    """
    my program
    
    @TODO Please Improve This Documentation!
    """
    passed = 0
    failed = 0
    raw_list = ["A", "B", "C", "D", "A.zip", "B.elc", "C.dill", "D.snark" ]
    drp_list = [".zip", ".elc", ".dill", ".snark"]
    t01 = excluding(raw_list, droppit = drp_list)
    flt_list = ["A", "B", "C", "D"]
    #
    # the first test...
    #
    if (t01 == flt_list):
        passed += 1
    else:
        failed += 1
        print("failed test 't01'")
    #
    # the second test...
    #
    try:
        t02 = excluding(raw_list, droppit = ".zip")
    except:
        passed += 1
    else:
        failed += 1
        print("failed test 't02'")
    #
    # the third test...
    #
    try:
        t03 = excluding("", droppit = drp_list)
    except:
        passed += 1
    else:
        failed += 1
        print("failed test 't03'")
    #
    # now print out the results...
    #
    print(f"{passed},{failed}")
