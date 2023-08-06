
import re

from dndbuddy_core import command


REGEX = r"^(make|create|new) (player|ch|char|character|sheet)$"

STEP_1 = """Step 1:  ..."""


class CreateCharacterCommand(command.Command):

    HELP = "character creation helper (try `new character`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        print(STEP_1)
