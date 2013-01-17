#!/usr/bin/env python
# encoding: utf-8
"""
evernote.py

Parse kindle clippings into evernote (Mac)

Based upon gist by Joost Plattel
http://www.jplattel.nl/kindle-notes-evernote-sync/
and subsequently cleaned up & extended.

Created by Olivier Thereaux on 2013-01-16.
"""

import os
import time
import sys
import getopt
from os.path import join, dirname, exists, realpath

# The library in ../lib/ has some classes and helpers
source_tree_lib = join(dirname(__file__), "..", "lib", "clipping.py")
if exists(source_tree_lib):
    sys.path.insert(0, dirname(source_tree_lib))
    try:
        import clipping
    finally:
        del sys.path[0]
else:
    import clipping



help_message = '''
evernote.py - Parse kindle clippings into evernote (Mac)

Usage: 
    evernote.py [file]
Options:
    file (optional) - location of Kindle clippings file.
                      Not needed if the Kindle is plugged in
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def MakeEvernoteNote(clip):
    """given a clipping, see if it has already been saved, and if not, save it to the Evernote notebook "Kindle"."""
    cmd = '''osascript<<END 
    tell application "Evernote" 
        if (not (notebook named "Kindle" exists)) then
    		create notebook "Kindle"
    	end if
    	if ((count of (find notes "'''+ clip.title.encode("utf-8") +" "+ clip.location.encode("utf-8")+" "+'''")) = 0) then
        set clip to create note title "'''+ clip.title.encode("utf-8") + "(" +clip.author.encode("utf-8") +") -- " + clip.date.encode("utf-8") + '''" notebook "Kindle" with text "'''+ clip.text.encode("utf-8") + "\n" + clip.location.encode("utf-8") + '''"
    	end if
    end tell 
END'''
    print cmd
    print
    # os.system(cmd)



def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2
    if len(args) > 0:
        clippings_file = args[0]
    else:
        clippings_file = None

    clippings = clipping.loadcatalog(clippings_file)
    for clip in clippings:        
        MakeEvernoteNote(clip)
        time.sleep(3) # need to wait a fair amount 
                      # or Evernote will not "find" the existing notes and just create duplicates
                      # TODO - report bug to Evernote

if __name__ == "__main__":
    sys.exit(main())

