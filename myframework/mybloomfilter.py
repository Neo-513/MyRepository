class MyBitMap:
	def __init__(self, size):
		self._size = size  # 存储比特的位数
		self._bitmap = 1 << size  # 默认首位为1且不参与存储，通过默认首位移位来开辟存储空间

	def set(self, idx):
		"""
		根据数据存储位置索引，将对应位置的比特值置为1
		:param idx: 数据存储位置索引
		"""
		if 0 <= idx < self._size:
			self._bitmap |= (1 << idx)  # 存值

	def get(self, idx):
		"""
		根据数据存储位置索引，获取对应位置存储的比特值
		:param idx: 数据存储位置索引
		:return 对应位置存储的比特值
		"""
		if 0 <= idx < self._size:
			return int((self._bitmap & (1 << idx)) != 0)  # 取值

	def get_bitmap(self):
		"""
		获取位图当前状态的二进制编码
		:return: 位图当前状态的二进制编码
		"""
		return bin(self._bitmap)[3:]  # 获取位图当前状态的二进制编码
