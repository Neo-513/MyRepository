import collections
import jieba
import json


def myprint(items):
	"""迭代打印
	:param items: 待打印集合
	"""
	if isinstance(items, dict):
		if items:  # 判断是否为空
			max_len = max(map(lambda x: len(str(x)), items))  # 列表元素最大长度
			for k, v in items.items():
				print(f"{k:<{max_len + 4}}{v}")
	else:
		for item in items:
			print(item)


def mysort(items, idx, reverse=True):
	"""排序集合
	:param items: 待排序集合
	:param idx: 按第几个元素排序
	:param reverse: 是否倒序（可选）
	:return: 排序后的集合
	"""
	if isinstance(items, list):
		items.sort(key=lambda x: x[idx], reverse=reverse)
	elif isinstance(items, dict):
		return dict(sorted(items.items(), key=lambda x: x[idx], reverse=reverse))


def replace_all(string, rplcs):
	"""替换字符串的关键字
	:param string: 待替换字符串
	:param rplcs: 替换关键字字典（若传入一个列表则默认替换为""）
	:return: 替换后的字符串
	"""
	if isinstance(rplcs, list):
		dic = {rplc: "" for rplc in rplcs}
	else:
		dic = rplcs
	for d in dic:
		string = string.replace(d, dic[d])
	return string


def lst2dic(lst):
	"""统计列表元素个数
	:param lst: 待统计元素的列表
	:return: 键名为列表元素、键值为该元素个数的字典（按元素个数倒序）
	"""
	dic = dict(collections.Counter(lst))  # 列表转为计数字典
	return mysort(dic, 1)  # 对字典按值排序


def jsn2dic(jsn):
	"""将json字符串转为json字典
	:param jsn: 待转换json字符串
	:return: 转换后的json字典
	"""
	dic = {"null": "None", "true": "True", "false": "False"}
	jsn = replace_all(jsn, dic)  # 去除特殊字符影响
	return eval(jsn)


def beautify_dic(dic):
	"""格式化打印字典
	:param dic: 待格式化打印字典
	"""
	print(json.dumps(dic, indent=4, ensure_ascii=False))


def analyze_nlp(kws):
	"""对中文进行分词
	:param kws: 待分词列表
	:return: 键名为分词、键值为个数的字典
	"""
	keywords = sum(map(lambda x: jieba.lcut(x), kws), [])
	return lst2dic(keywords)
