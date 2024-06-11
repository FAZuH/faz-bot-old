# type: ignore
from .model import Model

from .banned_user import BannedUser  # depends: Model
from .whitelisted_guild import WhitelistedGuild  # depends: Model
