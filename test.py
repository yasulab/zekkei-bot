#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import string

"""
zen = "@tango_bot　おにぎり"
han = "@tango_bot おにぎり"
#print han.lstrip("@tango_bot").lstrip()
#print zen.lstrip("@tango_bot").lstrip()
print string.replace(zen, "　", " ").lstrip("@tango_bot").lstrip()
print string.replace(han, "　", " ").lstrip("@tango_bot").lstrip()
"""

i = 1
tweet = "sthとsth"
while "sth" in tweet:
    tweet = string.replace(tweet, "sth",  "何か"+str(i) , 1)
    i += 1
print tweet

