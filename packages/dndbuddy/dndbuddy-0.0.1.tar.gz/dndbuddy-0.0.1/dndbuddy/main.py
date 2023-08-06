"""
Author: Matthew Cotton <matthewcotton.cs@gmail.com>
"""

import importlib
import traceback

from dndbuddy import constants

from dndbuddy_core import colors
from dndbuddy_core import settings
from dndbuddy_core import terms


INTERACTIVE_COMMANDS = []
REFERENCE_COMMANDS = [terms.TermsCommand()]
CLASS_COMMANDS = []
RACE_COMMANDS = []
SPELL_COMMANDS = []
MISC_COMMANDS = []

COMMANDS = []


def import_modules():
    global COMMANDS

    for module_name in settings.MODULE_NAMES:
        try:
            import_module(module_name)
        except ModuleNotFoundError as exc:
            print("Couldn't find module named '{}'.".format(module_name))
        except Exception as exc:
            traceback.print_exc()
            print("Couldn't import module named '{}' (see above)\n".format(module_name))

    COMMANDS = INTERACTIVE_COMMANDS + \
        REFERENCE_COMMANDS + \
        CLASS_COMMANDS + \
        RACE_COMMANDS + \
        SPELL_COMMANDS + \
        MISC_COMMANDS


def import_module(module_name):
    module = importlib.import_module(module_name)
    commands = module.COMMANDS

    INTERACTIVE_COMMANDS.extend(commands.get("interactive", []))
    REFERENCE_COMMANDS.extend(commands.get("reference", []))
    CLASS_COMMANDS.extend(commands.get("class", []))
    RACE_COMMANDS.extend(commands.get("race", []))
    SPELL_COMMANDS.extend(commands.get("spell", []))
    MISC_COMMANDS.extend(commands.get("misc", []))


def list_commands(commands, prefix='- '):
    for command in commands:
        try:
            print(prefix + command.HELP)
        except AttributeError:
            pass


def show_help():
    print("Things {} can do:".format(constants.TITLE))

    section = lambda s: colors.white(s, bold=True)

    if INTERACTIVE_COMMANDS:
        print(section("\nInteractive commands:"))
        list_commands(INTERACTIVE_COMMANDS)

    if REFERENCE_COMMANDS:
        print(section("\nInfo pages:"))
        list_commands(REFERENCE_COMMANDS)

    if CLASS_COMMANDS:
        print(section("\nClass info:"))
        list_commands(CLASS_COMMANDS)

    if RACE_COMMANDS:
        print(section("\nRace info:"))
        list_commands(RACE_COMMANDS)

    if SPELL_COMMANDS:
        print(section("\nSpells:"))
        list_commands(SPELL_COMMANDS)

    if MISC_COMMANDS:
        print(section("\nOther commands:"))
        list_commands(MISC_COMMANDS)

    print(section("\nHelp:") + " show this menu (try `help` or `?`)")
    print(section("Quit:") + " `exit` or `quit`")


def try_all_commands(inp):
    if inp.lower() in ('help', '?'):
        return show_help()

    for command in COMMANDS:
        if command(inp):
            break
    else:
        print("I don't understand `{}`.\n\nRun `help` for hints!".format(inp))


def menu():
    while True:
        inp = input(constants.PROMPT)
        if not inp:
            continue

        if inp.lower() in ('exit', 'quit', 'gg'):
            return

        try:
            try_all_commands(inp)
            print()
        except KeyboardInterrupt:
            print("Cancelled.")


def main():
    import_modules()

    print(constants.WELCOME)
    try:
        menu()
    except KeyboardInterrupt:
        pass
    print(constants.GOODBYE)


if __name__ == '__main__':
    main()
