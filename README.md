# The Semantic Web MIDI Tape

The swmiditp is a read/write RESTful interface for publishing MIDI as Linked Data

## What is this?

The Semantic Web MIDI Tape is a set of tools and associated RESTful API to stream MIDI as RDF triples, serialize them, attach additional metadata to them, upload/download them to a SPARQL endpoint, and play them back. The set of tools is available [in this repo](src/) and the [RESTful API](http://grlc.io/api/midi-ld/queries) is generated from [these SPARQL queries](https://github.com/midi-ld/queries) using [grlc](https://github.com/midi-ld/queries).

## Requirements and install

You'll need an input MIDI instrument (or virtual device) and a POSIX system with Python 2.7. To install requirements, clone this repository and do

``$ pip install -r requirements.txt``

## Usage example

The first thing you can do with swmiditp is to generate a live stream of RDF triples as you play along your MIDI instrument. Make sure your device is plugged in an recognized by your system. Then, move to ``src/`` and do

``python swmiditp-stream.py``

There is an interactive menu to guide you through the tool. The first thing is to select the input MIDI device you want to use from a list (if your's isn't there, make sure your system recognizes it). Simply type the device number and hit enter. After this, you'll see some basic metadata in RDF on screen, and if you start playing your MIDI device, you should see a stream RDF triples representing exactly your performance. You can hit Ctrl-C at any time to stop. This will trigger a few questions about the metadata you want to attach to your performance (such as your FOAF profile, links to the composer, etc.).

All interactions are redirected to ``stderr``, which means that you can always redirect the output of ``swmiditp-stream.py`` to a file and you'll get a syntactically valid RDF NTriples file:

``python swmiditp-stream.py > myperformance.nt``

 When you hit Ctrl-C to stop playing, the system will provide you a URI link to your MIDI RDF performance that uniquely identifies it; let's assume that link is http://purl.org/midi-ld/pattern/example and that you've saved your triples in a file called ``myperformance.nt``. Then you can do

``./swmiditp-upload.sh http://virtuoso-midi.amp.ops.labs.vu.nl/none myperformance.nt``

 The first parameter is the URI of the named graph you want to load the triples into (it can be arbitrary but could come in handy if you want to store different performances in different graphs). This will upload your performance in RDF to [the MIDI Linked Data cloud endpoint](http://virtuoso-midi.amp.ops.labs.vu.nl/sparql). You can change that endpoint by cloning [this repo](https://github.com/midi-ld/queries) and specifying your own endpoint in the ``insert_pattern`` query (make sure to edit the API call names in ``src/`` accordingly).

 After a few seconds (depending on how long you played) your performance will be available online in shiny de-referenceable RDF! Just direct your browser to http://purl.org/midi-ld/pattern/example and haven fun surfing the triples with [brwsr](https://github.com/Data2Semantics/brwsr/).

 You can retrieve the RDF of your MIDI performance back anytime with

``./swmiditp-download.sh http://purl.org/midi-ld/pattern/example > myperformance.ttl``

Through the ``rdf2midi`` algorithm of [midi2rdf](https://github.com/midi-ld/midi2rdf) you can convert this back into MIDI, and play it with your favourite synthesizer:

``python rdf2midi.py myperformance.ttl myperformance.mid``
``timidity myperformance.mid``
