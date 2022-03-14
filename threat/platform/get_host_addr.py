#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:25:49 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:25:51 wcobb>
 
"""
import socket

def get_host_addr():
    """
    Absurd hack.

    """
    return ((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                   if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
