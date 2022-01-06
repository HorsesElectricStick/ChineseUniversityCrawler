from multiprocessing.dummy import Process
from typing import Callable, List
from Utils.SettingsParser import get_a_setting
import logging


class BaseSpider:
    '''多线程的爬虫基类'''

    def __init__(self, *args, **kwargs) -> None:
        """
        初始化

        Args:
            target (Callable): 需要执行的函数.
        """
        thread_num = int(get_a_setting("THREAD_NUM"))
        self._threads: List[Process] = []

        self.logger = logging.getLogger(get_a_setting(
            "root_logging")).getChild(self.__class__.__name__)

        for i in range(thread_num):
            thread = Process(target=self.parse, args=args,
                             kwargs=kwargs, name=f"Thread-{i}")
            self._threads.append(thread)

    def parse(self, *args, **kwargs) -> None:
        """爬虫默认的处理函数，处理数据的逻辑代码应该写在这里"""
        ...

    def set_daemon(self, d: bool) -> None:
        """
        设置守护线程

        Args:
            d (bool): True开启，False关闭
        """
        for thread in self._threads:
            thread.setDaemon(d)

    def start(self, join: bool = False) -> None:
        """
        启动所有线程.

        Args:
            join (bool, optional): 是否阻塞主线程，默认为False.
        """
        for thread in self._threads:
            thread.start()
        if join:
            for thread in self._threads:
                thread.join()

    def join_start(self) -> None:
        """以阻塞主线程的方式启动所有线程"""
        self.start(join=True)
