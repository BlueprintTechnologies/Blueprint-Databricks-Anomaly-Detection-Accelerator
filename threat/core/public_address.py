#!/usr/bin/env python
"""
Created on Thursday, March 17, 2022 at 08:30:43 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-17 08:38:05 wcobb>
 
"""

def public_address(ipaddr) -> bool:
    """
    Small function for identifying whether an IP address is 'public'
    (as opposed to 'private')

    """
    private_starts = [
        "10.", "192.168", "172.16.", "172.17.", "172.18.", "172.19.",
        "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
        "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.",
    ]
    for test in private_starts:
        if (ipaddr.startswith(test)):
            return False
    return True

if (__name__ == "__main__"):
    print("")
    print(public_address("10.11.12.13"))
    print(public_address("192.168.1.1"))
    print(public_address("172.26.164.67"))
    
