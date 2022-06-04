import pyautogui
import tkinter as tk


class MousePosition:
	def __init__(self):
		self.gui = GUI()

	def get_position(self):  # 获取当前位置
		x, y = pyautogui.position()
		self.gui.var_position.set(f"({x:04},{y:03})")
		self.gui.root.after(1, self.get_position)

	def run(self):  # 运行
		self.gui.init_root()
		self.get_position()
		self.gui.root.mainloop()


class GUI:
	def __init__(self):
		self.root = tk.Tk()  # 主窗口

		'''主窗口'''
		self.var_position = tk.StringVar()  # 当前时间

	def init_root(self):  # 初始化主窗口
		self.root.overrideredirect(True)  # 隐藏标题栏
		self.root.geometry("+950+0")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸
		self.root.attributes("-topmost", True)  # 设置保持前端显示

		'''标签'''
		tk.Label(self.root, textvariable=self.var_position).grid(row=0, column=1)


if __name__ == "__main__":
	mouseposition = MousePosition()
	mouseposition.run()
