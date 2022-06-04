import math
from myframework import mycrawler as mc, myutils as mu


class BiliBili:
	def __init__(self, mid, cookie):
		self.mid = mid  # 用户uid
		self.cookie = cookie  # cookie

	def get_favs(self, fid):
		"""爬取收藏夹内容
		:param fid: 收藏夹id
		:return: 元素为视频标题、up id、up网名的列表
		"""
		url_fav = f"https://api.bilibili.com/x/v3/fav/resource/list?ps=20&media_id={fid}"

		urls = [f"{url_fav}&pn=1"]
		datas = mc.crawl(urls, cookie=self.cookie)
		page = math.ceil(mu.jsn2dic(datas[0])["data"]["info"]["media_count"] / 20)  # 每页20

		urls = [f"{url_fav}&pn={i + 1}" for i in range(page)]
		datas = mc.crawl(urls, cookie=self.cookie)
		return [[d["title"], d["upper"]["mid"], d["upper"]["name"], d["bvid"]] for data in datas for d in mu.jsn2dic(
			data)["data"]["medias"]]

	def get_ups(self):
		"""爬取关注up信息
		:return: 键名为up id、键值为up网名的字典
		"""
		url_up = f"https://api.bilibili.com/x/relation/followings?vmid={self.mid}&order=desc"

		urls = [f"{url_up}&pn=1"]
		datas = mc.crawl(urls, cookie=self.cookie)
		page = math.ceil(mu.jsn2dic(datas[0])["data"]["total"] / 50)  # 每页50

		urls = [f"{url_up}&pn={i + 1}" for i in range(page)]
		datas = mc.crawl(urls, cookie=self.cookie)
		return {d["mid"]: d["uname"] for data in datas for d in mu.jsn2dic(data)["data"]["list"]}

	def get_folders(self):
		"""爬取收藏夹信息
		:return: 元素为收藏夹id、收藏夹标题、收藏视频个数的字典
		"""
		urls = [f"https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={self.mid}"]
		datas = mc.crawl(urls, cookie=self.cookie)
		return [[d["id"], d["title"], d["media_count"]] for d in mu.jsn2dic(datas[0])["data"]["list"]]
