import demjson
import json


def read(path):  # 读json文件
	with open(path, mode="r", encoding="utf-8") as file:
		datas = demjson.decode(file.read())
	print(f"READ: {path}")
	return datas


def write(path, datas):  # 写json文件
	with open(path, mode="w", encoding="utf-8") as file:
		file.write(demjson.encode(datas))
	print(f"WRITE: {path}")


def jsn2dic(jsn):  # json字符串转为字典
	dic = {"null": "None", "true": "True", "false": "False"}
	for d in dic:
		jsn = jsn.replace(d, dic[d])
	return eval(jsn)


def beautify(jsn):  # 格式化json字符串
	dic = jsn2dic(jsn)
	print(json.dumps(dic, indent=4, ensure_ascii=False))
