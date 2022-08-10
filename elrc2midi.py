import os
from read_enhanced_lyric import Enhanced_Lrc
from make_midi import Make_MIDI

import argparse

parser = argparse.ArgumentParser(description='create a midi and an enhanced LRC from notation and lrc')
parser.add_argument('-e','--enhanced_lrc', type=str, default="enhanced_lrc/1.lrc", help='input enhanced lrc file path')
parser.add_argument('-m','--midi', type=str, default="midi/1.mid", help='output midi file path')
opt = parser.parse_args()

read_elrc = Enhanced_Lrc()
notes = read_elrc(opt.enhanced_lrc)

convert2midi = Make_MIDI()
convert2midi(notes, opt.midi)