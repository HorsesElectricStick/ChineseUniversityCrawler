import importlib
from Mould.BaseSpider import BaseSpider
from Utils.Exceptions import SpiderClassNotFound


class Core:
    def __init__(self, spider_modual: str, join: bool) -> None:
        modual = importlib.import_module(
            f".{spider_modual}", package="Spiders")
        try:
            self.spider_class:BaseSpider = modual.Spider
        except AttributeError:
            raise SpiderClassNotFound(spider_modual)
        self.join = join
        print(f"核心初始化正确\n爬虫模块:{modual}\n爬虫类:{self.spider_class}\njoin开关:{self.join}")
