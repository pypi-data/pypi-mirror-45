import requests
import logging
import json
from .api_meta_class import APIMetaClass
from ..config import api_config, response, log


class Tenant(metaclass=APIMetaClass):
    """
    以APIMetaClass为元类,加载api_config.api数据,生成方法.
    """
    __doc__ = json.dumps(api_config.api, ensure_ascii=False, indent=2)
    base_url = api_config.base_url
    api = api_config.api

    def __init__(self, x_token):
        self.header = {"x-token": x_token, "Content-Type": "application/json"}

    def _request(self, method, url, data, *args):
        try:
            if not isinstance(data, str):
                data = json.dumps(data)
            r = requests.request(method, url, data=data, headers=self.header)
        except IOError:
            r = response.ConnectError()
        return self._check_response(r, *args)

    @staticmethod
    def _check_response(res, *args):
        """
        1.检查响应,记录日志
        """
        status_code = res.status_code

        # 请求失败时,构造一个响应,便于后续处理
        if status_code != 200:
            logging.error("请求失败!status_code:{}".format(status_code))
            return {"code": response.ERROR_CODE, "message": "status_code:{}".format(status_code)}

        content = json.loads(res.content.decode())
        if len(args) > 0:
            # 根据code不同,记录不同等级的日志
            code = content.get('code')
            if code == 0:
                logging.info('{}, code: {}'.format(args, content.get('code')))
            else:
                logging.warning(
                    '{}, code:{}, message:{}'.format(args, content.get('code'), content.get('message', '')))

        return content
