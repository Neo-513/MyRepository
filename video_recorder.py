from PIL import ImageGrab
from tkinter.filedialog import askdirectory
import cv2
import numpy as np
import os
import time
import tkinter as tk


class VideoRecorder:
	FOURCC = cv2.VideoWriter_fourcc(*"mp4v")  # mp4编码器
	FPS = 15  # 帧率（通过计算近似所得）
	FRAME_SIZE = ImageGrab.grab().size  # 屏幕尺寸

	FOLDER = "C:/Users/Dell/Desktop"  # 默认保存目录
	DELAY = 3  # 默认准备时长
	DURATION = 60  # 默认录制时长

	def __init__(self):
		self.gui = GUI((self.record,), (self.FOLDER, self.FPS, self.DELAY, self.DURATION))
		self.timer = 0  # 计时器
		self.count = 0  # 计数器
		self.video = None  # 视频

	def core(self):  # 核心函数
		if self.gui.flag_record == 1 and self.count <= self.gui.fps * self.gui.duration * 60:
			self.shot()
			if self.count % self.gui.fps == 0:  # 每隔固定帧数刷新信息
				current_time = time.time() - self.timer  # 当前所计时间
				self.gui.var_record_time.set(self.sec2fmt(self.count / self.gui.fps))
				self.gui.var_current_fps.set(f"{(self.count / current_time):.2f} fps")
				self.gui.var_real_time.set(self.sec2fmt(current_time))
			self.count += 1
			self.gui.root.after(1, self.core)
		else:
			self.video.release()  # 释放视频资源
			self.gui.button_record.config(text="●")
			self.gui.label_state.config(fg="blue")

	def record(self):  # 录制
		if self.gui.flag_record < 0:
			self.gui.label_state.config(textvariable=self.gui.var_countdown, fg="red")
			self.gui.button_record.config(state="disabled", text="■")  # 禁用按钮
			self.gui.var_countdown.set(self.sec2fmt(-self.gui.flag_record))
			self.gui.flag_record += 1
			self.gui.root.after(1000, self.record)
		elif self.gui.flag_record == 0:
			self.gui.flag_record = 1  # 激活运行标志

			file_path = f"{self.gui.folder.rstrip('/')}/录屏{time.strftime('%Y%m%d%H%M%S', time.localtime())}.mp4"
			self.video = cv2.VideoWriter(file_path, fourcc=self.FOURCC, fps=self.FPS, frameSize=self.FRAME_SIZE)

			self.gui.var_record_time.set(self.sec2fmt())
			self.gui.var_current_fps.set("0.00 fps")
			self.gui.var_real_time.set(self.sec2fmt())
			self.gui.var_file_name.set(file_path.split("/")[-1][:-4])
			self.gui.button_record.config(state="normal", text="■")  # 启用按钮
			self.gui.label_state.config(textvariable=self.gui.var_record_time, fg="black")

			self.timer = time.time()  # 计时器
			self.count = 0  # 计数器
			self.gui.root.after(1, func=self.core)  # 核心函数
		else:
			self.gui.flag_record = -self.gui.delay  # 重置运行标志

	def shot(self):  # 抓取屏幕
		rgb = ImageGrab.grab()  # 抓取屏幕快照
		bgr = cv2.cvtColor(np.asarray(rgb), cv2.COLOR_RGB2BGR)  # rgb格式转换为opencv的bgr格式
		self.video.write(bgr)  # 将屏幕快照添加至视频中

	@staticmethod
	def sec2fmt(sec=0):  # 格式化秒数
		if sec == 0:
			return "00:00:00"
		hour = int(sec / 3600)
		minute = int((sec % 3600) / 60)
		second = int(sec % 60)
		return f"{hour:02}:{minute:02}:{second:02}"

	def run(self):  # 运行
		self.gui.init_root()
		self.gui.init_state()
		self.gui.root.mainloop()


