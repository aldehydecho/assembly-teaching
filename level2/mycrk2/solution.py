import datetime, sys

"""
valid hex digits, with correct CAsE
"""
decoder = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'b', 'C', 'd', 'E', 'f']


"""
given the username buffer (already augmented with time info),
and the number of the "pass", produces an integer
"""
def gen_number_a(buf, passn):
	result = (passn * 0xef41) + 0x2cdc3

	counter = 0
	for c in buf:
		result += c * counter
		counter += 1

	return result


"""
given the username string, produces a buffer, augmented with
current time info
"""
def augment_argv1(argv1):

	now = datetime.datetime.now()

	buf = [ord(c) for c in argv1]

	return buf + [(now.minute & 0xf) + 0x41] + [(now.hour & 0xf) + 0x42]


"""
maps a hex digit to the correct one according to the decoder array
"""
def mapdigit(digit):
	return decoder[int(digit, 16)]


"""
encodes a number in hex format, using the decoder array to produce
valid digits
"""
def num_to_hex(num):
	
	enc = [mapdigit(c) for c in hex(num).replace("0x", "")]

	padding = ["0"] * (8-len(enc))

	return "".join(padding + enc)


"""
given the username string, produces the command line for a valid user/key combination
please note that the generated pair is valid only within the same minute in which is generated
"""
def generate_key(username):
	inp = augment_argv1(username)

	key = ""

	for p in range(3):
		key += num_to_hex(gen_number_a(inp, p))

	print "COMMAND: ./mycrk2 {0} {1}".format(username, key)

if __name__ == "__main__":
	
	# default username, provide yours via command line args
	username = "porcodio"

	if len(sys.argv) >= 2:
		username = sys.argv[1]

	generate_key( username )

