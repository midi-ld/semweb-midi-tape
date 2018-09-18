#!/bin/bash

# swmiditp-upload.sh: Uploads MIDI LD data to endpoint via RESTful API

if [ $# -lt 3 ]
  then
    echo "Usage: swmiditp-upload.sh <named-graph-uri> <midi-rdf-file> <midi-rdf-uri>"
    exit 0
fi

# curl -s -o /dev/null -X POST -H'Content-Type: application/sparql-update' -d"INSERT DATA { GRAPH <http://virtuoso-midi.amp.ops.labs.vu.nl/none> { $(cat $1) } }" $2
curl -s  -o /dev/null -X POST http://grlc.io/api/midi-ld/queries/insert_pattern -d"g=<$1>" -d"data=$(cat $2)"
curl -s -X GET -G http://tapeapi.amp.ops.labs.vu.nl/ --data-urlencode "perf_uri=$3"
