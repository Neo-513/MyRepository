from PIL import ImageGrab
from tkinter.filedialog import askdirectory
import cv2
import numpy as np
import os
import pyaudio
import time
import tkinter as tk
# import wave


class Recorder:
	"""视频默认参数"""
	FOURCC = cv2.VideoWriter_fourcc(*"mp4v")  # mp4编码器
	FPS = 15  # 帧率（通过计算近似所得）
	FRAME_SIZE = ImageGrab.grab().size  # 屏幕尺寸

	"""音频默认参数"""
	CHANNELS = 1  # 单声道
	FORMAT = pyaudio.paInt16  # 采样位数
	RATE = 44100  # 采样频率
	BUFFER = 1024  # 缓冲区帧数

	def __init__(self):
		self.gui = GUI(self.func_record)
		self.video = None
		# self.video, self.audio, self.stream, self.pa = None, None, None, None  # 视频音频相关资源
		# self.datas = None

	def func_record(self):  # 录制
		if not self.gui.flag_record:
			self.gui.flag_record = 1  # 激活运行标志

			filepath = f"{self.gui.folder.rstrip('/')}/{time.strftime('%Y%m%d%H%M%S', time.localtime())}"  # 文件路径
			self.video = cv2.VideoWriter(f"{filepath}.mp4", fourcc=self.FOURCC, fps=self.FPS, frameSize=self.FRAME_SIZE)
			'''self.pa = pyaudio.PyAudio()  # 创建对象
			a = time.time()
			self.stream = self.pa.open(
				channels=self.CHANNELS, format=self.FORMAT, rate=self.RATE, frames_per_buffer=self.BUFFER, input=True
			)
			print(time.time() - a, a - s)
			self.video, self.audio = self.get_resource(filepath)'''
			self.count_down(filepath)  # 倒计时

			timer = time.time()  # 计时器
			count = 0  # 计数器
			while self.gui.flag_record:
				img = self.shot()
				self.video.write(img)  # 将屏幕快照添加至视频中

				if count % self.gui.fps == 0:  # 每隔固定帧数刷新信息
					current_time = time.time() - timer  # 当前所计时间
					'''标签赋值'''
					self.gui.var_record_time.set(self.gui.sec2msg(count / self.gui.fps))
					self.gui.var_current_fps.set(f"{(count / current_time):.2f} fps")
					self.gui.var_real_time.set(self.gui.sec2msg(current_time))
				count += 1
				if count >= self.gui.fps * self.gui.duration * 60:
					self.terminate()
		else:
			self.terminate()

	def terminate(self):  # 录制终结
		self.gui.flag_record = 0  # 重置运行标志
		self.gui.var_record.set("●")
		self.gui.label_state.config(fg="blue")
		self.video.release()  # 释放视频资源
		'''
		self.audio.close()  # 关闭音频文件
		self.stream.stop_stream()  # 停止流
		self.stream.close()  # 关闭流
		self.pa.terminate()  # 终结对象
		'''

	def count_down(self, filepath):  # 倒计时
		self.gui.var_record_time.set(self.gui.sec2msg())
		self.gui.var_current_fps.set("0.00 fps")
		self.gui.var_real_time.set(self.gui.sec2msg())
		self.gui.var_filename.set(filepath.split("/")[-1])
		self.gui.var_record.set("■")

		if self.gui.delay > 0:
			self.gui.label_state.config(textvariable=self.gui.var_delay, fg="red")
			self.gui.button_record.config(state="disabled")  # 禁用按钮
			for i in range(self.gui.delay, 0, -1):
				self.gui.var_delay.set(self.gui.sec2msg(self.gui.delay))
				time.sleep(1)
			self.gui.button_record.config(state="normal")  # 启用按钮
		self.gui.label_state.config(textvariable=self.gui.var_record_time, fg="black")  # 录屏计时

	@staticmethod
	def shot():  # 抓取屏幕
		rgb = ImageGrab.grab()  # 抓取屏幕快照
		bgr = cv2.cvtColor(np.asarray(rgb), cv2.COLOR_RGB2BGR)  # rgb格式转换为opencv的bgr格式
		return bgr

	'''def get_resource(self, filepath):  # 创建视频音频资源
		video = cv2.VideoWriter(f"{filepath}.mp4", fourcc=self.FOURCC, fps=self.FPS, frameSize=self.FRAME_SIZE)
		audio = wave.open(f"{filepath}.wav", "wb")  # 音频
		audio.setnchannels(self.CHANNELS)  # 设置声道
		audio.setsampwidth(self.pa.get_sample_size(self.FORMAT))  # 设置采样位数
		audio.setframerate(self.RATE)  # 设置采样频率
		return video, audio'''

	def run(self):  # 运行
		self.gui.init_root()
		self.gui.init_state()
		self.gui.root.mainloop()


