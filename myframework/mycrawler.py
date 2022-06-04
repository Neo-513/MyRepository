import aiofiles
import aiohttp
import asyncio
import math
import os
import re
import time

HEADERS = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.500"
	"5.63 Safari/537.36"
}  # 请求头


def crawl(urls, cookie="", rgx=None, folder="", encoding="utf-8"):
	"""url列表进行爬取网页数据或下载图片
	:param urls: url列表
	:param cookie: cookie
	:param rgx: 正则表达式
	:param folder: 保存图片目录
	:param encoding: 编码
	:return: 按url列表顺序的网页数据
	"""
	if cookie:
		HEADERS["cookie"] = cookie
	if folder and not os.path.exists(folder):
		os.mkdir(folder)  # 新建文件夹

	params = {
		"zfill": math.ceil(math.log(len(urls), 10)),  # 计数器补0位数
		"folder": folder,  # 文件夹
		"encoding": encoding,  # 编码
		"cmpl": re.compile(rgx, re.S) if rgx else None,  # 编译正则表达式
		"count": -1,  # 计数器
		"dic": {}  # url字典
	}
	asyncio.run(_main(urls, params))  # 异步执行爬取任务列表

	if not folder:
		return [params["dic"][url] for url in urls if url in params["dic"]]  # 按序返回数据


async def _main(urls, params):  # 任务列表
	timer = time.time()  # 计时器
	connector = aiohttp.TCPConnector(ssl=False)  # 取消ssl验证
	async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
		params["session"] = session  # session
		await asyncio.gather(*[asyncio.ensure_future(_fetch(url, params)) for url in urls])
	print(f"[CRAWLED IN]    {time.time() - timer}")  # 计时


async def _fetch(url, params):  # 爬取单个url
	session, zfill, encoding = params["session"], params["zfill"], params["encoding"]  # 常数参数
	folder, cmpl = params["folder"], params["cmpl"]  # 可选参数
	async with session.get(url) as response:
		params["count"] += 1  # 计数
		print(f"[{params['count']:0{zfill}}]  {folder}  {url}")  # 打印url信息
		response.raise_for_status()  # 判断页面连接状态
		if folder:  # 爬取图片
			async with aiofiles.open(f"{folder}/{url.split('/')[-1]}", mode="wb") as file:
				data = await response.read()  # 获取图片内容
				await file.write(data)  # 写入图片文件
		else:  # 爬取文本
			data = await response.text(encoding=encoding)  # 获取文本内容
			params["dic"][url] = cmpl.findall(data) if cmpl else data  # 加入url字典
