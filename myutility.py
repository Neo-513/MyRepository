import collections
import csv
import demjson
import jieba
import json
import time


def read(path):
	"""
	读文件
	:param path: 文件路径
	:return: 文件内容
	"""
	print(f"READ: {path}")
	file_type = path.split(".")[-1]  # 文件类型
	encoding = "gbk" if file_type == "csv" else "utf-8"  # 编码

	with open(path, mode="r", encoding=encoding) as f:
		if file_type == "txt":
			datas = f.read().split("\n")
		elif file_type == "csv":
			datas = [[r for r in reader] for reader in csv.reader(f)]
			if len(datas[0]) == 1:  # 一维列表
				datas = [data[0] for data in datas]
		elif file_type == "json":
			datas = demjson.decode(f.read())
	return datas


def write(path, datas):
	"""
	写文件
	:param path: 文件路径
	:param datas: 文件内容
	:return:
	"""
	print(f"WRITE: {path}")
	file_type = path.split(".")[-1]  # 文件类型
	encoding = "gbk" if file_type == "csv" else "utf-8"  # 编码

	with open(path, mode="w", encoding=encoding, newline="") as f:
		if file_type == "txt":
			f.write(datas)
		elif file_type == "csv":
			if not isinstance(datas[0], list):  # 一维列表
				datas = [[data] for data in datas]
			csv.writer(f).writerows(datas)
		elif file_type == "json":
			f.write(demjson.encode(datas))


def mysort(items, idx=0, reverse=True):
	"""
	排序集合
	:param items: 待排序集合
	:param idx: 按第几个元素排序
	:param reverse: 是否倒序（可选）
	:return: 排序后的集合
	"""
	if isinstance(items, list):
		items.sort(key=lambda x: x[idx], reverse=reverse)
		return items
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


def str2dic(string):
	"""
	将json字符串转为json字典
	:param string: 待转换字符串
	:return: 转换后的json字典
	"""
	dic = {"null": "None", "true": "True", "false": "False"}
	for d in dic:
		string = string.replace(d, dic[d])  # 去除特殊字符影响
	return eval(string)


def beautify_dic(dic):
	"""
	格式化打印json字典
	:param dic: json字典（json字符串自动转换为json字典）
	:return:
	"""
	if isinstance(dic, str):
		dic = str2dic(dic)
	print(json.dumps(dic, indent=4, ensure_ascii=False))


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


def timing(func):
	"""
	统计函数执行时间（装饰器）
	:param func: 待执行函数
	:return: 回调函数
	"""
	def callback(*args, **kwargs):
		"""
		回调函数
		:param args: 传递参数
		:param kwargs: 传递参数
		:return: 回调函数返回值
		"""
		timer = time.time()  # 计时器
		datas = func(*args, **kwargs)  # 执行函数
		print(f"TIMING: {time.time() - timer}")
		return datas
	return callback


def analyze_nlp(kws):
	"""
	对中文进行分词
	:param kws: 待分词列表
	:return: 键名为分词、键值为个数的字典
	"""
	keywords = sum(map(lambda x: jieba.lcut(x), kws), [])
	return lst2dic(keywords)
