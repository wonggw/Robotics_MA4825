import sys, select, termios, tty

settings = termios.tcgetattr(sys.stdin)
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


def getKey():
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
	if rlist:
		key = sys.stdin.read(1)
	else:
		key = ''

	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key
cut_status=0
while True:
	key=getKey()
	if key =='w':
		print("Forward")
	if key =='s':
		print("Reverse")
	if key =='a':
		print("Left")
	if key =='d':
		print("Right")
	if key =='v':
		cut_status =1
	elif key !='v' and cut_status==1:
		cut_status =0
		print("Releasing")
	if key =='c':
		cut_status =2
	elif key !='c' and cut_status==2:
		cut_status =0
		print("Cutting")
	if key =='1':
		break
	#print(key)
