#!/usr/bin/env python
"""
Created on Thursday, January 27, 2022 at 14:31:06 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Greenprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-09 09:22:18 wcobb>
 
"""

def is_strict_ascii(foo:str):
    """
    Function that returns True if something is STRICT ASCII and
    False if there are funky characters present.

    @TODO: please improve this documentation

    """
    try:
        foo.encode("ascii", "strict")
        return True
    except:
        return False
    
