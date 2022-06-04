import psutil
import time
import tkinter as tk


class NetSpeed:
	def __init__(self):
		self.gui = GUI()
		self.recv_before = psutil.net_io_counters().bytes_recv  # 当前已下载流量
		self.sent_before = psutil.net_io_counters().bytes_sent  # 当前已上传流量

	def calculate(self):  # 计算当前网速
		recv_now = psutil.net_io_counters().bytes_recv  # 当前已下载流量
		sent_now = psutil.net_io_counters().bytes_sent  # 当前已上传流量

		self.gui.var_time.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		self.gui.var_recv.set(self.byte2str(recv_now - self.recv_before))  # 1秒内下载的流量
		self.gui.var_sent.set(self.byte2str(sent_now - self.sent_before))  # 1秒内上传的流量

		self.recv_before = recv_now
		self.sent_before = sent_now
		self.gui.root.after(1000, self.calculate)

	@staticmethod
	def byte2str(byte):  # byte转为字符串
		kb = byte / 1024
		if kb > 1024:
			return f"{kb / 1024:>7.2f} MB/s"
		return f"{kb:>7.2f} KB/s"

	def run(self):  # 运行
		self.gui.init_root()
		self.calculate()
		self.gui.root.mainloop()


class GUI:
	def __init__(self):
		self.root = tk.Tk()  # 主窗口

		'''主窗口'''
		self.var_time = tk.StringVar()  # 当前时间
		self.var_recv = tk.StringVar()  # 当前下载速率
		self.var_sent = tk.StringVar()  # 当前上传速率

	def init_root(self):  # 初始化主窗口
		self.root.title("网速")  # 设置标题
		self.root.geometry("+1200+550")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸

		'''标签'''
		tk.Label(self.root, text="当前时间: ").grid(row=0, column=0)
		tk.Label(self.root, text="当前下载速率: ").grid(row=1, column=0)
		tk.Label(self.root, text="当前上传速率: ").grid(row=2, column=0)
		tk.Label(self.root, textvariable=self.var_time).grid(row=0, column=1)
		tk.Label(self.root, textvariable=self.var_recv).grid(row=1, column=1)
		tk.Label(self.root, textvariable=self.var_sent).grid(row=2, column=1)


if __name__ == "__main__":
	netspeed = NetSpeed()
	netspeed.run()
