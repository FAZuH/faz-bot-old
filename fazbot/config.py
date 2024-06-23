from __future__ import annotations
from pathlib import Path
from typing import Any, TYPE_CHECKING

from yaml import Dumper, Loader, dump, load

if TYPE_CHECKING:
    from pathlib import Path


class Config:

    def __init__(self, config_fp: str | Path) -> None:
        self._fp = Path(config_fp) if isinstance(config_fp, str) else config_fp
        self._config: dict[str, Any] = {}

    def read(self) -> None:
        with open(self._fp, "r") as stream:
            self._config = load(stream, Loader=Loader)

        app = self._config["application"]
        self.admin_discord_id = int(app["admin_discord_id"])
        self.dev_server_id = int(app["dev_server_id"])

        logging = self._config["logging"]
        self.discord_log_webhook = logging["discord_log_webhook"]
        self.discord_status_webhook = logging["discord_status_webhook"]

        secret = self._config["secret"]

        secret_discord = secret["discord"]
        self.discord_bot_token = secret_discord["bot_token"]

        secret_fazbot = secret["fazbot"]
        self.fazbot_db_username = secret_fazbot["username"]
        self.fazbot_db_password = secret_fazbot["password"]
        self.fazbot_db_max_retries = secret_fazbot["max_retries"]
        self.fazbot_db_name = secret_fazbot["database_name"]

        secret_wynndb = secret["wynndb"]
        self.wynndb_db_username = secret_wynndb["username"]
        self.wynndb_db_password = secret_wynndb["password"]
        self.wynndb_db_max_retries = secret_wynndb["max_retries"]
        self.wynndb_db_name = secret_wynndb["database_name"]

    def save(self) -> None:
        with open(self._fp, "w") as stream:
            dump(self._config, stream, Dumper)
