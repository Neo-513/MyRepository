import threading
import time


def timing(func):
	"""统计函数执行时间
	:param func: 待执行函数
	:return: 装饰器函数
	"""
	def inner(*args):  # 内部函数
		timer = time.time()  # 计时器
		datas = func(*args)  # 执行函数
		print(f"[TIMING]    {time.time() - timer}")
		return datas
	return inner


def loading(timeout):
	"""多线程打印加载进度条（该函数之后不应再执行其他命令且函数内部不含打印命令）
	:param timeout: 预计执行时间
	:return: 装饰器函数
	"""
	def sec2str(sec):  # 格式化秒数
		minute, second = divmod(sec, 60)
		hour, minute = divmod(minute, 60)
		return f"{hour:02}:{minute:02}:{second:02}"

	def show_process_bar():  # 显示进度条
		freq = 4
		for i in range(timeout * freq + 1):
			rate = i / (timeout * freq)  # 执行率
			block = int(rate * 50)  # 实心方块数

			current_time = f"[{sec2str(int(i / freq))}]"  # 已执行时间
			process_bar = f"{'■' * block}{'□' * (50 - block)}"  # 进度条
			percentage = f"{rate * 100:>6.2f}%"  # 百分比

			print(f"\r{current_time} {process_bar} {percentage}", end="")
			time.sleep(1 / freq)

	def decorator(func):  # 装饰器函数
		def callback(*args):  # 回调函数
			thread1 = threading.Thread(target=func, args=args)
			thread2 = threading.Thread(target=show_process_bar)
			thread1.start()
			thread2.start()
		return callback
	return decorator
