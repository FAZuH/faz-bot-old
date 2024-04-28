from typing import Any
from datetime import datetime
from dateparser import parse

from discord import Interaction


class Utils:

    @staticmethod
    async def parse_big_int(interaction: Interaction[Any], value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            await interaction.response.send_message(f"Failed parsing {value} into an integer.")

    @staticmethod
    async def parse_date(interaction: Interaction[Any], value: str) -> datetime | None:
        try:
            return parse(value)
        except ValueError:
            await interaction.response.send_message(f"Failed parsing {value} into a date.")
