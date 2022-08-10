import os

def lyric_reader(lyric_path, without_space = False):
	time = []
	content = []
	with open(lyric_path,'r') as f:
		number_line = 0
		for line in f:
			number_line += 1
			if line[0] != '[' or line[9] != ']':
				print("lyric time format error, line:"+str(number_line))
				os._exit(0)
			time.append(line[1:9])
			if without_space:
				content.append(line[10:-1])
			else:
				content.append(line[10:-1].split(' '))
	return time,content

def note_reader(note_path):
	durations = []
	pitches = []
	with open(note_path,'r') as f:
		for line in f:
			pitch_line = []
			duration_line = []
			notes = line.strip().split()
			for note in notes:
				duration, pitch = note.split(',')
				duration_line.append(float(duration))
				pitch_line.append(int(pitch))
			durations.append(duration_line)
			pitches.append(pitch_line)
	return pitches,durations


class vocal_note:
	def __init__(self, start, end, duration, pitch, lyric=None):
		self.start = start
		self.end = end
		self.duration = duration
		self.pitch = pitch
		self.lyric = lyric

	def add_lyric(self, lyric):
		self.lyric = lyric

	def __str__(self):
		return "onset: {}, offset: {}, duration: {}, pitch: {}, lyric: {}".format(self.start, self.end, self.duration, self.pitch, self.lyric)

	def time2tag(self, time):
		mm = int(time/60)
		ss = int(time%60)

		xx = str(time).split('.')[-1][:2] #:2保留两位小数 向下取

		if mm < 10:
			mm = '0'+str(mm)
		else:
			mm = str(mm)

		if ss < 10:
			ss = '0'+str(ss)
		else:
			ss = str(ss)

		if len(xx) < 2:
			xx = xx+'0'

		return mm+":"+ss+"."+xx

class Convert2_VocalNotes:
	def __call__(self, lyric_path, notation_path):
		phrase_timestamps, lyrics = lyric_reader(lyric_path)
		pitches, durations = note_reader(notation_path)
		output_phrases = []

		assert len(phrase_timestamps) == len(pitches), "total line number of lrc {} : ({} lines) is not equal to notation {} : ({} lines)".format(lyric_path, len(phrase_timestamps), notation_path, len(pitches))
		total_time_count = 0.0
		total_duration_count = 0.0
		total_averate_notetime = 0.0
		for i in range(len(phrase_timestamps)-1):
			assert (len(pitches[i])-self.count_restnote(pitches[i])) == len(lyrics[i]), "lrc : {} and notation : {} have different note numbers in line: {} (lrc: {}, notation: {}), please confirm the note numbers in lrc and notation file is the same, if one lyric has multiple pitches and durations just repeat this lyric (rest note is not included)".format(lyric_path, notation_path, i, len(lyrics[i]), len(pitches[i])-self.count_restnote(pitches[i]))
			phrase_start = self.tag2time(phrase_timestamps[i])
			phrase_end = self.tag2time(phrase_timestamps[i+1])
			
			time_piece = phrase_end - phrase_start
			duration_piece = sum([x for x in durations[i]])
			average_notetime = time_piece / duration_piece

			if average_notetime > total_averate_notetime * 1.25 and total_averate_notetime != 0:
				average_notetime = total_averate_notetime

			onset = 0.0
			offset = 0.0
			timer = phrase_start
			phrase = []
			for j in range(len(pitches[i])):
				onset = timer
				offset = timer + average_notetime*durations[i][j]
				timer = offset

				if pitches[i][j] == 0:
					continue
				else:
					phrase.append(vocal_note(onset, offset, durations[i][j], pitches[i][j]))

			assert len(phrase) == len(lyrics[i]), "lyrics number: {} not equal to note number: {}".format(len(lyrics[i]), len(phrase))
			for j in range(len(lyrics[i])):
				phrase[j].add_lyric(lyrics[i][j])

			output_phrases.append(phrase)

			total_time_count += average_notetime * duration_piece
			total_duration_count += duration_piece
			total_averate_notetime = total_time_count/total_duration_count

		#the last phrase have no phrase end, so use the average notetime to calculate its end
		onset = 0.0
		offset = 0.0
		timer = self.tag2time(phrase_timestamps[-1])
		phrase = []
		for j in range(len(pitches[-1])):
			onset = timer
			offset = timer + total_averate_notetime*durations[-1][j]
			timer = offset

			if pitches[-1][j] == 0:
				continue
			else:
				phrase.append(vocal_note(onset, offset, durations[-1][j], pitches[-1][j]))

		assert len(phrase) == len(lyrics[-1]), "lyrics number: {} not equal to note number: {}".format(len(lyrics[-1]), len(phrase))
		for j in range(len(lyrics[-1])):
			phrase[j].add_lyric(lyrics[-1][j])

		output_phrases.append(phrase)
		
		return output_phrases

	def count_restnote(self, pitches):
		count = 0
		for pitch in pitches:
			if pitch == 0:
				count += 1
		return count

	def tag2time(self, tag):
		mm = int(tag.split(':')[0])
		ss = int(tag.split(':')[1].split('.')[0])
		xx = int(tag.split(':')[1].split('.')[1]) / 100

		return (mm*60 + ss + xx)





