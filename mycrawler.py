import aiofiles
import aiohttp
import asyncio
import math
import os
import re
import time


class MyCrawler:
	HEADERS = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0."
		"4664.55 Safari/537.36"
	}  # 请求头

	def __init__(self, cookie="", encoding="utf-8"):
		self.HEADERS["cookie"] = cookie
		self.encoding = encoding

	def crawl(self, urls, rgx=None, folder=""):
		"""
		爬取url列表
		:param urls: url列表（支持单个url）
		:param rgx: 正则表达式（可选）
		:param folder: 保存图片目录（可选）
		:return: 按url列表顺序的网页数据
		"""
		if isinstance(urls, str):  # 单个url
			urls = [urls]
		if (not folder and len(urls) > 12000) or (folder and len(urls) > 1000):  # 判断是否异步过载
			return print("[OVERLOAD]")
		if folder and not os.path.exists(folder):
			os.mkdir(folder)  # 新建文件夹

		params = (
			{"count": -1},  # 计数器
			math.ceil(math.log(len(urls), 10)),  # 计数器补0位数
			folder,  # 文件夹
			self.encoding,  # 编码
			re.compile(rgx, re.S) if rgx else None,  # 编译正则表达式
			{}  # url字典
		)
		asyncio.run(self._main(urls, params))  # 异步执行爬取任务列表

		if not folder:
			if len(urls) == 1:  # 单个url
				return params[5][urls[0]]
			else:
				return [params[5][url] for url in urls if url in params[5]]  # 按序返回数据

	async def _main(self, tasks, params):  # 任务列表（外部不可调用）
		timer = time.time()  # 计时器
		connector = aiohttp.TCPConnector(ssl=False)  # 取消ssl验证
		async with aiohttp.ClientSession(headers=self.HEADERS, connector=connector) as session:
			await asyncio.gather(*[asyncio.ensure_future(self._fetch((task, session), params)) for task in tasks])
		print(f"TIMER: {time.time() - timer}")  # 计时

	@staticmethod
	async def _fetch(task, params):  # 爬取单个（外部不可调用）
		url, session = task
		async with session.get(url) as response:
			params[0]["count"] += 1  # 计数
			msg = f"[{params[0]['count']:0{params[1]}}]  {params[2]}  {url}"  # url信息
			try:
				print(msg)  # 打印url信息
				response.raise_for_status()  # 判断页面连接状态
				if params[2]:  # 爬取图片
					async with aiofiles.open(f"{params[2]}/{url.split('/')[-1]}", mode="wb") as file:
						datas = await response.read()
						await file.write(datas)
				else:  # 爬取文本
					data = await response.text(encoding=params[3])
					params[5][url] = params[4].findall(data) if params[4] else data
			except Exception as e:
				print(f"{msg}    {e}")  # 打印异常信息
