import importlib
import logging
from Mould.BaseSpider import BaseSpider
from Utils.Exceptions import SpiderClassNotFound
import logging
from Utils.SettingsParser import get_a_setting
import time


class Core:
    def __init__(self, spider_modual: str, join: bool) -> None:
        modual = importlib.import_module(
            f".{spider_modual}", package="Spiders")
        try:
            self.spider_class:BaseSpider = modual.Spider
        except AttributeError:
            raise SpiderClassNotFound(spider_modual)
        self.join = join
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logger = logging.getLogger(get_a_setting("ROOT_LOGGING"))
        sp:BaseSpider = self.spider_class()
        logger.info(f"核心初始化正确, 爬虫模块:{modual}, 爬虫类:{self.spider_class}, join开关:{self.join}")
        start_time = time.time()
        logger.info("任务开始")
        if join:
            sp.join_start()
        else:
            sp.start()

        logger.info(f"所有任务完成，共耗时{round(time.time()-start_time, 3)}")