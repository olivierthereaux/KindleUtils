#!/usr/bin/env python
# encoding: utf-8
"""
clipping.py

python library to manipulate Kindle clippings

Based upon gist by Joost Plattel
http://www.jplattel.nl/kindle-notes-evernote-sync/
and subsequently cleaned up & extended.

Created by Olivier Thereaux on 2013-01-16.
"""

import sys
import os
import re
import unittest
from os.path import join, dirname, exists

class Clipping(object):
    title = None
    author = None
    date = None
    text = None
    location = None
    
    def __init__(self):
		super(Clipping, self).__init__()
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __unicode__(self):
        # return u"%r" % self.__dict__
        return u"%r" % self.todict()

    def __str__(self):
        return "%r" % self.todict()

    def todict(self):
        dict_entry = dict()
        if self.title != None:
            dict_entry["Title"] = self.title
        if self.author != None:
            dict_entry["Author"] = self.author
        if self.date != None:
            dict_entry["Date"] = self.date
        if self.text != None:
            dict_entry["Text"] = self.text
        if self.location != None:
            dict_entry["Location"] = self.location
        return dict_entry
    


class ClippingTests(unittest.TestCase):
	def setUp(self):
		pass

def loadcatalog(clippings_file=None):
    clippings = list()
    if clippings_file == None: # see if the Kindle is mounted and grab the file from there
        if exists("/Volumes/Kindle/documents/"):
            clippings_file = join("/Volumes/Kindle/documents/", "My Clippings.txt")
        else:
            sys.exit("no clippings file provided, and Kindle not found")
    try:
        clippings_fh = open(clippings_file ,"r")
    except Exception, e:
        sys.exit("Could not load clippings file: %s" % e)
    data = "".join(clippings_fh.readlines()).decode("utf-8")
    data = data.replace(u"\ufeff", "") # remove bunch of ZERO WIDTH NO-BREAK SPACE
    clippings = list()
    raw_clippings = data.split('==========')
    for clip in raw_clippings:
        if re.search("Your Highlight", clip):
            clipping_meta, clipping_text = clip.split('\r\n\r\n')
            title_author, location_date = clipping_meta.split('\r\n- ')
            try:
                title, author = title_author.replace('\r\n','').split("(")
            except ValueError:
                title = title_author
                author = ""
            author = author.replace(")", "")
            location, date = location_date.split('| Added on ')
            clipping = Clipping()
            clipping.title=title
            clipping.author=author
            clipping.date=date
            clipping.text=clipping_text
            clipping.location=location
            clippings.append(clipping)
    #         try:
    # except Exception, e:
    #     sys.exit("Error while loading clippings file: %s" % e)

    return clippings


if __name__ == '__main__':
	unittest.main()