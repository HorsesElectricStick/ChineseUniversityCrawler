from Utils import SettingsParser
import argparse
import importlib
from Utils.Exceptions import SpiderClassNotFound
from Mould import BaseSpider
import time
from Utils import WebDriver
from Engine import Core


def test():
    time.sleep(1)
    print("启动!")
    driver = WebDriver.get_driver()
    print("浏览器初始化完成!")
    driver.set_download_path()
    print("修改下载地址完成!")


def main():
    parser = argparse.ArgumentParser(description='启动爬虫程序.')
    parser.add_argument('modual', metavar='MySpider', type=str,
                        help='你的爬虫模块名，应当放在Spiders文件夹下')
    parser.add_argument(
        "-j", "--join", action='store_true', help="以阻塞主线程的方式启动")
    args = parser.parse_args()
    core = Core(args.modual, args.join)


if __name__ == "__main__":
    main()
