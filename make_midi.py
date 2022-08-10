import os
import numpy as np
from utils import intToBytes,npToBytes

class Make_MIDI:
	def __init__(self,track_mode=1,track_num=2,tickPerQuarterNote=120):
		self.midi_header = b"MThd\x00\x00\x00\x06"
		self.track_mode = intToBytes(track_mode,2) #0 单音轨 1 多音轨同步 2 多音轨不同步
		self.track_num = intToBytes(track_num,2)
		self.tickPerQuarterNote = intToBytes(tickPerQuarterNote,2)
		self.tracks = []

	def __call__(self, note_arr, output_path):
		self.make(note_arr)
		self.write_binary(output_path)

	def write_binary(self,out_path):
		binary_str = self.midi_header+self.track_mode+self.track_num+self.tickPerQuarterNote
		for i in range(len(self.tracks)):
			binary_str += self.tracks[i]
		with open(out_path,"wb") as f:
			f.write(binary_str)


	def new_track(self,track_contents):
		track_header = b"MTrk"
		track_bytes_num = intToBytes(len(track_contents),4)
		return track_header+track_bytes_num+track_contents

	def make(self, note_arr, tick_time=1000):
		self.tracks.append(self.new_track(self.tempo_event(tick_time)+self.trackEndEvent()))
		contents = b""
		last_clock = 0
		multiple = 1000000/tick_time
		for phrase in note_arr:
			for note in phrase:
				start = note.start
				end = note.end
				pitch = note.pitch

				assert pitch > 0 and pitch < 128, "pitch should be in range[0,127]"
				assert start < end, "start should be earlier than end"

				global_tick_start = int(round(start - 0, 10)*multiple)
				global_tick_end = int(round(end - 0, 10)*multiple)

				tick_start = global_tick_start - last_clock
				tick_end = global_tick_end - global_tick_start

				contents += self.time_cat(self.dynamic_bytes(tick_start))+self.noteOnEvent(pitch)
				contents += self.time_cat(self.dynamic_bytes(tick_end))+self.noteOffEvent(pitch)

				last_clock = global_tick_end

		self.tracks.append(self.new_track(self.changeProgramEvent()+contents+self.trackEndEvent()))

	def noteOnEvent(self,note,velocity=64):
		header = b"\x90"
		note_byte = intToBytes(note,1)
		velocity = intToBytes(velocity,1)
		return header+note_byte+velocity  

	def noteOffEvent(self,note,velocity=0):
		header = b"\x90"
		note_byte = intToBytes(note,1)
		velocity = intToBytes(velocity,1)
		return header+note_byte+velocity

	def changeProgramEvent(self,program=0): #0 is piano
		header = b"\xC0"
		instrument_byte = intToBytes(program,1)
		return 	b"\x00"+header+instrument_byte   #\x00 means time

	def tempo_event(self,tick_time=1000): # tick_time is us (1000us = 1ms)
		header = b"\xFF\x51\x03"
		self.tick_time = tick_time
		timePerQuarterNote = self.tick_time*int.from_bytes(self.tickPerQuarterNote,byteorder="big")
		time_bytes = intToBytes(int(timePerQuarterNote),3)
		return b"\x00"+header+time_bytes   #\x00 means time

	def trackEndEvent(self):
		return b"\x00\xFF\x2F\x00"

	def dynamic_bytes(self,int_num):
		digit_units = digit_tens = digit_hundreds = 0
		if int_num > 2097151: # 2097151 = 128*128*128 - 1
			print("bad tick time > 2097151")
			os._exit(0)
		t = int_num
		if t > 16383: # 16383 = 128*128-1
			digit_hundreds = int(t/128/128) + 128
			t = t % (128*128)
		if t > 127:
			digit_tens = int(t/128) + 128
			t = t % 128
		elif t <= 127 and digit_hundreds != 0:
			digit_tens = int(t/128) + 128
		digit_units = t

		return [digit_hundreds,digit_tens,digit_units]

	def time_cat(self,time):
		[hundred,ten,unit] = time
		if hundred !=0 :
			return npToBytes(np.array([hundred,ten,unit]),1)
		elif hundred == 0 and ten != 0:
			return npToBytes(np.array([ten,unit]),1)
		else:
			return npToBytes(np.array([unit]),1)



