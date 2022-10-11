from re import compile, findall, I

def gta(log: str):
    """
    This function returns the user's GTAV version.
    
    The return type is 'string'.

    """
    r = compile('(?:.*?Product\sversion\:\s)(.*)', I)
    search = findall(r, log)
    if not search:
        return None
    return search[0]

def rage(log: str):
    """
    This function returns the user's RAGE version.
    
    The return type is 'string'.

    """
    r = compile('(?:.*v)(.*)(?:\sfor.*)', I)
    search = findall(r, log)
    if not search:
        return None
    return search[0]