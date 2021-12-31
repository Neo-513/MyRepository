import collections
import csv
import demjson
import jieba
import json
import time


def read(path):  # 读文件
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


def write(path, datas):  # 写文件
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


def mysort(items, idx=0, reverse=True):  # 排序列表和字典
	if isinstance(items, list):
		items.sort(key=lambda x: x[idx], reverse=reverse)
		return items
	elif isinstance(items, dict):
		return dict(sorted(items.items(), key=lambda x: x[idx], reverse=reverse))


def lst2dic(lst):  # 统计列表元素个数
	dic = dict(collections.Counter(lst))  # 列表转为计数字典
	return mysort(dic, 1)  # 对字典按值排序


def str2dic(string):  # 字符串转为字典
	dic = {"null": "None", "true": "True", "false": "False"}
	for d in dic:
		string = string.replace(d, dic[d])
	return eval(string)


def beautify_dic(dic):  # 格式化打印字典
	if isinstance(dic, str):
		dic = str2dic(dic)
	print(json.dumps(dic, indent=4, ensure_ascii=False))


def myprint(items):  # 迭代打印
	if isinstance(items, dict):
		max_len = max(map(lambda x: len(str(x)), items))  # 列表元素最大长度
		for k, v in items.items():
			print(f"{k:<{max_len + 4}}{v}")
	else:
		for item in items:
			print(item)


def timing(func):  # 统计时间
	def callback(*args, **kwargs):  # 回调函数
		timer = time.time()  # 计时器
		datas = func(*args, **kwargs)  # 执行函数
		print(f"TIMING: {time.time() - timer}")
		return datas
	return callback


def analyze_nlp(kws):  # 中文分词
	keywords = sum(map(lambda x: jieba.lcut(x), kws), [])
	return lst2dic(keywords)
