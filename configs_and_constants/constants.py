from enum import Enum


class Roles(Enum):
    user = "user"


class ContentTypes(Enum):
    video = "video"


class CollectionNames(Enum):
    roles = "roles"
    users = "users"
