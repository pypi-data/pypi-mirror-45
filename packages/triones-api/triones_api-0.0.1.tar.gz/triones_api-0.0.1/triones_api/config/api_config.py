base_url = "https://crm.meiqia.com/api/v1.0"

# 需要动态生成方法的类名
gen_func_class_names = ["Tenant"]

# 根据api方法名首个单词确定http请求方法
keywords = {
    "get": ["get", "dsl"],
    "post": ["post", "add", "create", "set"],
    "put": ["update", "append", "pop" "start", "stop", "modify"],
    "delete": ["delete", "clear"]
}

"""
定义api:
    - one 表示服务名
    - get_meta 方法名
    - {meta_name} 位置参数
    - {query:offset=0&limit=500&order_by=created_at&order_flag=DESC} 关键字参数, 参数名:默认值
"""

api = {
    "one": {
        "get_metas": "all-metas?acl=false",
        "get_meta": "{meta_name}/meta",
        "get_records": '{meta_name}/query?{query:offset=0&limit=500&order_by=created_at&order_flag=DESC}',
        "get_record": "{meta_name}/{id}",
        "create_record": "{meta_name}",
        "update_record": "{meta_name}/{id}",
        "delete_record": "{meta_name}/{id}/?version={version}",
        "dsl_query": "dsl/query?dsl={dsl}",
        "get_common_scripts": "common-scripts",
        "get_common_script": "common-scripts/{name}",
        "create_territory_type": "",
    },
    "one/service/territory": {
        "get_territory_types": "type",
        "create_territory_type": "type",
        "update_territory_type": "type/name",
        "get_territory_models": "model?offset=-1&limit=-1",
        "create_territory_model": "model",
        "get_territory_nodes": "node/query?tenant_id={tenant_id}",
        "add_public_territory_node": "node",
        "add_private_territory_node": "node/private/{user_id}",
        "update_territory_node": "node/{territory_id}/config",
        "get_territory_members_in_node": "node/{territory_id}/member?offset=-1&limit=-1",
        "get_territory_members": "member?limit=-1&offset=-1",
        "add_member": "member",
        "delete_member": "member/{member_id}",
        "add_territory_permission": "permission",
        "add_member_to_node": "node/{node_id}/member",
        "remove_member_from_node": "node/{node_id}/member",
        "add_member_to_permission": "member-permission",
        "remove_member_from_permission": "member-permission",
    },
    "meta-manager": {
        "create_standard": "{meta_name}/meta",
        "delete_standard": "{meta_name}/meta",
        "update_display_name": "{meta_name}/meta/modify-displayName",
        "append_column": "{meta_name}/meta/add",  # meta增加/删除一列是put方法,只能单独给个名字了.
        "pop_column": "{meta_name}/meta/drop",
        "update_column": "{meta_name}/meta/schema",
        "get_trigger": "{meta_name}/meta/trigger",
        "set_trigger": "{meta_name}/meta/trigger",
        "get_select_filters": "{meta_name}/meta/select-filters",
        "get_select_filter": "{meta_name}/meta/select-filters/{name}",
        "add_select_filter": "{meta_name}/meta/select-filters",
        "update_select_filter": "{meta_name}/meta/select-filters/{name}",
        "delete_select_filter": "{meta_name}/meta/select-filters/{name}",
        "get_sharing_rules": "sharing-rule/all",
        "add_sharing_rule": "sharing-rule",
        "delete_sharing_rule": "sharing-rule/{id}",
        "add_common_script": "common-scripts",
        "delete_common_script": "common-scripts/{name}",
        "get_manual_sharing_rows": "{std_name}/manual-sharing-row/record/{record_id}",
        "get_manual_sharing_row": '{std_name}/manual-sharing-row?row_ids=["{row_id}"]',
        "add_manual_sharing_row": '{std_name}/manual-sharing-row',
        "update_manual_sharing_row": '{std_name}/manual-sharing-row/{row_id}',
        "delete_manual_sharing_row": '{std_name}/manual-sharing-row/{row_id}',
        "create_search_index": 'service/search/index',
        "create_search_fields": 'service/search/fields',
        "get_validations": "{meta_name}/meta/validations",
        "get_validation": "{meta_name}/meta/validations/{name}",
        "add_validation": "{meta_name}/meta/validations",
        "delete_validation": "{meta_name}/meta/validations/{name}",
        "update_validation": "{meta_name}/meta/validations/{name}",
        "stop_validation": "{meta_name}/meta/validations/{name}/inactive",
        "start_validation": "{meta_name}/meta/validations/{name}/active",
    },
    "acl_admin": {
        "get_profiles": "basic_profile",
        "get_profile": "advanced_profile/{profile_id}",
        "add_profile": "profile",
        "delete_profile": "profile/{profile_id}",
        "append_ola_to_profile": "profile/{profile_id}/object_level_access",
        "append_fla_to_profile": "profile/{profile_id}/field_level_access",
        "append_function_level_access_to_profile": "profile/{profile_id}/function_level_access",
        "get_users_in_profile": "profile/{profile_id}/user",
        "add_user_to_profile": "profile/{profile_id}/user",
        "add_users_to_profile": "profile/{profile_id}/users",
        "get_permission_sets": "permission_set",
        "get_permission_set": "permission_set/{permission_id}",
        "add_permission_set": "permission_set",
        "add_user_to_permission_set": "permission_set/{permission_id}/user",
        "add_user_to_sys_permission_set": "system_permission_set/{sys_permission_name}/user",
        "remove_user_from_permission_set": "permission_set/{permission_id}/user/{user_id}",
        "get_users_in_permission_set": "permission_set/{permission_id}/user",
        "get_owd": "organization_wide_default",
        "add_owd": "organization_wide_default",
        "clear_OLA": "object_level_access",
        "clear_FLA": "field_level_access",
    },
    "layout/config": {
        "set_layout": "",
        "get_layout_link": "?platform={platform}&layout_name={layout_name}",
        "get_layout_links": "?platform={platform}",
    },
    "one/service/approvals/template/": {
        "get_approval_templates": "?option=All",
        "get_approval_template": "{id}",
        "add_approval_template": "",
        "update_approval_template": "{id}",
        "delete_approval_template": "{id}",
        "start_approval_template": "{id}/active",
        "stop_approval_template": "{id}/inactive",
    },
    "tenant-gateway": {
        "get_tenant_info": "tenant/org/{id}",
        "get_tenant_id": "verify_token",
        "update_tenant": "tenant/org/update"
    }
}
