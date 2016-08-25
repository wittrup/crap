
N = 0   #  character never appears in text
A = 1   #  character appears in plain ASCII text
I = 2   #  character appears in ISO-8859 text
X = 3   #  character appears in non-ISO extended ASCII (Mac, IBM PC)

text_chars  = [
	#                   BEL BS HT LF VT FF CR
	N, N, N, N, N, N, N, A, A, A, A, A, A, A, N, N,  #  0x0X
	#                               ESC
	N, N, N, N, N, N, N, N, N, N, N, A, N, N, N, N,  #  0x1X
	A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A,  #  0x2X
	A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A,  #  0x3X
	A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A,  #  0x4X
	A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A,  #  0x5X
	A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, A,  #  0x6X
	A, A, A, A, A, A, A, A, A, A, A, A, A, A, A, N,  #  0x7X
	#             NEL
	X, X, X, X, X, A, X, X, X, X, X, X, X, X, X, X,  #  0x8X
	X, X, X, X, X, X, X, X, X, X, X, X, X, X, X, X,  #  0x9X
	I, I, I, I, I, I, I, I, I, I, I, I, I, I, I, I,  #  0xaX
	I, I, I, I, I, I, I, I, I, I, I, I, I, I, I, I,  #  0xbX
	I, I, I, I, I, I, I, I, I, I, I, I, I, I, I, I,  #  0xcX
	I, I, I, I, I, I, I, I, I, I, I, I, I, I, I, I,  #  0xdX
	I, I, I, I, I, I, I, I, I, I, I, I, I, I, I, I,  #  0xeX
	I, I, I, I, I, I, I, I, I, I, I, I, I, I, I, I   #  0xfX
]

if __name__ == '__main__':
	print('\n'.join(str(text_chars[i:i+16]) for i in range(0, len(text_chars), 16)))