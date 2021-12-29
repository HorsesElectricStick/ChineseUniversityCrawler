from typing import Callable
from Mould import BaseSpider

class Spider(BaseSpider):
    def __init__(self, target: Callable, *args, **kwargs) -> None:
        super().__init__(target, *args, **kwargs)
        print("我是自定义爬虫，我初始化啦")

