# type: ignore
from .logger import Logger

from .console_logger import ConsoleLogger
from ._discord_logger import DiscordLogger  # ConsoleLogger
from ._performance_logger import PerformanceLogger

from .fazbot_logger import FazBotLogger  # Logger
