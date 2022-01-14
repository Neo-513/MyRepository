import collections
import jieba
import json
import threading
import time


def myprint(items):
	"""
	迭代打印
	:param items: 待打印集合
	:return:
	"""
	if isinstance(items, dict):
		max_len = max(map(lambda x: len(str(x)), items))  # 列表元素最大长度
		for k, v in items.items():
			print(f"{k:<{max_len + 4}}{v}")
	else:
		for item in items:
			print(item)


def mysort(items, idx, reverse=True):
	"""
	排序集合
	:param items: 待排序集合
	:param idx: 按第几个元素排序
	:param reverse: 是否倒序（可选）
	:return: 排序后的集合
	"""
	if isinstance(items, list):
		items.sort(key=lambda x: x[idx], reverse=reverse)
	elif isinstance(items, dict):
		return dict(sorted(items.items(), key=lambda x: x[idx], reverse=reverse))


def lst2dic(lst):
	"""
	统计列表元素个数
	:param lst: 待统计元素的列表
	:return: 键名为列表元素、键值为该元素个数的字典（按元素个数倒序）
	"""
	dic = dict(collections.Counter(lst))  # 列表转为计数字典
	return mysort(dic, 1)  # 对字典按值排序


def jsn2dic(jsn):
	"""
	将json字符串转为json字典
	:param jsn: 待转换json字符串
	:return: 转换后的json字典
	"""
	dic = {"null": "None", "true": "True", "false": "False"}
	for d in dic:
		jsn = jsn.replace(d, dic[d])  # 去除特殊字符影响
	return eval(jsn)


def beautify_dic(dic):
	"""
	格式化打印json字典
	:param dic: json字典（json字符串自动转换为json字典）
	:return:
	"""
	if isinstance(dic, str):
		dic = jsn2dic(dic)
	print(json.dumps(dic, indent=4, ensure_ascii=False))


def timing():
	"""
	统计函数执行时间
	:return: 装饰器函数
	"""
	def decorator(func):  # 装饰器函数
		def inner(*args):  # 内部函数
			timer = time.time()  # 计时器
			datas = func(*args)  # 执行函数
			print(f"TIMING: {time.time() - timer}")
			return datas
		return inner
	return decorator


def loading(timeout):
	"""
	多线程打印加载进度条（该函数之后不应再执行其他命令且函数内部不含打印命令）
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


def analyze_nlp(kws):
	"""
	对中文进行分词
	:param kws: 待分词列表
	:return: 键名为分词、键值为个数的字典
	"""
	keywords = sum(map(lambda x: jieba.lcut(x), kws), [])
	return lst2dic(keywords)
