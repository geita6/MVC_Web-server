import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()
    admin = auto()


class GilEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def gil_decode(d):
    if GilEncoder.prefix in d:
        name = d[GilEncoder.prefix]
        return UserRole[name]
    else:
        return d
