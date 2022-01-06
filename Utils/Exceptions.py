'''自定义异常'''
import logging


class NoSuchSettingError(Exception):
    '''获取setting时，如果不存在设置项，抛出此异常'''

    def __init__(self, setting) -> None:
        self.err_setting = setting
        super().__init__()

    def __str__(self) -> str:
        return f"无法获取到名为'{self.err_setting}'的设置项"


class SpiderClassNotFound(Exception):
    '''没有找到爬虫类，抛出此异常'''

    def __init__(self, module: str) -> None:
        self.module = module
        super().__init__()

    def __str__(self) -> str:
        return f"{self.module}下没有找到Spider类"
