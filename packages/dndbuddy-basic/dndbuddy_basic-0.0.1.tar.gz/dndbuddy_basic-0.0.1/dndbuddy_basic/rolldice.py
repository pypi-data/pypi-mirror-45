
import random
import re

from dndbuddy_core import colors
from dndbuddy_core import command


REGEX = r"^(\d+)?d(\d+) ?([\+\-]\d+)?( ?( w(ith)? )?(a|ad|adv|advan|advantage|d|dis|disadv|disadvan|disadvantage))?$"


def roll_plain(dice, base):
    return [random.randint(1, base) for _ in range(dice)]


class RollDiceCommand(command.Command):

    HELP = "roll dice (try `3d8` or `2d6-3` or `3d10 disadvantage`, etc.)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    def run(inp):
        match = RollDiceCommand.match(inp)
        (dice, base, mod) = match.groups()[:3]
        buff = match.groups()[-1]

        if not dice:
            dice = 1
        dice = int(dice)

        base = int(base)

        if not mod:
            mod = 0
        mod = int(mod)
        modtext = "{:+}".format(mod)
        if mod > 0:
            modtext = colors.green(modtext)
        elif mod < 0:
            modtext = colors.red(modtext)

        if base == 0:
            print("Base can't be 0, sorry!")
            return

        rolls = roll_plain(dice, base)
        total = sum(rolls) + mod
        if buff:
            rolls_2 = roll_plain(dice, base)
            total_2 = sum(rolls_2) + mod
            print("Roll 1:  {}  from {} {}".format(total, rolls, modtext))
            print("Roll 2:  {}  from {} {}".format(total_2, rolls_2, modtext))
            if buff.startswith('a'):
                print(colors.green("With advantage..."))
                if total_2 > total:
                    rolls = rolls_2
                total = max(total, total_2)
            else:
                print(colors.red("With disadvantage..."))
                if total_2 < total:
                    rolls = rolls_2
                total = min(total, total_2)
            print()

        print("Roll:  {}  from {} {}".format(colors.green(total), rolls, modtext))
