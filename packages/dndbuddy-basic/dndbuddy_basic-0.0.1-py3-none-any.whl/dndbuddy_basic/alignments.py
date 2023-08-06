
import re

from dndbuddy_core import command
from dndbuddy_core import pager


REGEX = r"^align(ments?)?$"

TEXT = """\
Alignment
=========

                  M   O   R   A   L   I   T   Y

              Good           Neutral          Evil
        +---------------+---------------+---------------+
      L |               |               |               |
      a |               |               |               |
  L   w |               |               |               |
      f |      LG       |      LN       |      LE       |
  A   u |               |               |               |
      l |               |               |               |
  W     |               |               |               |
        +---------------+---------------+---------------+
  F   N |               |               |               |
      e |               |               |               |
  U   u |               |               |               |
      t |      NG       | True  Neutral |      NE       |
  L   r |               |               |               |
      a |               |               |               |
  N   l |               |               |               |
        +---------------+---------------+---------------+
  E   C |               |               |               |
      h |               |               |               |
  S   a |               |               |               |
      o |      CG       |      CN       |      CE       |
  S   t |               |               |               |
      i |               |               |               |
      c |               |               |               |
        +---------------+---------------+---------------+


          Morality                            Lawfulness
          --------                            ----------
Tendency to do things in the        Interest in upholding/respecting
interest of:                        the law:
    - principle (good)                  - always       (lawful)
    - need      (neutral)               - if practical (neutral)
    - impulse   (evil)                  - never        (chaotic)
"""


class AlignmentsCommand(command.Command):

    HELP = "alignment info (try `alignment`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        pager.paged(TEXT)
