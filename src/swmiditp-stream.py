#!/usr/bin/env python

# swmiditp-stream.py: Stream MIDI RDF triples

import mido
import uuid
from rdflib import Graph, Namespace, RDF, Literal, URIRef
from datetime import datetime
import time
import sys

# if len(sys.argv) < 2:
#     print """\
# Usage: swmiditp-stream.py <midi input device>"""
#     exit(1)

midi_inputs = mido.get_input_names()
sys.stderr.write("swmiditp-stream.py: Stream MIDI RDF triples\n")
sys.stderr.write("Instructions:\n")
sys.stderr.write("1. Type you MIDI input device from the list below and press enter\n")
sys.stderr.write("2. Play your MIDI instrument along\n")
sys.stderr.write("3. When done, press Ctrl-C and you'll get a MIDI pattern identifier\n")
sys.stderr.write("You can redirect the output to a .nt file, e.g. ./swmiditp-stream.py > myplay.nt\n")
sys.stderr.write("\n")
sys.stderr.write("Detected MIDI input devices:\n")
for i in range(len(midi_inputs)):
    sys.stderr.write("[{}] {}".format(i, midi_inputs[i]))
    sys.stderr.write('\n')

try:
    mode = int(raw_input())
except ValueError:
    print "Not a number"
    exit(1)

# midi_input_device = sys.argv[1]
midi_input_device = midi_inputs[mode]

# initialize rdf graph
g = Graph()
# Namespaces
midi_r = Namespace("http://purl.org/midi-ld/")
midi = Namespace("http://purl.org/midi-ld/midi#")
prov = Namespace("http://www.w3.org/ns/prov#")
mo = Namespace("http://purl.org/ontology/mo/")

g.bind('midi-r', midi_r)
g.bind('midi', midi)
g.bind('prov', prov)
g.bind('mo', mo)

# Initialize pattern, track and event IDs
pattern_id = uuid.uuid4()
track_id = 0
event_id = 0

# time counter
start_time = time.time()

# Initialize the MIDI graph
piece = midi_r['pattern/' + str(pattern_id)]
g.add((piece, RDF.type, midi.Piece))
g.add((piece, midi.resolution, Literal(460)))
g.add((piece, midi['format'], Literal(1)))

# We'll set a single track (TODO: support more)
track = URIRef(piece + '/track' + str(track_id).zfill(2))
g.add((track, RDF.type, midi.Track))
g.add((piece, midi.hasTrack, track))

# Testing graph init stuff
# event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(0).zfill(2)]
# g.add((track, midi.hasEvent, event_uri))
# g.add((event_uri, RDF.type, midi.SetTempoEvent))
# g.add((event_uri, midi.bpm, Literal(8.300007e+01)))
# g.add((event_uri, midi.mpqn, Literal(722891)))
# g.add((event_uri, midi.tick, Literal(0)))
#
# event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(1).zfill(2)]
# g.add((track, midi.hasEvent, event_uri))
# g.add((event_uri, RDF.type, midi.TimeSignatureEvent))
# g.add((event_uri, midi.denominator, Literal(4)))
# g.add((event_uri, midi.metronome, Literal(96)))
# g.add((event_uri, midi.numerator, Literal(4)))
# g.add((event_uri, midi.thirtyseconds, Literal(8)))
# g.add((event_uri, midi.tick, Literal(0)))
#
# event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(2).zfill(2)]
# g.add((track, midi.hasEvent, event_uri))
# g.add((event_uri, RDF.type, midi.ControlChangeEvent))
# g.add((event_uri, midi.channel, Literal(0)))
# g.add((event_uri, midi.control, Literal(101)))
# g.add((event_uri, midi.tick, Literal(0)))
# g.add((event_uri, midi.value, Literal(0)))
#
# event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(3).zfill(2)]
# g.add((track, midi.hasEvent, event_uri))
# g.add((event_uri, RDF.type, midi.ProgramChangeEvent))
# g.add((event_uri, midi.channel, Literal(0)))
# g.add((event_uri, midi.tick, Literal(0)))
# g.add((event_uri, midi.program, URIRef("http://purl.org/midi-ld/programs/74")))

# event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(2).zfill(2)]
# g.add((event_uri, midi.channel, Literal(0)))
# g.add((event_uri, midi.control, Literal(101)))
# g.add((event_uri, midi.tick, Literal(0)))
# g.add((event_uri, midi.value, Literal(0)))
# g.add((event_uri, RDF.type, midi.ControlChangeEvent))
# g.add((track, midi.hasEvent, event_uri))

# PROV info
# g.add((piece, prov.wasDerivedFrom, Literal(filename)))
agent = URIRef("https://github.com/midi-ld/midi2rdf")
entity_d = piece
entity_o = URIRef("http://purl.org/midi-ld/file/{}".format(pattern_id))
activity = URIRef(piece + "-activity")

