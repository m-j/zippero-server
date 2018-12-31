from typing import List


class PrivilegeValidator:

    _readonly_keys: List[str]

    def __init__(self, keys_dict):
        self._readonly_keys = keys_dict['readonly']
        self._readwrite_keys = keys_dict['readwrite']

    def validate_request_readonly(self, request):
        pass

    def validate_request_readwrite(self, request):
        pass

