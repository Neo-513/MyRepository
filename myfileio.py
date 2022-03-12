import csv


def read(path, encoding="utf-8", trace=False):
	"""读取文件
	:param path: 文件路径
	:param encoding: 文件编码
	:param trace: 打印信息
	:return: 文件内容队列
	"""
	filetype = path.split(".")[-1]  # 文件类型
	if trace:
		print(f"[READ]    {path}")  # 打印读取信息
	with open(path, mode="r", encoding=encoding) as file:
		if filetype == "csv":
			data = [[r for r in reader] for reader in csv.reader(file)]
			if len(data) == 1:  # 一维列表
				data = data[0]
		else:
			data = file.read()
	return data


def write(path, data, encoding="utf-8", trace=False):
	"""写入文件
	:param path: 文件路径
	:param data: 文件数据
	:param encoding: 文件编码
	:param trace: 打印信息
	:return:
	"""
	filetype = path.split(".")[-1]  # 文件类型
	if trace:
		print(f"[WRITE]    {path}")
	with open(path, mode="w", encoding=encoding, newline="") as file:
		if filetype == "csv":
			if not isinstance(data[0], list):  # 一维列表
				data = [data]
			csv.writer(file).writerows(data)
		else:
			file.write(data)
