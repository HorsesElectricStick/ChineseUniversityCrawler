from typing import Any
import settings
from Utils.Exceptions import EmptySettingsValueError


def get_settings() -> dict:
    '''返回settings中所有设置与对应值的字典'''
    attrs = [i for i in dir(settings) if i[:2] != '__' and i[-2:] != '__']
    attrs_dic = {}
    for i in attrs:
        v = getattr(settings, i)
        if not v:
            raise EmptySettingsValueError(i)
        attrs_dic[i] = v
    return attrs_dic


def get_a_setting(name: str) -> Any:
    """
    输入要获取的设置项，返回对应的值

    Args:
        name (str): 要获取的设置项
    """
    v = getattr(settings, name)
    if not v:
        raise EmptySettingsValueError(name)
    return v
