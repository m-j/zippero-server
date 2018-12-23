from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass(frozen=True)
class PackageMetadata:
    name: str
    semver: str

    def as_dict(self):
        d = asdict(self)
        return d


@dataclass(frozen=True)
class PackageInfo:
    name: str
    versions: List[str]
    links: Optional[Dict[str, str]]

    def as_dict(self):
        return asdict(self)
