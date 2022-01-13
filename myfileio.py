import aiofiles
import asyncio
import csv


class MyFileIO:
	def __init__(self, trace=False):
		self.trace = trace  # 打印信息

	def read(self, paths, encoding="utf-8"):
		"""
		异步读取文件列表（文件类型必须一致）
		:param paths: 文件路径队列（支持单个文件路径）
		:param encoding: 文件编码
		:return: 文件内容队列
		"""
		return asyncio.run(self._main(encoding, paths))

	def write(self, paths, datas, encoding="utf-8"):
		"""
		异步写入文件列表（文件类型必须一致）
		:param paths: 文件路径队列（支持单个文件路径）
		:param datas: 文件内容队列（支持单个文件内容）
		:param encoding: 文件编码
		:return:
		"""
		asyncio.run(self._main(encoding, paths, datas))

	async def _main(self, encoding, paths, datas=None):  # 执行队列（外部不可调用）
		if isinstance(paths, str):  # 单个文件路径
			paths = [paths]
		file_type = paths[0].split(".")[-1]  # 文件类型
		if not all(map(lambda x: x.split(".")[-1] == file_type, paths)):  # 文件类型不一致
			return print("[TYPE ERROR]")
		if datas and len(paths) != len(datas):  # 文件路径队列和文件内容队列长度不一致
			return print("[LENGTH ERROR]")

		params = (
			file_type,  # 文件类型
			encoding,  # 编码
			{},  # 内容字典
			self.trace  # 打印信息
		)
		func = self._write if datas else self._read
		tasks = [(path, datas[i]) if datas else paths[i] for i, path in enumerate(paths)]
		await asyncio.gather(*[asyncio.ensure_future(func(task, params)) for task in tasks])

		if not datas:
			if len(paths) == 1:  # 单个文件路径
				return params[2][paths[0]]
			else:
				return [params[2][path] for path in paths]  # 按序返回文件内容

	@staticmethod
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

	@staticmethod
	async def _write(task, params):  # 写入单个文件（外部不可调用）
		path, datas = task
		if params[0] == "csv":
			with open(path, mode="w", encoding=params[1], newline="") as f:
				if not isinstance(datas[0], list):  # 一维列表
					datas = [[data] for data in datas]
				csv.writer(f).writerows(datas)
		else:
			async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
				if not isinstance(datas, str):
					datas = str(datas)
				await f.write(datas)
		if params[2]:
			print(f"READ: {path}")