g.add((agent, RDF.type, prov.Agent))
g.add((entity_d, RDF.type, prov.Entity))
g.add((entity_o, RDF.type, prov.Entity))
g.add((entity_o, RDF.type, midi.MIDIFile))
g.add((entity_o, midi.path, Literal(pattern_id)))
g.add((activity, RDF.type, prov.Activity))
g.add((entity_d, prov.wasGeneratedBy, activity))
g.add((entity_d, prov.wasAttributedTo, agent))
g.add((entity_d, prov.wasDerivedFrom, entity_o))
g.add((activity, prov.wasAssociatedWith, agent))
g.add((activity, prov.startedAtTime, Literal(datetime.now())))
g.add((activity, prov.used, entity_o))

print g.serialize(format='nt')

try:
    with mido.open_input(midi_input_device) as port:
        for msg in port:
            sg = Graph()
            status = None
            if msg.type == "note_on":
                status = "NoteOnEvent"
            elif msg.type == "note_off":
                status = "NoteOffEvent"
            else:
                print "BIG ERROR, unexpected event type {}".format(msg.type)
            pitch = msg.bytes()[1]
            velocity = msg.bytes()[2]
            channel = 0
            #print status, pitch, velocity, channel, timestamp
            # Creating triples!
            event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(event_id).zfill(4)]
            sg.add((track, midi.hasEvent, event_uri))
            sg.add((event_uri, RDF.type, midi[status]))
            sg.add((event_uri, midi.tick, Literal(int((time.time() - start_time)*1000))))
            start_time = time.time()
            sg.add((event_uri, midi.channel, Literal(channel)))
            sg.add((event_uri, midi.note, URIRef('http://purl.org/midi-ld/notes/{}'.format(pitch))))
            sg.add((event_uri, midi.velocity, Literal(velocity)))

            print sg.serialize(format='nt')

            # Merge sg with main graph
            g = g + sg

            event_id += 1
except KeyboardInterrupt:
    # Add end of track event
    event_id += 1
    event_uri = midi_r["pattern/" + str(pattern_id) + "/" + 'track' + str(track_id).zfill(2) + '/event' + str(event_id).zfill(4)]
    eg = Graph()
    eg.add((track, midi.hasEvent, event_uri))
    eg.add((event_uri, RDF.type, midi.EndOfTrackEvent))
    eg.add((event_uri, midi.tick, Literal(0)))

    print eg.serialize(format='nt')

    g = g + eg

    # Add metadata
    m = Graph()

    performance_uri = piece # The MIDI URI
    musical_work_uri = None # The URI of which this MIDI is a performance of
    composition_uri = None # The URI of the composition from which the work was produced
    composer_uri = None # The URI of the original artist who composed the work
    performer_uri = None # THe URI of the music artist that did the performance


    sys.stderr.write("Metadata info\n")
    sys.stderr.write("The URI of your performance is:\n")
    sys.stderr.write(URIRef(performance_uri))
    sys.stderr.write("\n")
    sys.stderr.write("What is the URI of the musical work of which this MIDI is a performance of? (e.g. http://dbpedia.org/resource/Hey_Jude)\n")
    musical_work_uri = URIRef(raw_input())
    sys.stderr.write("What is the URI of the composition from which the musical work was produced? (e.g. http://dbpedia.org/resource/Hey_Jude)\n")
    composition_uri = URIRef(raw_input())
    sys.stderr.write("What is the URI of the composer of the work? (e.g. http://dbpedia.org/resource/The_Beatles)\n")
    composer_uri = URIRef(raw_input())
    sys.stderr.write("What is the URI that identifies you as the artist that performed the work? (e.g. http://example.org/foaf.rdf)\n")
    performer_uri = URIRef(raw_input())
    sys.stderr.write("\n")

    m.add((piece, RDF.type, mo.Performance))
    m.add((piece, mo.performance_of, musical_work_uri))
    m.add((musical_work_uri, RDF.type, mo.MusicalWork))
    m.add((composition_uri, RDF.type, mo.Composition))
    m.add((composition_uri, mo.produced_work, musical_work_uri))
    m.add((composition_uri, mo.composer, composer_uri))
    m.add((composer_uri, RDF.type, mo.MusicArtist))
    m.add((piece, mo.performer, performer_uri))
    m.add((performer_uri, RDF.type, mo.MusicArtist))

    print m.serialize(format='nt')

    g = g + m

    exit(0)

    # print "Here is your RDF graph!"
    # print len(g)
    # for s,p,o in g.triples((None, None, None)):
    #     print s,p,o
    # with open('out.ttl', 'w') as outfile:
    #     outfile.write(g.serialize(format='turtle'))
