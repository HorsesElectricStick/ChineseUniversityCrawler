from multiprocessing.dummy import Process
from typing import Callable, List
from Utils.SettingsParser import get_a_setting


class Spider:
    '''多线程的爬虫基类'''

    def __init__(self, target: Callable, *args, **kwargs) -> None:
        """
        初始化

        Args:
            target (Callable): 需要执行的函数.
        """
        thread_num = int(get_a_setting("THREAD_NUM"))
        self._threads: List[Process] = []

        for i in range(thread_num):
            thread = Process(target=target, args=args, kwargs=kwargs, name=f"Thread-{i}")
            self._threads.append(thread)

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
