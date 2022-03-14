#!/usr/bin/env python
"""
Created on Friday, January 21, 2022 at 09:55:38 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-14 15:27:40 wcobb>
 
"""
import os, sys, time, math

import threat
from threat.core import places

if (__name__ == '__main__'):
    """
    my program
    
    @TODO Please Improve This Documentation!
    """
    passed = 0
    failed = 0

    # t01
    expected_list = sorted(['datasets', 'images', 'masks', 'models',
                            'extras', 'other', 'logfiles'])
    observed_list = sorted(eval(places("?")))
    if (observed_list == expected_list):
        passed += 1
    else:
        failed += 1
        print(f"failed t01")

    def expected_path(key, root = "data", base = "blueprint", proj = "threat"):
        return os.path.join("/", root, base, proj, key)

    # t02_07
    for key in observed_list:
        if (places(key) == expected_path(key)):
            passed += 1
        else:
            failed += 1
            print(f"failed t02_07")

    print(f"{passed},{failed}")

    

