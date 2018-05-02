# The Semantic Web MIDI Tape

A Read/Write RESTful Interface for Publishing MIDI as Linked Data

## What is this?

The Semantic Web MIDI Tape is a set of tools and associated RESTful API to stream MIDI as RDF triples, serialize them, attach additional metadata to them, upload/download them to a SPARQL endpoint, and play them back. The set of tools is available [in this repo](src/) and the [RESTful API](http://grlc.io/api/midi-ld/queries) is generated from [these SPARQL queries](https://github.com/midi-ld/queries) using [grlc](https://github.com/midi-ld/queries).

## Requirements and install

You'll need an input MIDI instrument (or virtual device) and a POSIX system with Python 2.7. To install requirements, clone this repository and do

``$ pip install -r requirements.txt``

## Usage example



``python swmiditp-stream.py``

``python swmiditp-stream.py > myperformance.nt # The last line of output in stderr will give you a link to your MIDI RDF performance http://purl.org/midi-ld/pattern/example``

``./swmiditp-upload.sh http://virtuoso-midi.amp.ops.labs.vu.nl/none myperformance.nt # This is any named graph you want to load the triples into``

--Open link in browser

``./swmiditp-download.sh http://purl.org/midi-ld/pattern/example > myperformance.ttl``
``python rdf2midi.py myperformance.ttl myperformance.mid``
``timidity myperformance.mid``
