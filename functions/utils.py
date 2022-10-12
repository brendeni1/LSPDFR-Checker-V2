from packaging import version
from re import compile, findall, M

def parseVersion(ver: str):
    """
    This function parses versions using the packaging library.
    
    The return type is 'string'.

    """
    try:
        parsed = version.parse(ver)
        return parsed
    except:
        return None

def compareVersion(installed: str, latest: str):
    """
    This function compares version numbers. If the version2 is bigger, a truthy value is returned.
    
    The return type is 'bool'.

    """
    installed = version.parse(installed)
    latest = version.parse(latest)

    if installed < latest:
        return True
    return False

def findPlugins(logString: str):
    """
    This function finds the plugins in a user's log.

    The return type is 'list'.

    """
    r = compile("^(?:.*LSPD First Response: )(.*?)(?:, Version=)(\d+\.\d+\.\d+\.\d+)(?:, Culture=)(.*?)(?:, PublicKeyToken=)(\w*|\d*)$", M)
    search = findall(r, logString)
    listOfPlugins = []
    for i in search:
        listOfPlugins.append(list(i))
    return listOfPlugins

def getID(ids: dict, name: str):
    """
    This function finds the plugins ID.

    The return type is 'int'.

    """
    id = ids.get(name)
    return id