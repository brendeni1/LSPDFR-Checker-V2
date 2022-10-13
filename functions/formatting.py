class col:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def title(name: str):
    """
    This function returns a formatted string used for titles. It is a underlined, bolded, capitalized string.
    
    The return type is 'string'.

    """
    formatted = col.BOLD + col.UNDERLINE + name + col.END
    
    return formatted

def separator():
    """
    This function returns the standard separator when called (\\n\\n----------\\n\\n).
    
    The return type is 'string'.

    """
    return "\n\n----------\n\n\n"

def section(label: str, separated: bool):
    """
    This function returns a section, optionally separated by the separator.
    
    The return type is 'string'.

    """
    formatted = f"{col.BOLD}{col.UNDERLINE}{label}{col.END}\n"
    if separated:
        formatted = separator() + f"{col.BOLD}{col.UNDERLINE}{label}{col.END}\n"
        return formatted
    return formatted

def statusUpdate(description: str, isSuccess: bool):
    """
    This function takes a description (string), and prints it as text to the console.
    
    isSuccess is meant to determine if the operation was successful or no, and should be supplied along with the function call. False will return a red message, and True will be green.

    The return type is 'string'.

    """
    formatted = None
    
    if not isSuccess:
        formatted = col.BOLD + col.RED + '❌ FAIL -->  ' + description.upper() + col.END  
        return formatted
    
    formatted = col.BOLD + col.GREEN + '✅ SUCCESS -->  ' + description.upper() + col.END
    
    return formatted