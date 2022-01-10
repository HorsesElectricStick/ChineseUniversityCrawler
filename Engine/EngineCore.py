from datetime import datetime
import importlib
import logging
from Mould.BaseSpider import BaseSpider
from Utils.Exceptions import SpiderClassNotFound
import logging
from Utils.Path import check_path
from Utils.SettingsParser import get_a_setting
import time
from os.path import abspath


class Core:
    def __init__(self, spider_modual: str, join: bool, save_log: bool) -> None:
        modual = importlib.import_module(
            f".{spider_modual}", package="Spiders")

        try:
            self.spider_class: BaseSpider = modual.Spider
        except AttributeError:
            raise SpiderClassNotFound(spider_modual)

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(get_a_setting("ROOT_LOGGER"))

        sp: BaseSpider = self.spider_class()

        self.logger.info(
            f"核心初始化正确, 爬虫模块:{modual}, 爬虫类:{self.spider_class}, join开关:{join}")

        if save_log:
            path = get_a_setting("log_file_path")
            check_path(path, create=True)
            self.logger.addHandler(logging.FileHandler(abspath(
                path)+'\\' + datetime.now().strftime("%Y.%m.%d %H-%M-%S")+".log", encoding='utf-8'))

        self.start_time = time.time()

        self.logger.info("任务开始")

        if join:
            sp.join_start()
        else:
            sp.start()

    def __del__(self):
        self.logger.info(f"所有任务完成，共耗时{round(time.time()-self.start_time, 3)}秒")
