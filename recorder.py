from mythread import MyThread
from PIL import ImageGrab
from tkinter.filedialog import askdirectory
import cv2
import numpy as np
import os
import time
import tkinter as tk


class Recorder:
	FOURCC = cv2.VideoWriter_fourcc(*"mp4v")  # mp4编码器
	FRAME_SIZE = ImageGrab.grab().size  # 屏幕尺寸
	VERSION = "v1.3"  # 版本号

	DESKTOP = "C:/Users/Dell/Desktop/1"  # 默认保存目录（桌面）
	FPS = 15  # 默认帧率（通过计算近似所得）
	DELAY = 3  # 默认准备时间
	DURATION = 60  # 默认录制时长

	def __init__(self):
		self.root = tk.Tk()  # 主窗口
		self.video = None

		self.flag = 0  # 录屏执行标识
		self.closed_setup = 1  # 设置窗口关闭状态

		self.folder = self.DESKTOP  # 保存目录
		self.fps = self.FPS  # 帧率
		self.delay = self.DELAY  # 准备时间
		self.duration = self.DURATION  # 录制时长

		self.var_record = tk.StringVar()  # 录制按钮文本
		self.var_delay = tk.StringVar()  # 倒计时

		self.var_record_time = tk.StringVar()  # 当前录制时长
		self.var_current_fps = tk.StringVar()  # 当前平均帧率
		self.var_real_time = tk.StringVar()  # 实际录制时长
		self.var_filename = tk.StringVar()  # 文件名

		self.var_folder = tk.StringVar()  # 保存目录
		self.var_fps = tk.StringVar()  # 帧率
		self.var_delay = tk.StringVar()  # 准备时间
		self.var_duration = tk.StringVar()  # 录制时长

		self._init_root()
		self._init_node_state()
		self.root.mainloop()  # 运行主窗口

	def record(self):  # 屏幕录制
		if not self.flag:
			self.flag = 1  # 激活运行标识

			filename = f"录屏{time.strftime('%Y%m%d%H%M%S', time.localtime())}"  # 文件名
			filepath = f"{self.folder[:-1] if self.folder[-1] == '/' else self.folder}/{filename}.mp4"  # 文件路径
			self.video = cv2.VideoWriter(filepath, fourcc=self.FOURCC, fps=self.FPS, frameSize=self.FRAME_SIZE)  # 视频

			self.var_filename.set(filename)
			self.var_record.set("停止")

			delay = int(self.delay)  # 准备时间
			if delay > 0:
				self.var_record_time.set(self.sec2msg())
				self.var_current_fps.set("0.00 fps")
				self.var_real_time.set(self.sec2msg())

				self.state.config(fg="red")  # 设置变红
				self.state.config(textvariable=self.var_delay)  # 倒计时
				for i in range(delay, 0, -1):  # 准备时间倒计时
					self.var_delay.set(self.sec2msg(i))
					time.sleep(1)
			self.state.config(textvariable=self.var_record_time)  # 录屏计时
			self.state.config(fg="black")  # 设置变黑

			timer, count, default_fps, default_duration = time.time(), 0, self.FPS, self.DURATION
			count = 0  # 计数器
			while self.flag:
				rgb = ImageGrab.grab()  # 抓取屏幕快照
				bgr = cv2.cvtColor(np.asarray(rgb), cv2.COLOR_RGB2BGR)  # RGB格式转换为openCv的BGR格式
				self.video.write(bgr)  # 将屏幕快照添加至视频中

				if count % default_fps == 0:  # 每隔固定帧数刷新信息
					current_time = time.time() - timer  # 当前所计时间
					self.var_record_time.set(self.sec2msg(count / default_fps))
					self.var_current_fps.set(f"{(count / current_time):.2f} fps")
					self.var_real_time.set(self.sec2msg(current_time))
				count += 1
				if count == default_fps * default_duration * 60:  # 超出默认录制时长
					self.terminate()
		else:
			self.flag = 0  # 重置运行标识
			self.terminate()

	def terminate(self):  # 终止录屏
		self.video.release()  # 释放视频资源
		self.var_record.set("开始")
		self.state.config(fg="blue")  # 设置变蓝

	def _init_root(self):  # 初始化主窗口
		self.root.title(f"录屏工具 {self.VERSION}")  # 设置标题
		self.root.geometry("+1200+600")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸

		self.var_record_time.set(self.sec2msg())
		self.var_current_fps.set("0.00 fps")
		self.var_real_time.set(self.sec2msg())
		self.var_delay.set(self.sec2msg())
		self.var_record.set("开始")

		tk.Button(self.root, textvariable=self.var_record, command=lambda: MyThread(self.record)).grid(row=0, column=0)

		tk.Label(self.root, text="当前录制时长: ").grid(row=1, column=0)
		tk.Label(self.root, text="当前平均帧率: ").grid(row=2, column=0)
		tk.Label(self.root, text="实际录制时长: ").grid(row=3, column=0)
		tk.Label(self.root, text="文件名: ").grid(row=4, column=0)
		tk.Label(self.root, textvariable=self.var_record_time, width=20).grid(row=1, column=1)
		tk.Label(self.root, textvariable=self.var_current_fps, width=20).grid(row=2, column=1)
		tk.Label(self.root, textvariable=self.var_real_time, width=20).grid(row=3, column=1)
		tk.Label(self.root, textvariable=self.var_filename, width=20).grid(row=4, column=1)

		menu_bar = tk.Menu(self.root)
		menu_main = tk.Menu(menu_bar, tearoff=False)
		menu_main.add_command(label="设置", command=self._init_node_setup)
		menu_bar.add_cascade(label="菜单", menu=menu_main)  # 添加至菜单栏
		self.root["menu"] = menu_bar  # 添加至主窗口

	def _init_node_state(self):  # 初始化状态窗口
		node_state = tk.Toplevel()  # 状态窗口
		node_state.overrideredirect(True)  # 隐藏标题栏
		node_state.geometry("+750+0")  # 设置位置
		node_state.resizable(0, 0)  # 禁止拉伸
		node_state.attributes("-topmost", True)  # 设置保持前端显示

		self.state = tk.Label(node_state, text=self.sec2msg())
		self.state.grid(row=0, column=0)

	def _init_node_setup(self):  # 初始化设置窗口
		def terminate():  # 终结
			node_setup.destroy()
			self.closed_setup = 1

		def submit():  # 确认
			if os.path.exists(self.var_folder.get()):
				self.folder = self.var_folder.get()
			if self.var_fps.get().isdigit() and 10 <= int(self.var_fps.get()) <= 25:
				self.fps = self.var_fps.get()
			if self.var_delay.get().isdigit() and 0 <= int(self.var_delay.get()) <= 5:
				self.delay = self.var_delay.get()
			if self.var_duration.get().isdigit() and 0 <= int(self.var_duration.get()) <= 60:
				self.duration = self.var_duration.get()
			terminate()

		def select_folder():  # 选择保存目录
			folder = askdirectory()
			if folder:
				self.var_folder.set(folder)
		
		if self.closed_setup and not self.flag:
			self.closed_setup = False

			node_setup = tk.Toplevel()  # 设置窗口
			node_setup.protocol("WM_DELETE_WINDOW", terminate)  # 绑定关闭事件
			node_setup.title("设置")  # 设置标题
			node_setup.geometry("+1200+400")  # 设置位置
			node_setup.resizable(0, 0)  # 禁止拉伸

			self.var_folder.set(self.folder)
			self.var_fps.set(self.fps)
			self.var_delay.set(self.delay)
			self.var_duration.set(self.duration)

			tk.Button(node_setup, text="选择目录", command=select_folder).grid(row=0, column=2)
			tk.Button(node_setup, text="确定", command=submit).grid(row=4, column=1)
			tk.Button(node_setup, text="取消", command=terminate).grid(row=4, column=2)

			tk.Entry(node_setup, textvariable=self.var_folder).grid(row=0, column=1)
			tk.Entry(node_setup, textvariable=self.var_fps).grid(row=1, column=1)
			tk.Entry(node_setup, textvariable=self.var_delay).grid(row=2, column=1)
			tk.Entry(node_setup, textvariable=self.var_duration).grid(row=3, column=1)

			tk.Label(node_setup, text="保存至").grid(row=0, column=0)
			tk.Label(node_setup, text="帧率").grid(row=1, column=0)
			tk.Label(node_setup, text="(10-25)fps").grid(row=1, column=2)
			tk.Label(node_setup, text="准备时间").grid(row=2, column=0)
			tk.Label(node_setup, text="(0-5)秒").grid(row=2, column=2)
			tk.Label(node_setup, text="录制时长").grid(row=3, column=0)
			tk.Label(node_setup, text="(0-60)分钟").grid(row=3, column=2)

	@staticmethod
	def sec2msg(sec=0):  # 格式化秒数
		if sec == 0:
			return "00:00:00"
		hour = int(sec / 3600)
		minute = int((sec % 3600) / 60)
		second = int(sec % 60)
		return f"{hour:02}:{minute:02}:{second:02}"


if __name__ == "__main__":
	Recorder()
