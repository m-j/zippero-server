from dataclasses import dataclass
from functools import reduce
from typing import List, Dict
from tornado.httputil import HTTPServerRequest
import bcrypt
import base64

api_key_header = 'Zippero-Api-Key'


@dataclass(frozen=True)
class KeyEntry:
    key_hash: bytes
    name: str

    def matches_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.key_hash)


def create_key_entry(dict_entry: Dict[str, str]):
    key = dict_entry['key']
    name = dict_entry['name']

    base_64_hashed = base64.b64decode(key.encode('utf-8'))

    return KeyEntry(base_64_hashed, name)

class PrivilegeValidator:
    _readonly_entries: List[KeyEntry]
    _readwrite_entries: List[KeyEntry]

    def load_keys(self, keys: Dict):
        self._readonly_entries = [create_key_entry(entry) for entry in keys['readonly']]
        self._readwrite_entries = [create_key_entry(entry) for entry in keys['readwrite']]

    def is_security_enabled(self):
        return len(self._readonly_entries) + len(self._readwrite_entries) > 0

    def validate_request_readonly(self, request: HTTPServerRequest):
        return self._validate_request(request, self._readonly_entries) or self.validate_request_readwrite(request)

    def validate_request_readwrite(self, request: HTTPServerRequest):
        return self._validate_request(request, self._readwrite_entries)

    def _validate_request(self, request, entries: List[KeyEntry]):
        if not self.is_security_enabled():
            return True
        if api_key_header not in request.headers.keys():
            return False

        api_key_value = request.headers.get(api_key_header)
        matches_any_key = reduce(lambda acc, ent: acc or ent.matches_password(api_key_value), entries,
                                 False)
        return matches_any_key

