import collections
import csv
import demjson
import jieba
import json
import time

super_path = "D:/MyCodes"  # 主目录


def read(path, show_len=False, split=True):  # 读文件
	if "." not in path:
		path = f"{super_path}/myfiles/{path}.csv"

	filetype = path.split(".")[-1]
	if filetype == "csv":
		with open(path, mode="r", encoding="gbk") as f:
			datas = [[r for r in reader] for reader in csv.reader(f)]
			if len(datas[0]) == 1:  # 一维列表
				datas = [data[0] for data in datas]
	elif filetype == "json":
		with open(path, mode="r", encoding="utf-8") as f:
			datas = demjson.decode(f.read())
	elif filetype == "txt":
		with open(path, mode="r", encoding="utf-8") as f:
			datas = f.read()
			if show_len:
				print(f"[{len(datas)}]", end="    ")
			if split:
				datas = datas.split("\n")
	print(f"READ: {path}")
	return datas


def write(path, datas):  # 写文件
	if "." not in path:
		path = f"{super_path}/myfiles/{path}.csv"

	filetype = path.split(".")[-1]
	if filetype == "csv":
		with open(path, mode="w", encoding="gbk", newline="") as f:
			if not isinstance(datas[0], list):  # 一维列表
				datas = [[data] for data in datas]
			csv.writer(f).writerows(datas)
	elif filetype == "json":
		with open(path, mode="w", encoding="utf-8") as f:
			f.write(demjson.encode(datas))
	elif filetype == "txt":
		with open(path, mode="w", encoding="utf-8") as f:
			f.write(datas)
	print(f"WRITE: {path}")


def mysort(items, idx=0, reverse=True):  # 排序列表和字典
	if isinstance(items, list):
		items.sort(key=lambda x: x[idx], reverse=reverse)
		return items
	elif isinstance(items, dict):
		return dict(sorted(items.items(), key=lambda x: x[idx], reverse=reverse))


def lst2dic(lst):  # 统计列表元素个数
	dic = dict(collections.Counter(lst))  # 列表转为计数字典
	return mysort(dic, 1)  # 对字典按值排序


def jsn2dic(jsn):  # json字符串转为字典
	dic = {"null": "None", "true": "True", "false": "False"}
	for d in dic:
		jsn = jsn.replace(d, dic[d])
	return eval(jsn)


def beautify_jsn(jsn):  # 格式化打印json字符串
	if isinstance(jsn, str):
		jsn = jsn2dic(jsn)
	print(json.dumps(jsn, indent=4, ensure_ascii=False))


def myprint(items):  # 打印
	if isinstance(items, dict):
		for k, v in items.items():
			print(f"{k}    {v}")
	else:
		for item in items:
			print(item)


def timing(func):  # 统计时间
	def callback(*args, **kwargs):  # 回调函数
		timer = time.time()  # 计时器
		datas = func(*args, **kwargs)  # 执行函数
		print(f"TIMING: {time.time() - timer}")
		return datas
	return callback


def analyze_nlp(kws):  # 中文分词
	keywords = sum(map(lambda x: jieba.lcut(x), kws), [])
	return lst2dic(keywords)


'''
for i in range(timeout * 2 + 1):  # 显示进度条
	print(f"\rLOADING:{(i / (timeout * 2)) * 100:>6.2f}% {'■' * i}{'□' * (timeout * 2 - i)}", end="")
	time.sleep(0.5)


# import win32api
# import win32con


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
