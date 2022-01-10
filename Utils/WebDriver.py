from typing import Any
from selenium.webdriver import Chrome
from selenium import webdriver
from lxml import etree
import os
from Utils import SettingsParser, Path


class MyDriver(Chrome):
    def get_html(self) -> Any:
        """返回解析后的HTML结构"""
        html = self.execute_script("return document.documentElement.outerHTML")
        html = etree.HTML(html)
        return html

    def set_download_path(self, path: str) -> str:
        """
        动态修改下载路径

        Args:
            path (str): 下载路径，此路径为settings.py中DOWNLOAD_FILE_PATH项的相对路径
        Returns:
            str: 下载路径的绝对路径
        """
        path = path.rstrip(os.sep)
        path = os.path.join(os.path.abspath(
            SettingsParser.get_a_setting("DOWNLOAD_FILE_PATH")), path)
        Path.check_path(path, create=True)
        self.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow', 'downloadPath': path}}
        self.execute("send_command", params)
        return path


def _get_driver(timeout: int = 5, download_path: str = None) -> MyDriver:
    """
    生成一个继承自selenium.webdriver.Chrome的MyDriver实例，并返回

    Args:
        timeout (int, optional): 超时设置，单位为秒. 默认为5.
        download_path (str, optional): 下载文件的存储路径. 默认为None.

    Returns:
        MyDriver: MyDriver实例
    """
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('log-level=4')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option(
        "prefs", {"download.default_directory": download_path,
                  "profile.default_content_settings.popups": 0,
                  "download.prompt_for_download": False,
                  "download.directory_upgrade": True,
                  "plugins.always_open_pdf_externally": True})
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = MyDriver(options=options)
    driver.set_page_load_timeout(timeout)
    driver.set_script_timeout(timeout)
    return driver


def get_driver() -> MyDriver:
    timeout = SettingsParser.get_a_setting("TIME_OUT")
    download_path = os.path.abspath(
        SettingsParser.get_a_setting("DOWNLOAD_FILE_PATH"))
    Path.check_path(download_path, create=True)
    return _get_driver(timeout=timeout, download_path=download_path)
