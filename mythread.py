from threading import Thread


class MyThread(Thread):
	def __init__(self, func, *args):
		super().__init__()

		self.func = func
		self.args = args

		self.setDaemon(True)
		self.start()

	def run(self):
		self.func(*self.args)
