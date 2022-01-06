自行编写的爬虫应当放在Spiders文件夹下，且继承于Mould.BaseSpider

在根目录使用命令启动爬虫

<code>
>>> python main.py MySpider -j  
#启动MySpider爬虫, -j代表以阻塞主线程的方式启动
</code>