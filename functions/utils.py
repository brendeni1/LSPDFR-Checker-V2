from packaging import version
from re import compile, findall, M
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

def getLatest(pluginID: str):
    """
    This function finds the plugins latest version from the LSPDFR Download Center API.

    The return type is 'str'.

    """
    response = getAPI(
        f'https://www.lcpdfr.com/applications/downloadsng/interface/api.php?fileId={pluginID}&textOnly=true&do=checkForUpdates',
    )
    
    if response.status_code >= 500:
        raise f"There is an issue with the LSPDFR Download Center API at the moment. (Error Code: {response.status_code})"
    
    if response.status_code == 429:
        raise f"You are making too many queries to lcpdfr.com. Try closing some tabs if you have them open. (Error Code: {response.status_code})"
    
    latest = response.text
    return latest