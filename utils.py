import os
import math
import numpy as np


def intToBytes(int_num,BytesNum,byteorder="big"):
	if int_num > pow(256,BytesNum) or BytesNum < 1:
		print("cant transform int to bytes cause BytesNum is too short")
		print(int_num,BytesNum)
		os._exit(0)
	if BytesNum == 1:
		return bytes([int_num])
	else:
		out = []
		quotient = 0
		remainder = int_num
		for i in range(BytesNum,1,-1):
			x = pow(256,i-1)
			quotient = math.floor(remainder/(x))
			out.append(quotient)
			remainder = remainder%(x)
		out.append(remainder)
		if byteorder == "big":
			return bytes(out)
		elif byteorder == "little":
			return bytes(out[::-1])
		else:
			print("byteorder must be big or little")
			os._exit(0)

def npToBytes(int_np,BytesNum,byteorder="big"):
	if BytesNum == 1:
		return bytes(int_np.tolist())

	length = len(int_np)
	out = np.zeros((length,BytesNum),dtype = np.int)
	quotient = np.zeros(length,dtype = np.int)
	remainder = int_np
	for i in range(BytesNum,1,-1):
		x = pow(256,i-1)
		quotient = np.floor(remainder/x)
		out[:,i-1] = quotient
		remainder = remainder%x
	out[:,0] = remainder
	if byteorder == "big":
		out = out[:,::-1]
	elif byteorder == "little":
		out = out
	else:
		print("byteorder must be big or little")
		os._exit(0)

	return bytes(out.flatten().tolist())

def write_enhanced_lyric(data, output_path):
	output_file = open(output_path, 'w')

	for phrase in data:
		out_str = '[' + phrase[0].time2tag(phrase[0].start) + ']'
		for word in phrase:
			# word.show_lyric()
			word_start = word.time2tag(word.start)
			word_end = word.time2tag(word.end)

			out_str += '<' + word_start + '>' + word.lyric + ' ' + str(word.pitch) + ' ' + str(word.duration) + '{' +word_end +'}'

		out_str += '\n'
		output_file.write(out_str)

class Elrc:
	def __init__(self, file_path):
		phrases = []
		with open(file_path, 'r') as f:
			for n,line in enumerate(f):
				if line[:2] != '[0': continue

				phrase = line.strip().split('<')
				phrase_start = self.tag2time(phrase[0][1:-1])

				words = []
				total_duration = 0

				for i,word in enumerate(phrase[1:]):
					word_start, lpd_end = word.split('>')
					lpd, word_end = word.split('{')
					word_end = word_end.split('}')[0]
					word_end = self.tag2time(word_end)

					lyric, pitch, duration = lpd.split(' ')

					word_start = self.tag2time(word_start)
					pitch = int(pitch)
					duration = float(duration)

					words.append(word_info(start=word_start, end=word_end, beat=duration, pitch=[pitch]))

				for word in words:
					word.show()


				phrases.append(words)

		self.phrases = phrases

	def data(self):
		return self.phrases

	def tag2time(self, tag_str):
		if len(tag_str)!= 8:
			print("invalid tag length: " + tag_str)
			os._exit(0)
		mm = float(tag_str[0:2])
		ss = float(tag_str[3:5])
		xx = float(tag_str[6:8])

		return mm*60 + ss + xx/100

