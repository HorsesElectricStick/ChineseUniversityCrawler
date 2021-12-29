import os


def check_path(path: str, create: bool = False) -> bool:
    """
    检查指定的路径是否存在，如果存在则返回True，不存在则返回False.
    根据传入的create参数，决定在路径不存在时，是否要根据路径创建文件夹.

    Args:
        path (str): 需要检查的路径
        create (bool, optional): 路径不存在时，是否根据路径创建文件夹. 默认为 False.

    Returns:
        bool: 检查的路径是否存在.
    """

    if (os.path.exists(path)):
        return True

    if create:
        os.makedirs(path, exist_ok=True)

    return False

