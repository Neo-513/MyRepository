import mycrawler
import myutility as mu


class MyBiliBili:
	def __init__(self, cookie):
		self.mc = mycrawler.MyCrawler(cookie=cookie)  # 爬虫

	def get_favs(self, fid):  # 获取收藏夹信息（上限1500）
		urls = [f"http://api.bilibili.com/x/v3/fav/resource/list?ps=20&media_id={fid}&pn={i + 1}" for i in range(75)]
		datas = self.mc.crawl(urls)
		items = map(lambda x: x["data"]["medias"], map(mu.str2dic, datas))
		return [[i["bv_id"], i["title"], i["upper"]["mid"], i["upper"]["name"]] for item in items if item for i in item]

	def get_ups(self, tid=None):  # 获取关注信息（上限2000）
		urls = [f"http://api.bilibili.com/x/relation/followings?vmid=37928647&order=desc&pn={i + 1}" for i in range(40)]
		datas = self.mc.crawl(urls)
		items = map(lambda x: x["data"]["list"], map(mu.str2dic, datas))
		return {i["mid"]: i["uname"] for item in items for i in item if not tid or (i["tag"] and i["tag"][0] == tid)}
