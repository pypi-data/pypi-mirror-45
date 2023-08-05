# README

## API方法的定义

- 所有的API方法在 `config/api_config.py` 文件中定义, 创建类时动态生成;

- 举例说明:
    - one 表示服务名.
    - get_meta 方法名, 其中包含请求方法.
    - {meta_name}/meta 请求url
    - {meta_name} 位置参数.
    - {query:offset=0&limit=500&order_by=created_at&order_flag=DESC} 关键字参数, 参数名:默认值.
    - 采用data关键字表示post数据,例如`create_record("Account", data={"objects": [{"t1": "测试客户"}]})`

    ```javascript
    api = {
        "one": {
            "get_metas": "all-metas?acl=false",
            "get_meta": "{meta_name}/meta",
            "get_records": "{meta_name}/query?{query:offset=0&limit=500&order_by=created_at&order_flag=DESC}",
            "get_record": "{meta_name}/{id}",
            "create_record": "{meta_name}",
            "update_record": "{meta_name}/{id}",
            "delete_record": "{meta_name}/{id}?version={version}",
            "dsl_query": "dsl/query?dsl={dsl}"
        },
        "meta-manager": {
            "create_standard": "{meta_name}/meta",
            "delete_standard": "{meta_name}/meta",
            "update_display_name": "{meta_name}/meta/modify-displayName",
            "add_column": "{meta_name}/meta/add",
            "drop_column": "{meta_name}/meta/drop",
            "update_column": "{meta_name}/meta/schema"
        }
    }
    ```

    - 各关键字对应的请求方法

    ```json
    {
        "get": ["get", "dsl"],
        "post": ["post", "add", "drop", "create", "set"],
        "put": ["update", "start", "stop", "modify"],
        "delete": ["delete"]
    }
    ```

## 方法的调用

参数的个数与顺序需和api_config.py文件中定义的一致.

```python
from triones_api import Tenant

token = "******"
t = Tenant(token)

# 位置参数
t.get_meta("User")
t.get_record("User", "AQACQqweGRMBAAAAAxqWI4VnaBXazAEA")
t.delete_record("Account", "AQACQqweGRMBAAAAnyK7Z6Q-cxVqXQUA", 0)

# 位置参数与关键字参数
t.get_records("Account", query='offset=0&limit=1&order_by=created_at&order_flag=DESC')
t.get_records("Account")

# 用关键字参数data表示请求数据
t.create_record("Account", data={"objects": [{"t1": "测试客户"}]})
t.update_display_name("Account", data={"display_name": "客户客户"})
```