import psutil
import time
import tkinter as tk


class NetSpeed:
	def __init__(self):
		self.gui = GUI((self.average,))
		self.flag = 0  # 运行时标志
		self.timer = 0  # 计时器
		self.sent_before, self.recv_before = 0, 0  # 当前上传下载速率
		self.sent_before_avg, self.recv_before_avg = 0, 0  # 平均上传下载速率

	def calculate(self):  # 测量当前网速
		sent_now = psutil.net_io_counters().bytes_sent  # 当前已上传流量
		recv_now = psutil.net_io_counters().bytes_recv  # 当前已下载流量

		if self.sent_before and self.recv_before:
			sent = (sent_now - self.sent_before) / 1024  # 1秒内上传的流量
			recv = (recv_now - self.recv_before) / 1024  # 1秒内下载的流量

			self.gui.var_time_now.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
			self.gui.var_sent_now.set(f"{sent:>7.2f} KB/s")
			self.gui.var_recv_now.set(f"{recv:>7.2f} KB/s")

		if self.flag:
			self.gui.var_time_avg.set(self.sec2fmt(time.time() - self.timer))

		self.sent_before = sent_now
		self.recv_before = recv_now
		self.gui.root.after(1000, self.calculate)

	def average(self):  # 测量平均网速
		if self.flag:
			self.flag = 0

			self.gui.button_calculate.config(text="开始统计")

			time_avg = round(time.time() - self.timer)  # 统计时间
			sent_now_avg = psutil.net_io_counters().bytes_sent  # 统计后已上传流量
			recv_now_avg = psutil.net_io_counters().bytes_recv  # 统计后已下载流量
			sent_avg = (sent_now_avg - self.sent_before_avg) / (1024 * time_avg)  # 统计已上传流量
			recv_avg = (recv_now_avg - self.recv_before_avg) / (1024 * time_avg)  # 统计已下载流量
			self.gui.var_time_avg.set(self.sec2fmt(time_avg))
			self.gui.var_sent_avg.set(f"{sent_avg:>7.2f} KB/s")
			self.gui.var_recv_avg.set(f"{recv_avg:>7.2f} KB/s")
		else:
			self.flag = 1

			self.gui.button_calculate.config(text="停止统计")
			self.gui.var_time_avg.set(self.sec2fmt())
			self.timer = time.time()

			self.sent_before_avg = psutil.net_io_counters().bytes_sent  # 统计前已上传流量
			self.recv_before_avg = psutil.net_io_counters().bytes_recv  # 统计前已下载流量

	@staticmethod
	def sec2fmt(sec=0):  # 格式化秒数
		if round(sec):
			hour = int(sec / 3600)
			minute = int((sec % 3600) / 60)
			second = int(sec % 60)
			return f"{hour:02}:{minute:02}:{second:02}"
		return "00:00:00"

	def run(self):  # 运行
		self.gui.init_root()
		self.calculate()
		self.gui.root.mainloop()


class GUI:
	def __init__(self, funcs):
		self.average, = funcs
		self.root = tk.Tk()  # 主窗口

		'''主窗口'''
		self.var_time_now = tk.StringVar()  # 当前时间
		self.var_sent_now = tk.StringVar()  # 当前上传速率
		self.var_recv_now = tk.StringVar()  # 当前下载速率
		self.var_time_avg = tk.StringVar()  # 统计时间
		self.var_sent_avg = tk.StringVar()  # 平均上传速率
		self.var_recv_avg = tk.StringVar()  # 平均下载速率
		self.button_calculate = None

	def init_root(self):  # 初始化主窗口
		self.root.title("网速测量工具")  # 设置标题
		self.root.geometry("+1200+550")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸

		'''参数'''
		default_speed = "   0.00 KB/s"
		self.var_time_now.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		self.var_sent_now.set(default_speed)
		self.var_recv_now.set(default_speed)
		self.var_time_avg.set("00:00:00")
		self.var_sent_avg.set(default_speed)
		self.var_recv_avg.set(default_speed)

		'''按钮'''
		self.button_calculate = tk.Button(self.root, text="开始统计", command=self.average)
		self.button_calculate.grid(row=3, column=0)

		'''标签'''
		tk.Label(self.root, text="当前时间: ").grid(row=0, column=0)
		tk.Label(self.root, text="当前上传速率: ").grid(row=1, column=0)
		tk.Label(self.root, text="当前下载速率: ").grid(row=2, column=0)
		tk.Label(self.root, text="平均上传速率: ").grid(row=4, column=0)
		tk.Label(self.root, text="平均下载速率: ").grid(row=5, column=0)
		tk.Label(self.root, textvariable=self.var_time_now).grid(row=0, column=1)
		tk.Label(self.root, textvariable=self.var_sent_now).grid(row=1, column=1)
		tk.Label(self.root, textvariable=self.var_recv_now).grid(row=2, column=1)
		tk.Label(self.root, textvariable=self.var_time_avg).grid(row=3, column=1)
		tk.Label(self.root, textvariable=self.var_sent_avg).grid(row=4, column=1)
		tk.Label(self.root, textvariable=self.var_recv_avg).grid(row=5, column=1)


if __name__ == "__main__":
	netspeed = NetSpeed()
	netspeed.run()
