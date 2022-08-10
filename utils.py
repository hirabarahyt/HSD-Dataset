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

