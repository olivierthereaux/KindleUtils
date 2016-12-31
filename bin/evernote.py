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
import re
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
evernote.py - Parse and sync kindle clippings into evernote (Mac)

Usage: 
    evernote.py [file]
Options:
    file (optional) - location of Kindle clippings file.
                      Not needed if the Kindle is plugged in
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def ParseKindleDate(date_string):
    # OMG THIS CODE WILL STOP WORKING IN 2100! I hope Amazon will fix their dates before that!
    date_string = re.sub(r", (\d) ", r", 0\1 ", date_string) # if day is 8 instead of 08
    date_string = re.sub(r" (\d\d) (\d\d:)", r" 20\1 \2", date_string) # if year is 13 instead of 2013 
    return time.strptime(date_string.strip(), '%A, %d %B %Y %H:%M:%S') # Saturday, 23 February 2013 17:56:26

def DateLastSync():
    cmd = '''osascript<<END 
    tell application "Evernote"
	set theNotes to every note in notebook "Kindle"
	set theLastNote to beginning of theNotes
	set theDate to creation date of theLastNote
	do shell script "echo " & quote & theDate & quote
end tell
END'''
    return ParseKindleDate(os.popen(cmd).read())    


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
    os.system(cmd)
    time.sleep(1) # Be gentle 


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error as msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
    
    except Usage as err:
        print(sys.argv[0].split("/")[-1] + ": " + str(err.msg), file=sys.stderr)
        print("\t for help use --help", file=sys.stderr)
        return 2
    if len(args) > 0:
        clippings_file = args[0]
    else:
        clippings_file = None

    last_sync_date = DateLastSync()
    clippings = clipping.loadcatalog(clippings_file)
    for clip in clippings:
        clipdate = ParseKindleDate(clip.date)
        # print clip.title.encode("utf-8"), clip.date.encode("utf-8"), last_sync_date
        if  clipdate > last_sync_date:
            # print "yes"
            MakeEvernoteNote(clip)
        else:
            # print "no"
            pass

if __name__ == "__main__":
    sys.exit(main())

