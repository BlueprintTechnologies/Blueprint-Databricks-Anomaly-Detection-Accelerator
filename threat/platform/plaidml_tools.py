#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:27:03 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:27:04 wcobb>
 
"""
import os, sys, dill, gzip, time
import pandas as pd
import numpy as np

##
## this adapts your run-time environment to what is appropriate
##
def config_plaidml_runtime(verbose=False):
    if (verbose):
        print("configure_plaidml_runtime:")
    os.environ["PYTHON_ROOT"] = "/usr" # default value on most unix clones
    items = list(sys.path)
    for item in items:
        this_python = ("python%d.%d" % (sys.version_info.major, sys.version_info.minor))
        if (verbose):
            print("...testing '%s' for '%s'" % (item, this_python))
        if (item.endswith(this_python)):
            if (verbose):
                print("...found '%s' in '%s'" % (this_python, item))
            os.environ["PYTHON_ROOT"] = item.replace(os.path.join("lib", this_python), "")
            break
    if (sys.platform == "darwin"):
        os.environ["PLAIDML_NATIVE_PATH"] = os.path.join(os.environ["PYTHON_ROOT"], "lib", "plaidml.dylib")
    elif (sys.platform == "linux"):
        os.environ["PLAIDML_NATIVE_PATH"] = os.path.join(os.environ["PYTHON_ROOT"], "lib", "libplaidml.so")
    else:
        raise RuntimeError(("...unrecognized environment"))
    os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
    os.environ["RUNFILES_DIR"] = os.path.join(os.environ["PYTHON_ROOT"], "share", "plaidml")
    os.environ["PLAIDML_NATIVE_PATH"] = os.path.join(os.environ["PYTHON_ROOT"], "lib", "libplaidml.so")
    os.environ["PLAIDML_USE_STRIPE"] = "1"
    if (verbose):
        print("...PYTHON_ROOT         = '%s'" % os.environ["PYTHON_ROOT"])
        print("...KERAS_BACKEND       = '%s'" % os.environ["KERAS_BACKEND"])
        print("...RUNFILES_DIR        = '%s'" % os.environ["RUNFILES_DIR"])
        print("...PLAIDML_NATIVE_PATH = '%s'" % os.environ["PLAIDML_NATIVE_PATH"])
        print("...PLAIDML_USE_STRIPE  = '%s'" % os.environ["PLAIDML_USE_STRIPE"])
    return None

