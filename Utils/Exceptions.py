# 此文件下包含了一些自定义的异常

class EmptySettingsValueError(Exception):
    '''当获取settings时，如果值为空或者未设置，抛出此异常'''

    def __init__(self, setting) -> None:
        self.err_setting = setting
        super().__init__(setting)

    def __str__(self) -> str:
        return "settings.py中 {0} 项为空或未设置".format(self.err_setting)
