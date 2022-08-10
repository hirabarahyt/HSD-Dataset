import os
from preprocess import vocal_note

class Enhanced_Lrc:
	def __call__(self, file_path):
		phrases = []
		with open(file_path, 'r') as f:
			for n,line in enumerate(f):
				phrase = line.strip().split('<')
				phrase_start = self.tag2time(phrase[0][1:-1])

				notes = []
				total_duration = 0

				for i,note in enumerate(phrase[1:]):
					start, lpd_end = note.split('>')
					lpd, end = lpd_end.split('{')
					end = end.split('}')[0]
					end = self.tag2time(end)

					lyric, pitch, duration = lpd.split(' ')

					start = self.tag2time(start)
					pitch = int(pitch)
					duration = float(duration)

					notes.append(vocal_note(start=start, end=end, duration=duration, pitch=pitch, lyric=lyric))

				phrases.append(notes)

		return phrases

	def tag2time(self, tag_str):
		if len(tag_str)!= 8:
			print("invalid tag length: " + tag_str)
			os._exit(0)
		mm = float(tag_str[0:2])
		ss = float(tag_str[3:5])
		xx = float(tag_str[6:8])

		return mm*60 + ss + xx/100