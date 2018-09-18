#!/usr/bin/env python

import hashlib
import sys

def midiURL(midifile):
    hash = hashlib.md5(open(midifile, 'rb').read()).hexdigest()
    return "http://purl.org/midi-ld/pattern/{}".format(hash)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: midi-ld-url.py <input_midi_file>"
        exit(1)
    print midiURL(sys.argv[1])
