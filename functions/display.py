import functions.formatting as formatting
from termcolor import colored, cprint

def details(commandLine: str, ptt: str):
    print(formatting.section('Log Details:', False))
    print(commandLine)
    print()
    print(ptt)

def knownIssues(issues: list):
    print(formatting.section('Known Issues In Log:', True))
    if not issues:
        cprint("(No Issues Found)", 'green', attrs=['bold'])
    else:
        for i in issues:
            if issues[-1] == i:
                print(i)
                continue
            print(f"{i}\n")

def gtaRage(gta: str, rage: str):
    print(formatting.section('Base Game Versions:', True))
    print(gta)
    print(rage)

def lspdfrNative(lspdfr: str, native: str):
    print(lspdfr)
    print()
    print(native)

def upToDate(plugins: list, length: int):
    """
    This function prints the Up-To-Date plugins.

    """
    if length > 0:
        print(formatting.section(f"The Following Plugins {colored(f'Are Up-To-Date ({length}):', 'green')}", True))
        for i in plugins:
            print(i)

def outdated(plugins: list, length: int):
    """
    This function prints the outdated plugins.

    """
    if length > 0:
        print(formatting.section(f"The Following Plugins {colored(f'Need To Be Updated ({length}):', 'yellow')}", True))
        for i in plugins:
            print(i)

def deprecated(plugins: list, length: int):
    """
    This function prints the Deprecated plugins.

    """
    if length > 0:
        print(formatting.section(f"The Following Plugins {colored(f'Need To Be Removed ({length}):', 'red')}", True))
        for i in plugins:
            print(i)

def incorrect(plugins: list, length: int):
    """
    This function prints the Incorrectly Installed plugins.

    """
    if length > 0:
        print(formatting.section(f"The Following Plugins {colored(f'Were Incorrectly Installed ({length}):', 'cyan')}", True))
        for i in plugins:
            print(i)

def ignored(plugins: list, length: int):
    """
    This function prints the Ignored plugins.

    """
    if length > 0:
        print(formatting.section(f"The Following Plugins {colored(f'Were Ignored ({length}):', 'blue')}", True))
        for i in plugins:
            print(i)