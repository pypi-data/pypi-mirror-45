from tcell_agent.rust.models.utils import convert_params, convert_post_params, convert_multidict_params


class PatchesRequest(dict):
    def __init__(self, appsensor_meta):
        dict.__init__(self)
        # todo: cache these params if/when Patches requests converts them so they're not double converted.  sep. PR
        post_params_list = convert_post_params(appsensor_meta.post_dict, appsensor_meta.files_dict,
                                               appsensor_meta.encoding)

        self["full_uri"] = appsensor_meta.location
        self["method"] = appsensor_meta.method
        self["path"] = appsensor_meta.path
        self["remote_address"] = appsensor_meta.remote_address
        self["request_bytes_length"] = appsensor_meta.request_content_bytes_len
        # todo: cache these params if/when Patches requests converts them so they're not double converted.  sep. PR
        self["query_params"] = convert_multidict_params(appsensor_meta.get_dict, appsensor_meta.encoding)
        self["post_params"] = post_params_list
        self["headers"] = convert_params(appsensor_meta.encoding, appsensor_meta.headers_dict)
        self["cookies"] = convert_params(appsensor_meta.encoding, appsensor_meta.cookie_dict)
