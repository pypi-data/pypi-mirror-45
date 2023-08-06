
import re

from dndbuddy_core import command


REGEX = r"^hit ?(die|dice)?$"

TEXT = """\
Hit Dice
========
    Number of Hit Dice always equals the player's level (level 3 has 3 hit dice)

    Type of Hit Die (d8, d10, etc) determined by Class notes

    Resting
    -------
    During a short rest, can spend Hit Dice to recover X(d(hit die) + CON) Hit Points
    During a long rest, recover up to half of total Hit Dice, minimum of 1.
    """


class HitDiceCommand(command.Command):

    HELP = "hit dice guide (try `hit dice`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        print(TEXT)
