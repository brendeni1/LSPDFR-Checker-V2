from packaging import version

def parseVersion(ver: str):
    """
    This function parses versions using the packaging library.
    
    The return type is 'string'.

    """
    parsed = version.parse(ver)
    
    return parsed

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