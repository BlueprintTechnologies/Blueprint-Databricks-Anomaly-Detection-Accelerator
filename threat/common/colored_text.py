#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:29:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:30:10 wcobb>
 
"""
import os, sys, dill, gzip, time

def colored_text(plain, fgd="", bgd=""):
    """
    Small routine that wraps an input text string 'plain'
    with ANSI color codes and produces 'colored' text.

    @TODO: please improve this documentation

    """
    
    fcolor = {"black":  u"\u001b[30m",
              "red":    u"\u001b[31;1m",
              "yellow": u"\u001b[33;1m",
              "green":  u"\u001b[32;1m",
              "cyan":   u"\u001b[36;1m",
              "blue":   u"\u001b[34;1m",
              "magenta":u"\u001b[35;1m",
              "white":  u"\u001b[37;1m",
              "reset":  u"\u001b[0m",
             }

    bcolor = {"black":  u"\u001b[40m",
              "red":    u"\u001b[41;1m",
              "yellow": u"\u001b[43;1m",
              "green":  u"\u001b[42;1m",
              "cyan":   u"\u001b[46;1m",
              "blue":   u"\u001b[44;1m",
              "magenta":u"\u001b[45;1m",
              "white":  u"\u001b[47;1m",
              "reset":  u"\u001b[0m",
             }

    if ((fgd != "") and (bgd != "")):
        colored = ("%s%s%s%s%s" %
                       (fcolor[fgd], bcolor[bgd], plain,
                        fcolor["reset"], bcolor["reset"]))
        return colored
    elif ((fgd == "") and (bgd != "")):
        colored = ("%s%s%s" %
                       (bcolor[bgd], plain, bcolor["reset"]))
        return colored
    elif ((fgd != "") and (bgd == "")):
        colored = ("%s%s%s" %
                       (fcolor[fgd], plain, fcolor["reset"]))
        return colored
    else:
        return plain

def black(x, bgd=''):
    """
    Trivial little function for creating black text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='yellow', bgd = bgd)

def red(x, bgd=''):
    """
    Trivial little function for creating red text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='red', bgd = bgd)

def yellow(x, bgd=''):
    """
    Trivial little function for creating yellow text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='yellow', bgd = bgd)

def green(x, bgd=''):
    """
    Trivial little function for creating green text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='green', bgd = bgd)

def cyan(x, bgd=''):
    """
    Trivial little function for creating cyan text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='cyan', bgd = bgd)

def blue(x, bgd=''):
    """
    Trivial little function for creating blue text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='blue', bgd = bgd)

def magenta(x, bgd=''):
    """
    Trivial little function for creating magenta text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='magenta', bgd = bgd)

def white(x, bgd=''):
    """
    Trivial little function for creating white text with
    and optional background specified by one of: ['black',
    'red', 'yellow', 'green', 'cyan', 'blue', 'magenta',
    'white'']

    """
    return colored_text(x, fgd='white', bgd = bgd)


    
if (__name__ == "__main__"):
    """
    """
    print("")                # c o l o r e d  t e x t !
    print("Trivial example of %s%s%s%s%s%s%s %s%s%s%s%s" %
              (colored_text("c","red"),
               colored_text("o","yellow"),
               colored_text("l","green"),
               colored_text("o","cyan"),
               colored_text("r","blue"),
               colored_text("e","magenta"),
               colored_text("d","red","yellow"),
               colored_text("t","green","cyan"),
               colored_text("e","magenta","red"),
               colored_text("x","yellow","green"),
               colored_text("t","cyan","magenta"),
               colored_text("!","black","red"),))

    
