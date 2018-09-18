from flask import Flask, request
from rdf2midi import rdf2midi
import subprocess
import pretty_midi as pm
import os
from rdflib import Graph, URIRef, Namespace, OWL
import hashlib

app = Flask(__name__)

def poly2mono(s, o, q_threshold = 2):
    midi_old = pm.PrettyMIDI(s)
    midi_new = pm.PrettyMIDI()

    # search all tracks for multiple simultaneous notes
    # see https://github.com/craffel/pretty-midi/issues/119
    for instr in midi_old.instruments:
        instr_is_mono = True
        for note1 in instr.notes:
            dur1 = note1.end - note1.start
            # if the instrument is still monophonic: keep searching
            if instr_is_mono == True:
                for note2 in instr.notes:
                    # skip any notes that have already been note1
                    if not note2.start < note1.start:
                        # if there is overlap
                        if (note1 != note2) and (note2.start < note1.end):
                            overlap = note1.end - note2.start
                            # if the overlap is larger than threshold: consider non-monophonic and break
                            if overlap > dur1/q_threshold:
                                instr_is_mono = False
                                break
                            # if the overlap is smaller than the threshold: quantise
                            else:
                                note1.end = note2.start
            # if the instrument is no longer monophonic: proceed to the next instrument
            else:
                break
        # if the instrument is monophonic: add to new MIDI file
        if instr_is_mono:
            midi_new.instruments.append(instr)
    # if the new MIDI file contains tracks: save; else add to list
    if len(midi_new.instruments) != 0:
        midi_new.write('midi-ld-similarity/data/' + o)
    # else:
    # 	non_monophonic.append(s)

@app.route("/", methods=['GET'])
def swmiditp_api():
    # 1. rdf2midi of perf_uri -> poly.mid
    # 2. poly.mid -> mono.midi
    # 2.5. frbr links
    # 3. similarity match of mono.midi against data/
    # 4. add resulting triples to graph_uri
    perf_uri = request.args.get('perf_uri')
    graph_uri = request.args.get('graph_uri')

    print perf_uri
    print graph_uri

    triples = subprocess.check_output(['./swmiditp-download.sh', '{}'.format(perf_uri)])
    with open('out.ttl', 'w') as f:
        f.write(triples)

    rdf2midi('out.ttl', 'poly.mid')
    poly2mono('poly.mid', 'mono.mid')

    # perf_uri sameAs poly.mid
    # poly.mid sameAs mono.mid

    hash_poly = hashlib.md5(open('poly.mid', 'rb').read()).hexdigest()
    hash_mono = hashlib.md5(open('midi-ld-similarity/data/mono.mid', 'rb').read()).hexdigest()
    poly_uri = URIRef('http://purl.org/midi-ld/pattern/{}'.format(hash_poly))
    mono_uri = URIRef('http://purl.org/midi-ld/pattern/{}'.format(hash_mono))
    perf_uri = URIRef(perf_uri)

    frbr_g = Graph()
    frbr_uri = URIRef("http://purl.org/vocab/frbr/core#")
    frbr = Namespace(frbr_uri)
    frbr_g.bind('frbr', frbr)
    frbr_g.add((mono_uri, frbr['transformation'], poly_uri))
    frbr_g.add((poly_uri, OWL.sameAs, perf_uri))
    print frbr_g.serialize(format='nt')
    with open('midi-ld-similarity/links.nt', 'w') as f:
        f.write(frbr_g.serialize(format='nt'))

    os.chdir('midi-ld-similarity')

    print subprocess.check_output(['./swmiditp-similarity.sh', 'mono.mid', 'http://purl.org/midi-ld/saam-demo'])

    return '200'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8010, debug=True)
