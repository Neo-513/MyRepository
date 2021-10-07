# import win32api
# import win32con
from selenium import webdriver
import aiofiles
import aiohttp
import asyncio
import csv
import datetime
import demjson
import math
import os
import psutil
import re
import requests
import time

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 S" \
	"afari/537.36"  # 浏览器代理
headers = {"user-agent": user_agent}  # 请求头
super_path = "D:/MyCodes"  # 主目录
driver_path = f"{super_path}/chromedriver.exe"  # 驱动目录


def read(path):  # 读文件
	if "." not in path:
		path = f"{super_path}/myfiles/{path}.csv"
	file_type = path.split(".")[-1]
	encoding = "gbk" if file_type == "csv" else "utf-8"

	with open(path, mode="r", encoding=encoding) as file:
		if file_type == "csv":
			datas = [[r for r in reader] for reader in csv.reader(file)]
			if len(datas[0]) == 1:  # 一维列表
				datas = [data[0] for data in datas]
		elif file_type == "json":
			datas = demjson.decode(file.read())
		elif file_type == "txt":
			datas = file.read()
		else:
			return print(f"TYPE ERROR: {file_type}")
		print(f"READ: {path}")
		return datas


def write(path, datas):  # 写文件
	if "." not in path:
		path = f"{super_path}/myfiles/{path}.csv"
	file_type = path.split(".")[-1]
	encoding = "gbk" if file_type == "csv" else "utf-8"

	with open(path, mode="w", encoding=encoding, newline="") as file:
		if file_type == "csv":
			if not isinstance(datas[0], list):  # 一维列表
				datas = [[data] for data in datas]
			csv.writer(file).writerows(datas)
		elif file_type == "json":
			file.write(demjson.encode(datas))
		elif file_type == "txt":
			file.write(datas)
		else:
			return print(f"TYPE ERROR: {file_type}")
		print(f"WRITE: {path}")


def timing(func):  # 统计时间
	def wrapper(*args, **kwargs):  # 包裹函数
		before = time.time()
		datas = func(*args, **kwargs)  # 执行函数
		now = time.time()
		print(f"TIMING: {now - before}")
		return datas
	return wrapper


class MyCrawler:  # 异步爬虫类
	def __init__(self, cookie="", gbk=False):
		headers["cookie"] = cookie  # 设置cookie
		self.encoding = "gbk" if gbk else "utf-8"  # 字符集

	@timing
	def crawl(self, urls, rgx=None, folder="", dic=False):  # 异步爬取队列，请求<=12000，图片<=1000
		async def main():  # 任务列表
			connector = aiohttp.TCPConnector(ssl=False)  # 取消ssl验证
			async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
				await asyncio.gather(*[asyncio.ensure_future(self.fetch(url, session, params)) for url in urls])

		params = (
			{"counter": -1},  # 计数器
			math.ceil(math.log(len(urls), 10)),  # 计数器补0位数
			folder,  # 文件夹
			self.encoding,  # 字符集
			{},  # url字典
			rgx  # 正则表达式
		)
		if folder and not os.path.exists(folder):
			os.mkdir(folder)  # 新建文件夹
		asyncio.run(main())  # 异步执行爬取任务列表
		if not folder:
			return params[4] if dic else [params[4][url] for url in urls if url in params[4]]

	@staticmethod
	async def fetch(url, session, params):  # 异步爬取单个
		async with session.get(url) as response:
			try:
				params[0]["counter"] += 1
				response.raise_for_status()  # 判断页面连接状态
				print(f"[{params[0]['counter']:0{params[1]}}]  {params[2]}  {url}")  # 打印信息
				if params[2]:  # 爬取图片
					async with aiofiles.open(f"{params[2]}/{url.split('/')[-1]}", mode="wb") as f:
						datas = await response.read()
						await f.write(datas)
				else:  # 爬取文本
					data = await response.text(encoding=params[3])
					params[4][url] = re.findall(params[5], data, flags=re.S) if params[5] else data
			except Exception as e:
				print(f"[{params[0]['counter']:0{params[1]}}]  {params[2]}  {url}    {e}")  # 打印异常信息

	def get_html(self, url, rgx=None):  # 同步爬取单个
		with requests.get(url, headers=headers) as response:
			try:
				response.raise_for_status()
				response.encoding = self.encoding
				print(f"{url}")
				datas = response.text
				return re.findall(rgx, datas, flags=re.S) if rgx else datas
			except Exception as e:
				print(f"{url}    {e}")


