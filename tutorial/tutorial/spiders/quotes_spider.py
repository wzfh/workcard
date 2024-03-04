# from pathlib import Path
#
# import scrapy
#
#
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#
#     def start_requests(self):
#         urls = [
#             "https://quotes.toscrape.com/page/1/",
#             "https://quotes.toscrape.com/page/2/",
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = f"quotes-{page}.html"
#         Path(filename).write_bytes(response.body)
#         self.log(f"Saved file {filename}")
import pyDes

k = pyDes.triple_des(bytes.fromhex('e96d6e19f138ad260215794f403ee9a8'), pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
print(k.decrypt("\x1d"))
data = bytes().fromhex('1d84b30afe994991ba37ca85926ebd6a')
print(data)
e = k.decrypt(data)
print(e)