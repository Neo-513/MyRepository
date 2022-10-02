import aiofiles
import aiohttp
import asyncio
import browser_cookie3
import math
import os
import re
import time

HEADERS = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0"
	" Safari/537.36 Edg/105.0.1343.53"
}  # 请求头


def get_cookie(url):
	"""
	通过url获取当前cookie字符串
	:param url: url
	:return: cookie字符串
	"""
	return "; ".join([f"{c.name}={c.value}" for c in browser_cookie3.edge() if c.domain in url])


def crawl(urls, cookie=None, rgx=None, folder="", encoding="utf-8", proxy=""):
	"""
	url列表进行爬取网页数据或下载图片
	:param urls: url列表
	:param cookie: 当前cookie对应的url
	:param rgx: 正则表达式
	:param folder: 保存图片目录
	:param encoding: 编码
	:param proxy: 本机代理
	:return: 按url列表顺序的网页数据
	""" 
	if cookie:
		HEADERS["cookie"] = cookie
	if folder and not os.path.exists(folder):
		os.mkdir(folder)  # 新建文件夹

	params = {
		"proxy": proxy,  # 本机代理
		"zfill": math.ceil(math.log(len(urls), 10)),  # 计数器补0位数
		"folder": folder,  # 文件夹
		"encoding": encoding,  # 编码
		"cmpl": re.compile(rgx, re.S) if rgx else None,  # 编译正则表达式
		"count": -1,  # 计数器
		"dic": {}  # url字典
	}
	if proxy:
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # 设置允许代理策略
	asyncio.run(_main(urls, params))  # 异步执行爬取任务列表

	if not folder:
		return [params["dic"][url] for url in urls if url in params["dic"]]  # 按序返回数据


async def _main(urls, params):  # 任务列表
	tic = time.time()
	connector = aiohttp.TCPConnector(ssl=False)  # 取消ssl验证
	async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
		params["session"] = session  # session
		await asyncio.gather(*[asyncio.ensure_future(_fetch(url, params)) for url in urls])
	toc = time.time()
	print(f"[CRAWLED IN]    {toc - tic}")


async def _fetch(url, params):  # 爬取单个url
	async with params["session"].get(url, proxy=params["proxy"]) as response:
		params["count"] += 1  # 计数
		print(f"[{params['count']:0{params['zfill']}}]  {params['folder']}  {url}")  # 打印url信息
		response.raise_for_status()  # 判断页面连接状态
		if params["folder"]:  # 爬取图片
			async with aiofiles.open(f"{params['folder']}/{url.split('/')[-1]}", mode="wb") as file:
				data = await response.read()  # 获取图片内容
				await file.write(data)  # 写入图片文件
		else:  # 爬取文本
			data = await response.text(encoding=params["encoding"])  # 获取文本内容
			params["dic"][url] = params["cmpl"].findall(data) if params["cmpl"] else data  # 加入url字典
