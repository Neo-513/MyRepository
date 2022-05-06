import base64
import tkinter as tk


class WorkUtil:
	def __init__(self):
		funcs = (self.quote, self.unquote, self.upper, self.encode, self.decode, self.clear)
		self.gui = GUI(funcs)

	def quote(self):  # 加引号
		text_input = self.gui.text_input.get(1.0, tk.END)[:-1]
		lines = [f"\"{line.rstrip()}\"" for line in text_input.split("\n")]
		text_output = "\n".join(lines) + ";"
		self.gui.text_output.delete(1.0, tk.END)
		self.gui.text_output.insert(1.0, text_output)

	def unquote(self):  # 去引号
		text_input = self.gui.text_input.get(1.0, tk.END)[:-1]
		lines = [line.rstrip(";").rstrip().strip("\t").strip("\"") for line in text_input.split("\n")]
		text_output = "\n".join(lines)
		self.gui.text_output.delete(1.0, tk.END)
		self.gui.text_output.insert(1.0, text_output)

	def upper(self):  # 大写
		text_input = self.gui.text_input.get(1.0, tk.END)[:-1]
		text_output = text_input.rstrip().upper()
		self.gui.text_output.delete(1.0, tk.END)
		self.gui.text_output.insert(1.0, text_output)

	def encode(self):  # base64加密
		text_input = self.gui.text_input.get(1.0, tk.END)[:-1]
		text_output = base64.b64encode(bytes(text_input.strip(), "utf-8"))
		self.gui.text_output.delete(1.0, tk.END)
		self.gui.text_output.insert(1.0, text_output)

	def decode(self):  # base64解密
		text_input = self.gui.text_input.get(1.0, tk.END)[:-1]
		text_output = str(base64.b64decode(text_input.strip()))[2:-1]
		self.gui.text_output.delete(1.0, tk.END)
		self.gui.text_output.insert(1.0, text_output)

	def clear(self):  # 清空
		self.gui.text_input.delete(1.0, tk.END)
		self.gui.text_output.delete(1.0, tk.END)

	def run(self):  # 运行
		self.gui.init_root()
		self.gui.root.mainloop()


class GUI:
	def __init__(self, funcs):
		self.funcs = funcs  # 函数集合
		self.root = tk.Tk()  # 主窗口

		'''主窗口'''
		self.text_input, self.text_output = None, None  # 文本框

	def init_root(self):  # 初始化主窗口
		self.root.title("后台常用功能")  # 设置标题
		self.root.geometry(f"+700+400")  # 设置位置
		self.root.resizable(0, 0)  # 禁止拉伸

		'''按钮'''
		tk.Button(self.root, text="加引号", command=self.funcs[0], bg="skyblue", width=10).grid(row=1, column=10)
		tk.Button(self.root, text="去引号", command=self.funcs[1], bg="skyblue", width=10).grid(row=2, column=10)
		tk.Button(self.root, text="大写", command=self.funcs[2], bg="skyblue", width=10).grid(row=3, column=10)
		tk.Button(self.root, text="base64加密", command=self.funcs[3], bg="skyblue", width=10).grid(row=4, column=10)
		tk.Button(self.root, text="base64解密", command=self.funcs[4], bg="skyblue", width=10).grid(row=5, column=10)
		tk.Button(self.root, text="清空", command=self.funcs[5], bg="skyblue", width=10).grid(row=6, column=10)

		'''标签'''
		tk.Label(self.root, text="输入").grid(row=0, column=0)
		tk.Label(self.root, text="输出").grid(row=0, column=11)

		'''文本框'''
		self.text_input = tk.Text(self.root, width=50)
		self.text_input.grid(row=1, column=0, rowspan=7, columnspan=10)
		self.text_output = tk.Text(self.root, width=50)
		self.text_output.grid(row=1, column=11, rowspan=7, columnspan=10)


if __name__ == "__main__":
	workutil = WorkUtil()
	workutil.run()
