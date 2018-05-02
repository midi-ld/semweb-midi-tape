#!/bin/bash

# play-midi-ld.sh: Downloads a MIDI of the MIDI LD cloud by URI

if [ $# -eq 0 ]
  then
    echo "Usage: swmiditp-download.sh <midi-ld-uri>"
    exit 0
fi


curl -s -X GET -G --header "Accept: text/turtle" "http://grlc.io/api/midi-ld/queries/pattern_graph" --data-urlencode "pattern=$1"
# ./rdf2midi.py api.ttl api.mid
# timidity api.mid
# rm api.mid
