from email.mime.text import MIMEText
import smtplib
from typing import List
from Utils.SettingsParser import get_a_setting


class EmailSender:
    def __init__(self) -> None:
        self.sender = get_a_setting("SENDER")
        self.smtp_host = get_a_setting("SMTP_HOST")
        self.smtp_user = get_a_setting("SMTP_USER")
        self.smtp_password = get_a_setting("SMTP_PASSWORD")
        self.smtpObj = smtplib.SMTP(self.smtp_host)
        self.smtpObj.login(self.smtp_user, self.smtp_password)

    def sendEmail(self, receivers: List[str], title: str, content: str) -> None:
        """
        发送邮件

        Args:
            receivers (List[str]): 接收者的邮箱地址列表，会向此列表中的所有邮箱发送邮件
            title (str): 邮件的标题
            content (str): 邮件的正文
        """
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = self.sender
        message['To'] = ','.join(receivers)
        message['Subject'] = title

        self.smtpObj.sendmail(self.sender, receivers, message.as_string())
