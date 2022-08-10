import argparse
from preprocess import Convert2_VocalNotes
from make_midi import Make_MIDI
from utils import write_enhanced_lyric

parser = argparse.ArgumentParser(description='create a midi and an enhanced LRC from notation and lrc')
parser.add_argument('-l','--lrc', type=str, default="lrc/1.lrc", help='inpu lrc file path')
parser.add_argument('-n','--notation', type=str, default="notation/1.txt", help='input notation file path')
parser.add_argument('-m','--midi', type=str, default="midi/1.mid", help='output midi file path')
parser.add_argument('-e','--enhanced_lrc', type=str, default="enhanced_lrc/1.lrc", help='output enhanced lrc file path')
parser.add_argument('--lrc_folder', type=str, default="lrc/", help='inpu lrc file path')
parser.add_argument('--notation_folder', type=str, default="notation/", help='input notation file path')
parser.add_argument('--midi_folder', type=str, default="midi/", help='output midi file path')
parser.add_argument('--enhanced_lrc_floder', type=str, default="enhanced_lrc/", help='output enhanced lrc file path')
opt = parser.parse_args()


#process one song
convert2notes = Convert2_VocalNotes()
notes = convert2notes(opt.lrc, opt.notation)
convert2midi = Make_MIDI()
convert2midi(notes, opt.midi)
write_enhanced_lyric(notes, opt.enhanced_lrc)

#process all songs
# for i in range(1,69):
# 	convert2notes = Convert2_VocalNotes()
# 	notes = convert2notes(opt.lrc_folder+str(i)+".lrc", opt.notation_folder+str(i)+".txt")
# 	convert2midi = Make_MIDI()
# 	convert2midi(notes, opt.midi_folder+str(i)+".midi")
# 	write_enhanced_lyric(notes, opt.enhanced_lrc_floder+str(i)+".lrc")