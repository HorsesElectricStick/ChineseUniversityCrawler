import logging
from typing import Any, Generator, List, Literal, Union
from Mould import BaseSpider, BaseTask
from Utils.SettingsParser import get_a_setting
from Utils.WebDriver import MyDriver, get_driver
from queue import Queue
from selenium.webdriver.remote.webelement import WebElement

TASK_TYPE = Literal['u', 'f']
SUFFIX = ['pdf', 'xls', 'xlsx', 'doc', 'zip', 'rar', '7z', 'docx']
TITLE_KEYWORD = ['2021', '拟录取']


class UrlTask(BaseTask):
    def __init__(self, school: str, url: str) -> None:
        self.school = school
        self.url = url
        super().__init__()


class FileTask(UrlTask):
    ...


class MyQueue(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        self.logger = logging.getLogger(get_a_setting(
            "root_logging")).getChild(self.__class__.__name__)
        super().__init__(maxsize=maxsize)

    def put(self, item: Union[UrlTask, FileTask]) -> None:
        self.logger.info(
            f"队列添加: {item.__class__.__name__}  {item.school}  {item.url}")
        return super().put(item)


class Spider(BaseSpider):
    def __init__(self) -> None:
        urlTask = {'广东工业大学': ['https://yzw.gdut.edu.cn/sszs.htm'],
                   '南京工业大学': ['http://gra.njtech.edu.cn/zsxx/sszs.htm'],
                   '江苏大学': ['https://yz.ujs.edu.cn/index/tzgg/14.htm']}
        self.task_queue = MyQueue()
        for school in urlTask:
            for url in urlTask[school]:
                self.task_queue.put(UrlTask(school, url))
        super().__init__(self.task_queue)
        self.logger.info(f"初始化任务，共{self.task_queue.qsize()}个")

    def join_start(self) -> None:
        self.start()
        self.task_queue.join()

    def parse(self, queue: MyQueue) -> None:
        driver = get_driver()
        while queue.qsize():
            task: Union[UrlTask, FileTask] = queue.get()
            new_tasks = Spider.url_task_handle(driver, task)
            for i in new_tasks:
                queue.put(i)
            queue.task_done()
            self.logger.info(
                f"任务已处理: {task.__class__.__name__}  {task.school}  {task.url}")

    @staticmethod
    def elements_check(driver: MyDriver, school: str, l: List[WebElement]) -> Generator[UrlTask, Any, Any]:
        for i in l:
            url: str = i.get_attribute(
                'href') if i.get_attribute('href') else ''
            title = i.text
            if any(url.endswith(sf) for sf in SUFFIX):
                Spider.file_handle(driver, school, i)
            elif any(sf in title for sf in SUFFIX):
                Spider.file_handle(driver, school, i)
            elif all(kw in title for kw in TITLE_KEYWORD):
                yield UrlTask(school, url)

    @staticmethod
    def file_handle(driver: MyDriver, school: str, element: WebElement) -> None:
        driver.set_download_path(school)
        element.click()

    @staticmethod
    def url_task_handle(driver: MyDriver, task: FileTask) -> Generator[UrlTask, Any, Any]:
        driver.get(task.url)
        a = driver.find_elements_by_xpath('//a')
        tasks = Spider.elements_check(driver, task.school, a)
        for task in tasks:
            yield task