class GUI:
	FOLDER = "D:/1"  # "C:/Users/Dell/Desktop"
	FPS = 15
	DELAY = 0  # 3
	DURATION = 1  # 60
	VERSION = "v1.4"

	def __init__(self, func_record):
		self.func_record = func_record  # 录制函数
		self.root = tk.Tk()  # 主窗口
		self.flag_record, self.flag_setup = 0, 0  # 运行标志、设置窗口标志

		'''主窗口'''
		self.var_record_time = tk.StringVar()  # 当前录制时长
		self.var_current_fps = tk.StringVar()  # 当前平均帧率
		self.var_real_time = tk.StringVar()  # 实际录制时长
		self.var_filename = tk.StringVar()  # 文件名
		self.var_record = tk.StringVar()  # 录制按钮文本
		self.button_record = None
		self.button_record = tk.Button(self.root, command=self.func_record)  # 录制按钮

		'''状态窗口'''
		self.label_state = None  # 倒计时标签

		'''设置窗口'''
		self.var_folder = tk.StringVar()  # 保存目录
		self.var_fps = tk.StringVar()  # 帧率
		self.var_delay = tk.StringVar()  # 准备时间
		self.var_duration = tk.StringVar()  # 录制时长
		self.folder = self.FOLDER  # 保存目录
		self.fps = self.FPS  # 帧率
		self.delay = self.DELAY  # 准备时间
		self.duration = self.DURATION  # 录制时长

	def init_root(self):  # 初始化主窗口
		self.root.title(f"录屏工具 {self.VERSION}")  # 设置标题
		self.root.geometry("+1200+600")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸

		'''可变参数'''
		self.var_record_time.set(self.sec2msg())
		self.var_current_fps.set("0.00 fps")
		self.var_real_time.set(self.sec2msg())
		self.var_record.set("●")

		'''按钮'''
		self.button_record.config(textvariable=self.var_record, fg="red", font=("",))
		self.button_record.grid(row=5, column=0, columnspan=2)

		'''标签'''
		tk.Label(self.root, text="当前录制时长: ").grid(row=1, column=0)
		tk.Label(self.root, text="当前平均帧率: ").grid(row=2, column=0)
		tk.Label(self.root, text="实际录制时长: ").grid(row=3, column=0)
		tk.Label(self.root, text="文件名: ").grid(row=4, column=0)
		tk.Label(self.root, textvariable=self.var_record_time, width=20).grid(row=1, column=1)
		tk.Label(self.root, textvariable=self.var_current_fps, width=20).grid(row=2, column=1)
		tk.Label(self.root, textvariable=self.var_real_time, width=20).grid(row=3, column=1)
		tk.Label(self.root, textvariable=self.var_filename, width=20).grid(row=4, column=1)

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

		'''标签'''
		self.label_state = tk.Label(state, text=self.sec2msg())
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
			if self.var_duration.get().isdigit() and 0 <= int(self.var_duration.get()) <= 60:
				self.duration = int(self.var_duration.get())
			terminate()

		def select_folder():  # 选择保存目录
			folder = askdirectory()
			if folder:
				self.var_folder.set(folder)

		if not self.flag_setup and not self.flag_record:
			self.flag_setup = 1  # 激活设置窗口标志

			setup = tk.Toplevel()  # 设置窗口
			setup.protocol("WM_DELETE_WINDOW", terminate)  # 绑定关闭事件
			setup.title("设置")  # 设置标题
			setup.geometry("+1200+400")  # 设置位置
			setup.resizable(0, 0)  # 禁止拉伸

			'''可变参数'''
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
			tk.Label(setup, text="准备时间").grid(row=2, column=0)
			tk.Label(setup, text="录制时长").grid(row=3, column=0)
			tk.Label(setup, text="(10-25)fps").grid(row=1, column=2, columnspan=2)
			tk.Label(setup, text="(0-5)秒").grid(row=2, column=2, columnspan=2)
			tk.Label(setup, text="(0-60)分钟").grid(row=3, column=2, columnspan=2)

	@staticmethod
	def sec2msg(sec=0):  # 格式化秒数
		if sec == 0:
			return "00:00:00"
		hour = int(sec / 3600)
		minute = int((sec % 3600) / 60)
		second = int(sec % 60)
		return f"{hour:02}:{minute:02}:{second:02}"


if __name__ == "__main__":
	recorder = Recorder()
	recorder.run()
