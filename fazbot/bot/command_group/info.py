from discord.app_commands import Group

from . import GroupBase


class Info(GroupBase, Group):

    def setup(self) -> None:
        Group.__init__(self, name="info", description="Information commands.")
        self._setup(self)
