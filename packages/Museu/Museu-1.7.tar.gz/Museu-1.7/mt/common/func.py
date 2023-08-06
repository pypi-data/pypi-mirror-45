#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-26 09:15:03
# @Author  : Blackstone
# @to      :

def dot_name_to_object(name):
    """Resolve a dotted name to a global object."""
    name = name.split('.')
    used = name.pop(0)
    #print(name)
    #print(used)
    found = __import__(used)
   # print(found)
    for n in name:
    	
        used = used + '.' + n

        #print("used=>",used)
        try:
            #print("found=>",found)
           # print("n=>",n)
            found = getattr(found, n)
            #print("found=>",found)
        except AttributeError:
            __import__(used)
            found = getattr(found, n)


    return found