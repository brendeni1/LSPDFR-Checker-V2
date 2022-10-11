import re

def pluginTimeout(log: str):
    """
    This function returns the Plugin Timeout Threshold. If it isn't in the log, None is returned.
    
    The return type is 'list'.

    """
    r = re.compile("(?:.*?Read value:\s)(\d{5})")
    timeout = re.findall(r, log)
    if not timeout:
        return None
    
    return timeout[0]

def commandLineArgs(log: str):
    """
    This function returns a list of command line arguments. If none are in the log, None is returned.
    
    The return type is 'list'.

    """
    r = re.compile("(?:.*Command line option\s)(?:\"|'|-)(.*?)(?:'|\")?(?:\s.*)")
    options = re.findall(r, log)
    if not options:
        return None
    
    return options