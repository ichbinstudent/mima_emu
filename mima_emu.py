import re, sys

class Memory:
	def __init__(self, mem= {}):
		self.mem = mem
	def ReadVal(self, pos):
		return int(self.mem[pos])

	def StoreVal(self, pos, val):
		self.mem[pos] = int(val)

speicher = {
	'x': 62,
	'y': 0,
}


#asm = "LDC 0;STV z;LABEL A; EQL x;NOT;JMN B;HALT;LABEL B; LDV y;ADD z;STV z;LDC 0;NOT;ADD x;STV x;LDC 0;LABEL C;JMP A"
#asm = "LDV y;ADD z;STV z;LDC 0;NOT;ADD x;STV x;LDC 0"

asm = 	""" LDC 0,
			STV y,
			LABEL while,
			LDC 0,
			NOT,
			ADD x,
			JMN end,
			LDC 0,
			NOT,
			ADD x,
			AND x,
			STV x,
			LDC 1,
			ADD y,
			STV y,
			JMP while,
			LABEL end,
			HALT"""


memory = Memory(speicher)
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

print(labels)
print(final)


pos = 0
while (pos < len(final)):
	akku = akku % (2**24)
	x = final[pos]
	if(pos + 1 < len(final)):
		print(x, final[pos+1])
	else:
		print(x)
	#print(memory.mem, akku)
	print('\t'.join(str(format(memory.mem[e], '024b')) for e in memory.mem), format(akku, '024b'))
	if(x == 'AND'):
		akku = akku & memory.ReadVal(final[pos + 1])
		pos += 2
		continue
	if(x == 'LDC'):
		akku = int(final[pos + 1])
		pos += 2
		continue
	if(x == 'ADD'):
		akku = akku + memory.ReadVal(final[pos + 1])
		pos += 2
		continue
	if(x == 'LDV'):
		akku = memory.ReadVal(final[pos + 1])
		pos += 2
		continue
	if(x == 'STV'):
		memory.StoreVal(final[pos + 1], akku)
		pos += 2
		continue
	if(x == 'EQL'):
		if (akku == memory.ReadVal(final[pos + 1])):
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

