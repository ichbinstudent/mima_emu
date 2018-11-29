import re

class Memory:
	def __init__(self, mem= {}):
		self.mem = mem
	def ReadVal(self, pos):
		return self.mem[pos]

	def StoreVal(self, pos, val):
		self.mem[pos] = val

'''
asm = 	"""
		LDC 0,
		STV i,
		LABEL loop,
		LDV i,
		STIV i,
		LDC 1,
		ADD i,
		STV i,
		LDC 4,
		NOT,
		ADD i,
		JMN loop,
		HALT
		"""
'''

asm="""
	LDC 0,
	STV x,
	LABEL while,
	LDV x,
	EQL 4,
	JMN end,
	STIV x,
	LDV 1,
	ADD x,
	STV x,
	JMP while,
	LABEL end,
	HALT
	"""

memory = Memory({
	'i':  '0',
	})

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

