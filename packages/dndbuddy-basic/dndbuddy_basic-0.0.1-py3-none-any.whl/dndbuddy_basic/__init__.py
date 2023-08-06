
from dndbuddy_basic import alignments
from dndbuddy_basic import armor
from dndbuddy_basic import combat
from dndbuddy_basic import createcharacter
from dndbuddy_basic import hitdice
from dndbuddy_basic import rolldice
from dndbuddy_basic import weapons


COMMANDS = {
    "interactive": [
        rolldice.RollDiceCommand(),
        createcharacter.CreateCharacterCommand(),
    ],
    "reference": [
        alignments.AlignmentsCommand(),
        armor.ArmorCommand(),
        combat.CombatCommand(),
        hitdice.HitDiceCommand(),
        weapons.WeaponsCommand(),
    ],
    "class": [],
    "race": [],
    "spell": [],
    "misc": [],
}
