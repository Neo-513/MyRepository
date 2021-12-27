from tkinter.filedialog import askdirectory
import os
import tkinter as tk


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
		self.button_record = None  # 录制按钮

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
		self.button_record = tk.Button(self.root, textvariable=self.var_record, fg="red", font=("",))
		self.button_record.config(command=self.func_record)
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

	def run(self):  # 运行
		self.init_root()
		self.init_state()
		self.root.mainloop()

	@staticmethod
	def sec2msg(sec=0):  # 格式化秒数
		if sec == 0:
			return "00:00:00"
		hour = int(sec / 3600)
		minute = int((sec % 3600) / 60)
		second = int(sec % 60)
		return f"{hour:02}:{minute:02}:{second:02}"


if __name__ == "__main__":
	gui = GUI(None)
	gui.run()
