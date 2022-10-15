import math
import sys


class MyBitMap:
	def __init__(self, size):
		self._size = size  # 存储比特的位数
		self._bitmap = 1 << size  # 默认首位为1且不参与存储，通过默认首位移位来开辟存储空间

	def set(self, bit):
		"""
		根据数据存储位置索引，将对应位置的比特值置为1
		:param bit: 数据存储位置索引
		"""
		if 0 <= bit < self._size:
			self._bitmap |= (1 << bit)  # 存值

	def get(self, bit):
		"""
		根据数据存储位置索引，获取对应位置存储的比特值
		:param bit: 数据存储位置索引
		:return 对应位置存储的比特值
		"""
		if 0 <= bit < self._size:
			return int((self._bitmap & (1 << bit)) != 0)  # 取值

	def get_size(self):
		"""
		获取位图的容量
		:return: 位图的容量
		"""
		return self._size

	def get_bitmap(self):
		"""
		获取位图
		:return: 位图
		"""
		return self._bitmap

	def get_sizeof(self):
		"""
		获取位图在系统中占用的大小
		:return: 位图在系统中占用的大小
		"""
		return sys.getsizeof(self._bitmap)


class MyBloomFilter:
	def __init__(self, n):
		self._false_positive = 0.01  # 误判率
		self._m = math.ceil(- n * math.log(self._false_positive) / (math.log(2) ** 2))  # 二进制比特长度
		self._k = math.ceil(- math.log(self._false_positive) / math.log(2))  # 哈希函数个数
		self._bitmap = MyBitMap(self._m)  # 位图对象

	def set(self, element):
		"""
		将字符串存入布隆过滤器
		:param element: 待存入字符串
		"""
		hash_code = self._time33(element)  # 通过time33算法计算初始哈希值
		for _ in range(self._k):  # 进行k次哈希计算
			hash_code >>= 1  # 上一次哈希的结果右移一位
			self._bitmap.set(hash_code % self._m)  # 存储当前哈希结果

	def get(self, element):
		"""
		检查字符串是否在布隆过滤器中
		:param element: 待检查字符串
		:return: 字符串是否在布隆过滤器中（若为True则可能存在，若为False则一定不存在）
		"""
		hash_code = self._time33(element)  # 通过time33算法计算初始哈希值
		for _ in range(self._k):  # 进行k次哈希计算
			hash_code >>= 1  # 上一次哈希的结果右移一位
			if not self._bitmap.get(hash_code % self._m):
				return False
		return True

	def get_size(self):
		"""
		获取布隆过滤器的容量
		:return: 布隆过滤器的容量
		"""
		return self._m

	def get_bitmap(self):
		"""
		获取布隆过滤器的位图对象
		:return: 布隆过滤器的位图对象
		"""
		return self._bitmap

	@staticmethod
	def _time33(element):
		"""
		time33算法，将字符串转为数字
		:param element: 待转换字符串
		:return: 转换后的哈希值
		"""
		hash_code = 5381  # 初始值5381(0001 0101 0000 0101)利于分散哈希值
		for c in element:
			hash_code += (hash_code << 5) + ord(c)  # 上一次的哈希值乘33加上本字符的ASCII值
		return hash_code
