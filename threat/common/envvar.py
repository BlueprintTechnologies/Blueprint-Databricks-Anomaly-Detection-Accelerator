#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:30:21 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-21 10:01:38 wcobb>
 
"""
import os

def envvar(symbolic_name:str, default:str = ".") -> str:
    """
    Wrapper method to facilitate fetching environment variables in a
    somewhat less cumbersome fashion.

    @TODO: please improve this documentation
    """
    try:
        value = os.environ[symbolic_name]
    except:
        value = default
        print(f"'{symbolic_name}' does not exist, using '{value}' instead")
    return value