class GUI:
	def __init__(self, funcs, defaults):
		self.record, = funcs  # 录制函数
		self.folder, self.fps, self.delay, self.duration = defaults  # 默认参数
		self.root = tk.Tk()  # 主窗口

		'''主窗口'''
		self.var_record_time = tk.StringVar()  # 当前录制时长
		self.var_current_fps = tk.StringVar()  # 当前平均帧率
		self.var_real_time = tk.StringVar()  # 实际录制时长
		self.var_file_name = tk.StringVar()  # 文件名
		self.flag_record = 0  # 运行标志
		self.button_record = None  # 录制按钮

		'''状态窗口'''
		self.var_countdown = tk.StringVar()  # 倒计时
		self.label_state = None  # 倒计时标签

		'''设置窗口'''
		self.var_folder = tk.StringVar()  # 保存目录
		self.var_fps = tk.StringVar()  # 帧率
		self.var_delay = tk.StringVar()  # 准备时长
		self.var_duration = tk.StringVar()  # 录制时长
		self.flag_setup = 0  # 设置窗口标志

	def init_root(self):  # 初始化主窗口
		self.root.title(f"录屏工具")  # 设置标题
		self.root.geometry("+1200+600")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸

		'''参数'''
		self.var_record_time.set("00:00:00")
		self.var_current_fps.set("0.00 fps")
		self.var_real_time.set("00:00:00")
		self.var_file_name.set("")
		self.flag_record = -self.delay

		'''按钮'''
		self.button_record = tk.Button(self.root, text="●", fg="red", font=("",))
		self.button_record.config(command=self.record)
		self.button_record.grid(row=5, column=0, columnspan=2)

		'''标签'''
		tk.Label(self.root, text="当前录制时长: ").grid(row=1, column=0)
		tk.Label(self.root, text="当前平均帧率: ").grid(row=2, column=0)
		tk.Label(self.root, text="实际录制时长: ").grid(row=3, column=0)
		tk.Label(self.root, text="文件名: ").grid(row=4, column=0)
		tk.Label(self.root, textvariable=self.var_record_time, width=20).grid(row=1, column=1)
		tk.Label(self.root, textvariable=self.var_current_fps, width=20).grid(row=2, column=1)
		tk.Label(self.root, textvariable=self.var_real_time, width=20).grid(row=3, column=1)
		tk.Label(self.root, textvariable=self.var_file_name, width=20).grid(row=4, column=1)

		'''菜单'''
		menu_bar = tk.Menu(self.root)  # 菜单栏
		menu_main = tk.Menu(menu_bar, tearoff=False)
		menu_main.add_command(label="设置", command=self.init_setup)
		menu_bar.add_cascade(label="菜单", menu=menu_main)  # 添加至菜单栏
		self.root["menu"] = menu_bar  # 添加至主窗口

	def init_state(self):  # 初始化状态窗口
		state = tk.Toplevel()  # 状态窗口
		state.overrideredirect(True)  # 隐藏标题栏
		state.geometry("+750+0")  # 设置位置
		state.resizable(0, 0)  # 禁止拉伸
		state.attributes("-topmost", True)  # 设置保持前端显示

		'''参数'''
		self.var_countdown.set("00:00:00")

		'''标签'''
		self.label_state = tk.Label(state, textvariable=self.var_countdown)
		self.label_state.grid(row=0, column=0)

	def init_setup(self):  # 初始化设置窗口
		def terminate():  # 终结
			self.flag_setup = 0  # 重置设置窗口标志
			setup.destroy()

		def submit():  # 确认
			if os.path.exists(self.var_folder.get()):
				self.folder = self.var_folder.get()
			if self.var_fps.get().isdigit() and 10 <= int(self.var_fps.get()) <= 25:
				self.fps = int(self.var_fps.get())
			if self.var_delay.get().isdigit() and 0 <= int(self.var_delay.get()) <= 5:
				self.delay = int(self.var_delay.get())
				self.flag_record = -self.delay
			if self.var_duration.get().isdigit() and 0 <= int(self.var_duration.get()) <= 60:
				self.duration = int(self.var_duration.get())
			terminate()

		def select_folder():  # 选择保存目录
			folder = askdirectory()
			if folder:
				self.var_folder.set(folder)

		if not self.flag_setup and self.flag_record != 1:
			self.flag_setup = 1  # 激活设置窗口标志

			setup = tk.Toplevel()  # 设置窗口
			setup.protocol("WM_DELETE_WINDOW", terminate)  # 绑定关闭事件
			setup.title("设置")  # 设置标题
			setup.geometry("+1200+400")  # 设置位置
			setup.resizable(0, 0)  # 禁止拉伸

			'''参数'''
			self.var_folder.set(self.folder)
			self.var_fps.set(self.fps)
			self.var_delay.set(self.delay)
			self.var_duration.set(self.duration)

			'''按钮'''
			tk.Button(setup, text="选择目录", command=select_folder).grid(row=0, column=2, columnspan=2)
			tk.Button(setup, text="确定", command=submit).grid(row=4, column=2)
			tk.Button(setup, text="取消", command=terminate).grid(row=4, column=3)

			'''单文本框'''
			tk.Entry(setup, textvariable=self.var_folder).grid(row=0, column=1)
			tk.Entry(setup, textvariable=self.var_fps).grid(row=1, column=1)
			tk.Entry(setup, textvariable=self.var_delay).grid(row=2, column=1)
			tk.Entry(setup, textvariable=self.var_duration).grid(row=3, column=1)

			'''标签'''
			tk.Label(setup, text="保存至").grid(row=0, column=0)
			tk.Label(setup, text="帧率").grid(row=1, column=0)
			tk.Label(setup, text="准备时长").grid(row=2, column=0)
			tk.Label(setup, text="录制时长").grid(row=3, column=0)
			tk.Label(setup, text="(10-25)fps").grid(row=1, column=2, columnspan=2)
			tk.Label(setup, text="(0-5)秒").grid(row=2, column=2, columnspan=2)
			tk.Label(setup, text="(0-60)分钟").grid(row=3, column=2, columnspan=2)


if __name__ == "__main__":
	video_recorder = VideoRecorder()
	video_recorder.run()
