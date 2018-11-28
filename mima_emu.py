import re

class Memory:
	def __init__(self, mem= {}):
		self.mem = mem
	def ReadVal(self, pos):
		return self.mem[pos]

	def StoreVal(self, pos, val):
		self.mem[pos] = val


asm = 	"""
		LDC 0,
		STV i,
		LABEL loop,
		LDV i,
		STIV i,
		LDC 1,
		ADD i,
		STV i,
		LDC 5,
		EQL i,
		NOT
		JMN loop,
		HALT
		"""


memory = Memory({
	'i':  '0',
	'0': '1',
	'1': '1',
	'2': '1',
	'3': '1',
	'4': '1',
	})
'''
	'6': '0',
	'7': '10',
	'8': '0',
	'9': '10',
	'10': '0',
	'11': '10',
	'12': '0',
	'13': '10',
	'14': '0',
	'15': '10',
	'16': '0',
	'17': '10',
	'18': '0',
	'19': '10',
	'20': '0',
	'21': '10',
	'22': '0',
	'23': '10',
	'24': '0',
'''
akku = 0
labels = []

final = re.findall(r"[\w']+", asm)
print(final)

pos = 0
while (pos < len(final)):
	x = final[pos]
	if(x == "LABEL"):
		labels.append([final[pos + 1], pos])
		final.pop(pos)
		final.pop(pos)
		continue
	pos+=1

pos = 0
while (pos < len(final)):
	akku = akku % (2**24)
	x = final[pos]
	if(pos + 1 < len(final)):
		print(x, final[pos+1])
	else:
		print(x)
	print(memory.mem, akku) # decimal
	#print('\t'.join(str(format(memory.mem[e], '024b')) for e in memory.mem), format(akku, '024b')) # binary
	if(x == 'STIV'):
		memory.StoreVal(memory.ReadVal(final[pos + 1]), str(akku))
		pos += 2
		continue
	if(x == 'LDIV'):
		akku = int(memory.ReadVal(memory.ReadVal(final[pos + 1])))
		pos += 2
		continue
	if(x == 'AND'):
		akku = akku & int(memory.ReadVal(final[pos + 1]))
		pos += 2
		continue
	if(x == 'LDC'):
		akku = int(final[pos + 1])
		pos += 2
		continue
	if(x == 'ADD'):
		akku = akku + int(memory.ReadVal(final[pos + 1]))
		pos += 2
		continue
	if(x == 'LDV'):
		akku = int(memory.ReadVal(final[pos + 1]))
		pos += 2
		continue
	if(x == 'STV'):
		memory.StoreVal(final[pos + 1], str(akku))
		pos += 2
		continue
	if(x == 'EQL'):
		if (akku == int(memory.ReadVal(final[pos + 1]))):
			akku = -1
		else:
			akku = 0
		pos += 2
		continue
	if(x == 'NOT'):
		akku = ~akku
		pos += 1
		continue
	if(x == 'JMP'):
		pos = int(''.join(str(e) for e in [t[1] for t in labels if t[0] == final[pos + 1]]))
		continue
	if(x == 'JMN'):
		if(akku > 2**23):
			pos = int(''.join(str(e) for e in [t[1] for t in labels if t[0] == final[pos + 1]]))
		else:
			pos += 2
		continue
	if(x == 'HALT'):
		break
	break

