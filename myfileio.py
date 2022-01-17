import aiofiles
import asyncio
import csv


def read(paths, encoding="utf-8", trace=False):
	"""
	异步读取文件列表（文件类型必须一致）
	:param paths: 文件路径队列（支持单个文件路径）
	:param encoding: 文件编码
	:param trace: 打印信息
	:return: 文件内容队列
	"""
	return asyncio.run(_main(encoding, trace, paths))


def write(paths, datas, encoding="utf-8", trace=False):
	"""
	异步写入文件列表（文件类型必须一致）
	:param paths: 文件路径队列（支持单个文件路径）
	:param datas: 文件内容队列（支持单个文件内容）
	:param encoding: 文件编码
	:param trace: 打印信息
	:return:
	"""
	asyncio.run(_main(encoding, trace, paths, datas))


async def _main(encoding, trace, paths, datas=None):  # 执行队列（外部不可调用）
	if not isinstance(paths, list):  # 单个文件路径
		paths = [paths]
		if datas:
			datas = [datas]
	file_type = paths[0].split(".")[-1]  # 文件类型
	if not all(map(lambda x: x.split(".")[-1] == file_type, paths)):  # 文件类型不一致
		return print("[TYPE ERROR]")
	if datas:
		if len(paths) != len(datas):  # 文件路径队列和文件内容队列长度不一致
			return print("[LENGTH ERROR]")

	params = (
		file_type,  # 文件类型
		encoding,  # 编码
		{},  # 内容字典
		trace  # 打印信息
	)
	if datas:
		func, tasks = _write, [(path, datas[i]) for i, path in enumerate(paths)]
	else:
		func, tasks = _read, paths
	await asyncio.gather(*[asyncio.ensure_future(func(task, params)) for task in tasks])

	if not datas:
		if len(paths) == 1:  # 单个文件路径
			return params[2][paths[0]]
		else:
			return [params[2][path] for path in paths]  # 按序返回文件内容


async def _read(path, params):  # 读取单个文件（外部不可调用）
	if params[0] == "csv":
		with open(path, mode="r", encoding=params[1]) as f:
			datas = [[r for r in reader] for reader in csv.reader(f)]
			if len(datas[0]) == 1:  # 一维列表
				datas = [data[0] for data in datas]
	else:
		async with aiofiles.open(path, mode="r", encoding="utf-8") as f:
			datas = await f.read()
			if params[0] == "txt":
				datas = datas.split("\n")
	params[2][path] = datas
	if params[3]:
		print(f"READ: {path}")


async def _write(task, params):  # 写入单个文件（外部不可调用）
	path, data = task
	if params[0] == "csv":
		with open(path, mode="w", encoding=params[1], newline="") as f:
			if not isinstance(data[0], list):  # 一维列表
				data = [[d] for d in data]
			csv.writer(f).writerows(data)
	else:
		async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
			if not isinstance(data, str):
				data = str(data)
			await f.write(data)
	if params[2]:
		print(f"READ: {path}")
