import collections
import jieba
import json


def myprint(items, trace=True, tab=False):
	"""迭代打印
	:param items: 待打印集合
	:param trace: 是否打印信息
	:param tab: 是否使用tab进行连接
	"""
	if items:  # 判断是否为空
		if isinstance(items, dict):
			if tab:
				for k, v in items.items():
					print(f"{k}\t{v}")
			else:
				max_len = max(map(lambda x: len(str(x)), items))  # 列表元素最大长度
				for k, v in items.items():
					print(f"{k:<{max_len + 4}}{v}")
		else:
			for item in items:
				print(item)
		if trace:
			print(f"[COUNT]    {len(items)}")


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
	for d in dic:
		jsn = jsn.replace(d, dic[d])
	return eval(jsn)


def beautify_dic(dic):
	"""格式化打印字典
	:param dic: 待格式化打印字典
	"""
	print(json.dumps(dic, indent=4, ensure_ascii=False))


def default_dic(item_type):
	"""获取含有默认数据类型的字典
	:param item_type: 默认数据类型
	:return: 含有默认数据类型的字典
	"""
	return collections.defaultdict(item_type)


def analyze_nlp(kws):
	"""对中文进行分词
	:param kws: 待分词列表
	:return: 键名为分词、键值为个数的字典
	"""
	keywords = sum(map(lambda x: jieba.lcut(x), kws), [])
	return lst2dic(keywords)
