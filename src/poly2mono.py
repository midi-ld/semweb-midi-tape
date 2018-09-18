#!/usr/bin/env python

import pretty_midi as pm
import sys

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
        midi_new.write(o)
    # else:
    # 	non_monophonic.append(s)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: poly2mono.py <input_poly_midi_file> <output_mono_midi_file>"
        exit(1)
    poly2mono(sys.argv[1], sys.argv[2])
    exit(0)
