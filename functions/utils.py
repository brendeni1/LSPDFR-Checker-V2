from packaging import version
from re import compile, findall, M, I, sub
from requests import get as getAPI

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

def findPlugins(logString: str, logSplit: list):
    """
    This function finds the plugins in a user's log.

    The return type is 'list'.

    """
    rStart = compile(".*Folder\sis\s.*plugins\\\lspdfr", M | I)
    
    searchStart = findall(rStart, logString)
    
    if not searchStart:
        return None

    rEnd = compile("^.*LSPD First Response: Creating Plugin: .*", M | I)
    
    searchEnd = findall(rEnd, logString)
    
    if not searchEnd:
        return None

    start = logSplit.index(searchStart[0]) + 1
    end = logSplit.index(searchEnd[0])

    section = logSplit[start:end]

    r = compile("^(?:.*LSPD First Response: )(.*?)(?:, Version=)(\d+\.\d+\.\d+\.\d+)(?:, Culture=)(.*?)(?:, PublicKeyToken=)(\w*|\d*)$", M | I)

    foundPlugins = []

    for i in section:
        breakdown = findall(r, i)
        if not breakdown:
            continue
        foundPlugins.append(breakdown[0])

    return foundPlugins

def getID(ids: dict, name: str):
    """
    This function finds the plugins ID.

    The return type is 'int'.

    """
    id = ids.get(name)
    return id

def getLatest(pluginID: str):
    """
    This function finds the plugins latest version from the LSPDFR Download Center API.

    The return type is 'str'.

    """
    response = getAPI(
        f'https://www.lcpdfr.com/applications/downloadsng/interface/api.php?fileId={pluginID}&textOnly=true&do=checkForUpdates',
    )
    
    if response.status_code >= 500:
        raise Exception(f"There is an issue with the LSPDFR Download Center API at the moment. (Error Code: {response.status_code})")
    
    if response.status_code == 429:
        raise Exception(f"You are making too many queries to lcpdfr.com. Try closing some tabs if you have them open. (Error Code: {response.status_code})")
    
    latest = sub(r"(\()|(\))", "", response.text)
    return latest