import math
import mycrawler
import myutils as mu


class BiliBili:
	def __init__(self, cookie):
		self.mc = mycrawler.MyCrawler(cookie=cookie)  # 爬虫

	def get_favs(self, fid):
		"""爬取收藏夹内容
		:param fid: 收藏夹id
		:return: 元素为视频bv、视频标题、up id、up网名的列表
		"""
		urls = [f"http://api.bilibili.com/x/v3/fav/resource/list?ps=20&pn={i + 1}&media_id={fid}" for i in range(
			self._count_favs(fid))]
		datas = self.mc.crawl(urls)
		return [[d["bv_id"], d["title"], d["upper"]["mid"], d["upper"]["name"]] for data in datas for d in mu.jsn2dic(
			data)["data"]["medias"]]

	def get_ups(self, tag=None):
		"""爬取关注up信息
		:param tag: 类别
		:return: 键名为up id、键值为up网名的字典
		"""
		urls = [f"http://api.bilibili.com/x/relation/followings?vmid=37928647&order=desc&pn={i + 1}" for i in range(
			self._count_ups())]
		datas = self.mc.crawl(urls)
		return {d["mid"]: d["uname"] for data in datas for d in mu.jsn2dic(data)["data"]["list"] if (
			d["tag"] == [tag] if tag else 1)}

	def _count_favs(self, fid):  # 计算收藏夹内容个数（外部不可调用）
		url = f"http://api.bilibili.com/x/v3/fav/resource/list?ps=20&pn=1&media_id={fid}"
		data = self.mc.crawl(url)
		count = mu.jsn2dic(data)["data"]["info"]["media_count"]
		return math.ceil(count / 20)  # 每页20

	def _count_ups(self):  # 计算关注up个数（外部不可调用）
		url = f"http://api.bilibili.com/x/relation/followings?vmid=37928647&order=desc&pn=1"
		data = self.mc.crawl(url)
		count = mu.jsn2dic(data)["data"]["total"]
		return math.ceil(count / 50)  # 每页50
