import logging
import json
import time
import requests
from scrapy import signals
from spider_common.notify import SignalEnum

logger = logging.getLogger(__name__)


class SignalHandler(object):
    def __init__(self, api=None):
        """

        :param api: callable api url, like http://ip:port/path
        API Protocol
        v1 2019-04-03
        POST application/json
        {"title":"","content":""}
        """
        self.api = api

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        ext = cls(settings.get('NOTIFICATION_API'))

        def add_signal_callback(signal_enum, priority=0):
            crawler.signals.connect(getattr(ext, signal_enum.name), signal=getattr(signals, signal_enum.name.lower()))

        signals_config = settings.get('SIGNALS_ALLOW_TO_NOTIFY')
        if signals_config is None:
            for signal_enum in SignalEnum:
                add_signal_callback(signal_enum)
        elif isinstance(signals_config, list):
            for signal_enum in signals_config:
                add_signal_callback(signal_enum)
        elif isinstance(signals_config, dict):
            # todo
            pass
        return ext

    def send_notification(self, data):
        if self.api:
            retry_times = 3
            while retry_times > 0:
                try:
                    resp = requests.post(self.api, json=data)
                    if resp.status_code == 200:
                        break
                except requests.RequestException:
                    pass
                time.sleep(1)
                retry_times -= 1

    def spider_error(self, failure, response, spider):
        content = "Spider Error on {0}, traceback: {1}".format(response.url, failure.getTraceback())
        logger.error(content)
        self.send_notification({
            "title": "{} Spider Error".format(spider.name),
            "content": content
        })

    def item_error(self, item, response, spider, failure):
        content = "Item Pipeline on {0}, traceback: {1}\nitem: {2}".format(
            type(item),
            failure.getTraceback(),
            json.dumps(dict(**item)), )
        self.send_notification({
            "title": "{1} Spider {1} item error".format(spider.name, type(item).__name__),
            "content": content
        })

    def spider_opened(self, spider):
        content = "opened spider {}".format(spider.name)
        self.send_notification({
            "title": "{} Spider Opened".format(spider.name),
            "content": content
        })

    def spider_closed(self, spider, reason):
        content = "closed spider {}, reason: {}".format(spider.name, reason)
        self.send_notification({
            "title": "{} Spider Closed".format(spider.name),
            "content": content
        })

    def spider_idle(self, spider):
        self.send_notification({
            "title": "{} Spider turn idle".format(spider.name),
            "content": ""
        })
