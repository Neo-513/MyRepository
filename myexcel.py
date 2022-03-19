import openpyxl


def read(path):
	"""读取excel
	:param path: 文件路径
	:return: 键名为页名、键值为二维数组的数据集合字典
	"""
	file = openpyxl.load_workbook(path)  # 文件对象
	dic = {}  # 数据集合字典

	for sheetname in file.sheetnames:  # 遍历表名
		datas = file[sheetname]  # 单张表数据集合
		dic[sheetname] = [[cell.value if cell.value else "" for cell in row] for row in datas.rows]

	file.close()  # 关闭文件对象
	print(f"[READ]    {path}")  # 打印信息
	return dic


def write(path, dic):
	"""读取excel
	:param path: 文件路径
	:param dic: 键名为页名、键值为二维数组的数据集合字典
	"""
	file = openpyxl.Workbook()  # 文件对象
	file.remove(file.active)  # 删除默认表

	for sheetname in dic:  # 遍历表名
		sheet = file.create_sheet(sheetname)  # 创建表
		datas = dic[sheetname]  # 单张表数据集合
		row = len(datas)  # 行数
		col = len(datas[0])  # 列数
		for r in range(row):  # 遍历行
			for c in range(col):  # 遍历单元格
				sheet.cell(r + 1, c + 1).value = datas[r][c]  # 写入单元格数据（起始索引为1）

	file.save(path)  # 保存文件
	file.close()  # 关闭文件对象
	print(f"[WITRE]    {path}")  # 打印信息