class MySelenium:  # 模拟浏览器类
	options = webdriver.ChromeOptions()  # 浏览器设置
	options.add_argument(f"user-agent={user_agent}")  # 添加请求头

	def get_cookie(self, url, timeout=15):
		"""通过登录行为获取cookie"""
		with webdriver.Chrome(executable_path=driver_path, chrome_options=self.options) as driver:
			driver.get(url)
			driver.delete_all_cookies()
			for i in range(timeout * 2 + 1):  # 显示进度条
				print(f"\rLOADING:{(i / (timeout * 2)) * 100:>6.2f}% {'■' * i}{'□' * (timeout * 2 - i)}", end="")
				time.sleep(0.5)
			cookies = driver.get_cookies()
			print("\n" + "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]))

	def get_elems_by_xpath(self, url, xpath, cookies=None):
		"""通过xpath获取元素"""
		self.options.add_argument("--headless")  # 设置无头浏览器
		self.options.add_argument("--disable-gpu")  # 设置无头浏览器
		with webdriver.Chrome(executable_path=driver_path, options=self.options) as driver:
			driver.get(url)
			time.sleep(3)  # 等网页刷新
			if not cookies:
				driver.delete_all_cookies()
				for cookie in cookies:
					driver.add_cookie(cookie)
			driver.refresh()

			for i in range(100):  # 下拉次数默认100
				driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 脚本下拉页面
				time.sleep(0.05)
				print(i % 10, end="" if i < 99 else "\n")
			elems = driver.find_element_by_xpath(xpath).text
		return elems


def netspeed():  # 测量当前网速
	while True:
		sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
		recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
		time.sleep(1)
		sent_now = psutil.net_io_counters().bytes_sent  # 1秒后已发送的流量
		recv_now = psutil.net_io_counters().bytes_recv  # 1秒后已接收的流量
		sent = (sent_now - sent_before) / 1024  # 发送的流量
		recv = (recv_now - recv_before) / 1024  # 接收的流量
		print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}      上传:{sent:>7.2f} KB/s      下载:{recv:>7.2f} KB/s")


def jsonstr_to_dict(jsonstr):  # json字符串转为字典
	dic = {"null": "None", "true": "True", "false": "False"}
	for d in dic:
		jsonstr = jsonstr.replace(d, dic[d])
	return eval(jsonstr)


'''
def cmd(command):  # 执行cmd
	# os.system("chcp 65001")  # 页面编码转为gbk
	print(command)
	print(os.popen(command).read())


def pip(lib):  # 通过清华镜像pip安装模块
	command = "pip install %s -i https://pypi.tuna.tsinghua.edu.cn/simple/" % lib
	cmd(command)

def remove_repeat(folder_src, folder_dst):  # 文件去重
	files_src = []  # 不变
	for folder in os.listdir(folder_src):
		files_src += os.listdir("%s/%s" % (folder_src, folder))
	files_dst = os.listdir(folder_dst)  # 变

	for file_dst in files_dst:
		if file_dst in files_src:
			src = "%s/%s" % (folder_dst, file_dst)
			dst = "E:/recycle/" + file_dst
			os.rename(src, dst)
			print("REPEAT: " + file_dst)
		else:
			print("NOT REPEAT: " + file_dst)

def click(x, y, interval=0.3):
	win32api.SetCursorPos([x, y])
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)
	time.sleep(interval)


def keyboard(key):
	win32api.keybd_event(key, 0, 0, 0)
	win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def normalize_symbol(data):
	for i in range(len(data)):
		d = data[i]
		if 65296 <= ord(d) <= 65305 or 65313 <= ord(d) <= 65339 or 65345 <= ord(d) <= 65371:
			data = data.replace(d, chr(ord(d) - 65248))
	return data
'''

if __name__ == "__main__":
	netspeed()
