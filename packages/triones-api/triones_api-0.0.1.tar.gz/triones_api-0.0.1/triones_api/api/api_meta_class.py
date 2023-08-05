import re
from ..config import api_config


class APIMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        if name not in api_config.gen_func_class_names:
            return type.__new__(mcs, name, bases, attrs)

        new_funcs = {}
        for api_group_name, api_data in attrs.get('api').items():
            # 每个子项都要处理为一个方法
            for f_name, f_url in api_data.items():
                new_func = mcs.gen_func(api_group_name, f_name, f_url)
                new_funcs[f_name] = new_func
        new_funcs.update(attrs)
        return type.__new__(mcs, name, bases, new_funcs)

    def gen_func(api_group_name, f_name, f_url):
        """
        动态生成方法.
        :param api_group_name:  api组名
        :param f_name:          方法名
        :param f_url:           方法url
        :return: function
        """

        def infer_request_method():
            """获取请求方法"""
            action = f_name.split("_", 1)[0]
            for k, v in api_config.keywords.items():
                if action in v:
                    return k
            raise ValueError("Unknown Keyword '{}' in '{}'".format(action, f_name))

        def func(self, *args, **kwargs):
            """
            :param self: 调用者
            :param args: url中的参数
            :return: dict: 请求结果.
            """

            # 请求url
            request_url = f_url

            # 处理url中关键字参数,既{key:value}格式.
            keyword_params = re.findall("\{([^{}]+?):([^{}]+?)\}", f_url)
            # 将request_url中的关键字参数替换为真实值.
            for kp in keyword_params:
                # 调用时没有传入关键字参数,就取默认值,否则取传入的参数, param=""视为传入了参数
                kp_value = kp[1] if kwargs.get(kp[0]) is None else kwargs.get(kp[0])
                request_url = re.sub("\{" + kp[0] + ":[^{}]+?\}", kp_value, request_url)

            # 处理url中位置参数,既{key}格式.将{key}替换为{},再用*args填充.
            request_url = re.sub("\{([^:]*?)\}", "{}", request_url)
            request_url = "/".join([self.base_url, api_group_name, request_url.format(*args)])

            # log内容
            log_data = [f_name] + list(args)
            # 请求数据
            data = kwargs.get('data')
            # 请求方法
            request_method = infer_request_method()

            # 发送请求
            res = self._request(request_method, request_url, data, log_data)
            return res

        return func
