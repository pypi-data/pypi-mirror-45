
import re

from dndbuddy_core import command


ADV = "ADV."
DIS = "DIS."

DC = "D.C."
MOD = "mod"
BONUS = "bonus"

PRO = "PRO"

STR = "STR"
DEX = "DEX"
CON = "CON"
INT = "INT"
WIS = "WIS"
CHA = "CHA"

ATK = "ATK"
DMG = "DMG"
SPEED = "SPEED"


REGEX = r"^terms?$"

TEXT = """\
Terms
=====
    ADV. = Advantage
           Roll twice, take the higher total
    DIS. = Disadvantage
           Roll twice, take the lower total

    D.C. = Difficulty Class
           Number to beat with an ability check

    mod = Modifier
          The +/- number associated with a stat/skill

    PRO = Proficiency
          ...

    STR = Strength
    DEX = Dexterity
    CON = Constitution
    INT = Intelligence
    WIS = Wisdom
    CHA = Charisma

    ATK = Attack
    DMG = Damage
"""


class TermsCommand(command.Command):

    HELP = "index of terms (try `terms`)"

    @staticmethod
    def match(inp):
        return re.match(REGEX, inp)

    @staticmethod
    def run(inp):
        print(TEXT)
