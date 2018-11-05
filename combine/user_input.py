import threading 
import time
import sys
import select


class input_thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.cmd_input=self.timeout_input(0,"Do you want to cut?[Y/N]:	")
		self.cut_status=0

	def run(self):
		while (True):
			self.cmd=self.ask_input()
			time.sleep(0.3)

	def ask_input(self):

		if self.cmd_input=="Y" or self.cmd_input=="y":
			print("Cutting in progress")
			self.cmd_input = self.timeout_input(0,"\nDo you want to cut?[Y/N]:	")
			self.cut_status=2

		elif self.cmd_input=="N" or self.cmd_input=="n":
			print("Releasing scissors")
			self.cmd_input = self.timeout_input(0,"\nDo you want to cut?[Y/N]:	")
			self.cut_status=1

		else:
			self.cmd_input = self.timeout_input(0,"")
			self.cut_status=0

	def timeout_input(self,timeout, prompt="", timeout_value=None):
		sys.stdout.write(prompt)
		sys.stdout.flush()
		ready, _, _ = select.select([sys.stdin], [], [], timeout)
		if ready:
			 return sys.stdin.readline().rstrip('\n')
		else:
			#sys.stdout.write('\n')
			sys.stdout.flush()
			return timeout_value
	def status(self):
		
		return self.cut_status
