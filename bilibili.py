import math
import mycrawler
import myutils as mu


class BiliBili:
	def __init__(self, uid, cookie):
		self.mc = mycrawler.MyCrawler(cookie=cookie)  # 爬虫
		self.url_fav = "http://api.bilibili.com/x/v3/fav/resource/list?ps=20"  # 收藏夹url
		self.url_up = f"http://api.bilibili.com/x/relation/followings?vmid={uid}&order=desc"  # 关注up url

	def get_favs(self, fid):
		"""爬取收藏夹内容
		:param fid: 收藏夹id
		:return: 元素为视频标题、up id、up网名的列表
		"""
		urls = [f"{self.url_fav}&media_id={fid}&pn={i + 1}" for i in range(self._count_fav(fid))]
		datas = self.mc.crawl(urls)
		return [[d["title"], d["upper"]["mid"], d["upper"]["name"]] for data in datas for d in mu.jsn2dic(data)[
			"data"]["medias"]]

	def get_ups(self):
		"""爬取关注up信息
		:return: 键名为up id、键值为up网名的字典
		"""
		urls = [f"{self.url_up}&pn={i + 1}" for i in range(
			self._count_up())]
		datas = self.mc.crawl(urls)
		return {d["mid"]: d["uname"] for data in datas for d in mu.jsn2dic(data)["data"]["list"]}

	def _count_fav(self, fid):  # 计算收藏夹内容个数（外部不可调用）
		url = f"{self.url_fav}&media_id={fid}&pn=1"
		data = self.mc.crawl(url)
		count = mu.jsn2dic(data)["data"]["info"]["media_count"]
		return math.ceil(count / 20)  # 每页20

	def _count_up(self):  # 计算关注up个数（外部不可调用）
		url = f"{self.url_up}&pn=1"
		data = self.mc.crawl(url)
		count = mu.jsn2dic(data)["data"]["total"]
		return math.ceil(count / 50)  # 每页50
