
import re

from dndbuddy_core import command
from dndbuddy_core import pager


REGEX = r"^wea?p(ons?)?$"

TEXT = """\
Weapons
=======

    Weapons
    -------
    Name                    Damage              Properties

    Simple Melee Weapons
        Club                1d4 bludgeoning     Light
        Dagger              1d4 piercing        Finesse, light, thrown (range 20/60)
        Greatclub           1d8 bludgeoning     Two-handed
        Handaxe             1d6 slashing        Light, thrown (range 20/60)
        Javelin             1d6 piercing        Thrown (range 30/120)
        Light hammer        1d4 bludgeoning     Light, thrown (range 20/60)
        Mace                1d6 bludgeoning     ---
        Quarterstaff        1d6 bludgeoning     Versatile (1d8)
        Spear               1d6 piercing        Thrown (range 20/60), versatile (1d8)
    Simple Ranged Weapons
        Crossbow, light     1d8 piercing        Ammunition (range 80/320), loading, two-handed
        Shortbow            1d6 piercing        Ammunition (range 80/320), two-handed
    Martial Melee Weapons
        Battleaxe           1d8 slashing        Versatile (1d10)
        Greataxe            1d12 slashing       Heavy, two-handed
        Greatsword          2d6 slashing        Heavy, two-handed
        Longsword           1d8 slashing        Versatile (1d10)
        Maul                2d6 bludgeoning     Heavy, two-handed
        Morningstar         1d8 piercing        ---
        Rapier              1d8 piercing        Finesse
        Scimitar            1d6 slashing        Finesse, light
        Shortsword          1d6 piercing        Finesse, light
        Trident             1d6 piercing        Thrown (range 20/60), versatile (1d8)
        Warhammer           1d8 bludgeoning     Versatile (1d10)
    Martial Ranged Wearpons
        Crossbow, hand      1d6 piercing        Ammunition (range 30/120), light, loading
        Crossbow, heavy     1d10 piercing       Ammunition (range 100/400), heavy, loading, two-handed
        Longbow             1d8 piercing        Ammunition (range 150/600), heavy, two-handed

    Ranges
    ------
             +---------+--------------+------------+--------+
             | < Reach | Normal Range | Long Range | Beyond |
    +--------+---------+--------------+------------+--------+
    | Melee  | Normal  | ---          | ---        | ---    |
    +--------+---------+--------------+------------+--------+
    | Ranged | DIS.    | Normal       | DIS.       | ---    |
    +--------+---------+--------------+------------+--------+
    Note:  Reach (normally 5 feet) is affected by creature Size

    Weapon Proficiency
    ------------------
    SIMPLE weapon  = anyone can use
    MARTIAL weapon = only if proficient

    If you're proficient with your weapon, add your PRO bonus to ATK ROLLS

    Weapon Properties
    -----------------
    Ammunition = need one free hand to load
    Finesse    = pick STR or DEX, then apply to both the ATK *and* DMG rolls
    Heavy      = SMALL creatures have DIS. using Heavy weapons
    Light      = w/ two Light weapons, use Bonus action for 2nd (DMG mod max 0)
    Loading    = one shot takes one round, can't multi-shot
    Range      = (normal/long) in feet = (normal/DIS.)
    Reach      = adds 5 feet to reach, for ATKs and OPP-ATKs
    Special    = has additional rules, see PHB
    Thrown     = can make ranged attack, use whatever melee bonuses apply
    Two-Handed = need two hands
    Versatile  = one or two hands (two-handed DMG in parentheses)

    Improvised = 1d4/1d4 (20/60), damage type up to DM"""


class WeaponsCommand(command.Command):

    HELP = "weapon info (try `weapon`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        pager.paged(TEXT)
