'''获取设置项的工具函数'''

from typing import Any
import settings
from Utils.Exceptions import NoSuchSettingError


def get_settings() -> dict:
    '''返回settings中所有设置与对应值的字典'''
    attrs = [i for i in dir(settings) if i[:2] != '__' and i[-2:] != '__']
    attrs_dic = {}
    for i in attrs:
        v = get_a_setting(i)
        attrs_dic[i] = v
    return attrs_dic


def get_a_setting(name: str) -> Any:
    """
    输入要获取的设置项，返回对应的值

    Args:
        name (str): 要获取的设置项
    """
    name = name.upper()
    try:
        v = getattr(settings, name)
    except:
        raise NoSuchSettingError(name)
    else:
        return v
