from playwright.async_api import async_playwright
import aiofiles
import aiohttp
import asyncio
import browser_cookie3
import collections
import lxml.etree
import math
import os
import re
import time


def crawl(urls, cookie=None, parser=None, attrs=None, proxy="", folder="", encoding="utf-8"):
	"""
	根据url列表进行爬取网页数据或下载图片
	:param urls: url列表
	:param cookie: 当前url对应的cookie
	:param parser: 网页解析器（正则表达式、xpath）
	:param attrs: xpath对应的属性
	:param proxy: 本机代理
	:param folder: 保存图片目录
	:param encoding: 编码
	:return: 按url列表顺序的网页数据
	"""
	params = {
		"urls": urls,
		"cookie": cookie,
		"parser": parser,
		"attrs": attrs,
		"proxy": proxy,
		"folder": folder,
		"encoding": encoding
	}

	tictoc = time.time()
	if isinstance(urls, list):
		datas = StaticCrawler(params).crawl()  # 静态爬虫
	else:
		datas = DynamicCrawler(params).crawl()  # 动态爬虫
	print(f"[CRAWLED IN]    {time.time() - tictoc}")
	return datas


def get_cookie(url):
	"""
	通过url获取当前cookie字符串
	:param url: url
	:return: cookie字符串
	"""
	return "; ".join([f"{c.name}={c.value}" for c in browser_cookie3.edge() if c.domain in url])


class StaticCrawler:
	_HEADERS = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0"
		".0.0 Safari/537.36 Edg/106.0.1370.42"
	}  # 请求头

	def __init__(self, params):
		self.urls = params["urls"]
		self.cookie = params["cookie"]
		self.parser = params["parser"]
		self.attrs = params["attrs"]
		self.proxy = params["proxy"]
		self.folder = params["folder"]
		self.encoding = params["encoding"]
		self.session = None  # session
		self.zfill = math.ceil(math.log(len(self.urls), 10))  # 计数器补0位数
		self.count = -1  # 计数器
		self.dic = collections.defaultdict(dict)  # 结果集字典

		if self.cookie:
			self._HEADERS["cookie"] = self.cookie  # cookie
		if self.parser and ".+?" in self.parser:
			self.parser = re.compile(self.parser, re.S)  # 编译正则表达式
		if self.folder and not os.path.exists(self.folder):
			os.mkdir(self.folder)  # 新建文件夹

	def crawl(self):
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # 设置策略
		asyncio.run(self._main())  # 异步执行爬取任务列表

		if not self.folder:
			return [self.dic[url] for url in self.urls if url in self.dic]  # 按url列表顺序返回数据

	async def _main(self):  # 任务列表
		connector = aiohttp.TCPConnector(ssl=False)  # 取消ssl验证
		async with aiohttp.ClientSession(headers=self._HEADERS, connector=connector) as session:
			self.session = session  # session
			tasks = [asyncio.ensure_future(self._fetch(url)) for url in self.urls]  # 任务列表
			await asyncio.gather(*tasks)  # 异步执行任务列表

	async def _fetch(self, url):  # 爬取单个url
		async with await self.session.get(url, proxy=self.proxy) as response:
			self.count += 1  # 计数
			print(f"[{self.count:0{self.zfill}}]  {self.folder}  {url}")  # 打印url信息
			response.raise_for_status()  # 判断页面连接状态

			if self.folder:  # 爬取图片
				async with await aiofiles.open(f"{self.folder.rstrip('/')}/{url.split('/')[-1]}", mode="wb") as file:
					data = await response.read()  # 获取图片内容
					await file.write(data)  # 写入图片文件
			else:  # 爬取文本
				data = await response.text(encoding=self.encoding)  # 获取网页所有源码
				if self.parser:
					if isinstance(self.parser, re.Pattern):
						self.dic[url] = self.parser.findall(data)  # 通过正则表达式搜索
					else:
						nodes = lxml.etree.HTML(data).xpath(self.parser)  # 获取节点
						if self.attrs:
							self.dic[url] = {attr: [node.get(attr) for node in nodes] for attr in self.attrs}  # 获取属性
						self.dic[url][""] = [node.text for node in nodes if node.text]  # 获取文本内容
				else:
					self.dic[url] = data  # 整个网页内容


class DynamicCrawler:
	def __init__(self, params):
		self.url = params["urls"]
		self.parser = params["parser"]
		self.attrs = params["attrs"]
		self.browser = None  # 模拟浏览器对象
		self.dic = {}  # 结果集字典

	def crawl(self):
		asyncio.run(self._main())
		return self.dic

	async def _main(self):
		async with async_playwright() as playwright:
			async with await playwright.chromium.launch() as browser:
				self.browser = browser  # 浏览器对象
				tasks = [asyncio.ensure_future(self._fetch())]  # 任务列表
				await asyncio.gather(*tasks)  # 异步执行任务列表

	async def _fetch(self):
		async with await self.browser.new_page() as page:
			await page.goto(self.url)  # 跳转至url
			nodes = await page.query_selector_all(self.parser)  # 获取节点
			self.dic[""] = [await node.text_content() for node in nodes if await node.text_content()]  # 获取文本内容
			if self.attrs:
				for attr in self.attrs:
					self.dic[attr] = [
						await node.get_attribute(attr) for node in nodes if await node.get_attribute(attr)
					]  # 获取属性
