
import re

from dndbuddy_core import command
from dndbuddy_core import pager


REGEX = r"^arm(ou?rs?)?$"

TEXT = """
Armor
=====

    Armor
    -----
    Armor                   Armor Class (AC)
    Light Armor
        Padded              11 + DEX mod
        Leather             11 + DEX mod
        Studded leather     11 + DEX mod
    Medium Armor
        Hide                12 + DEX mod (max 2)
        Chain shirt         13 + DEX mod (max 2)
        Scale mail          14 + DEX mod (max 2)
        Breastplate         14 + DEX mod (max 2)
        Half plate          15 + DEX mod (max 2)
    Heavy Armor
        Ring mail           14
        Chain mail          16
        Splint              17
        Plate               18
    Shield
        Shield              +2

    Armor Proficiency
    -----------------
    If wearer isn't proficient with their armor:
        - DIS. on ALL ability checks
        - DIS. on ALL saving throws
        - DIS. on ALL attack rolls that use STR or DEX
        - can't cast spells

    Heavy Armor
    -----------
    If wearer doesn't meet STR requirement for their armor,
    they have a penalty of -10ft. from their SPEED"""


class ArmorCommand(command.Command):

    HELP = "armor info (try `armor`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        pager.paged(TEXT)
