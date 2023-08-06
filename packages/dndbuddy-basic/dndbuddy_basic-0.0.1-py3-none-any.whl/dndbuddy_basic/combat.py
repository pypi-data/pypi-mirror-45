
import re

from dndbuddy_core import command


REGEX = r"^combat$"

TEXT = """\
Order of Play
-------------

    1) Move
    2) Action
    3) Bonus action
    4) Reaction

    Acronym to remember order of play:  "may-bar"  (M A Ba R)"""


class CombatCommand(command.Command):

    HELP = "combat info (try `combat`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        print(TEXT)
