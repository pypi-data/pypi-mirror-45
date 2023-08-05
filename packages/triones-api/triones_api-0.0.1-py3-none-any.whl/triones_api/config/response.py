# status_code != 200 时伪造的响应code.
ERROR_CODE = -1


class ConnectError:
    """请求发生错误时的响应"""

    def __init__(self):
        self.status_code = None
