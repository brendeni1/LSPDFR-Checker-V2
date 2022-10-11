import os
import re
from time import time
import json
from termcolor import colored, cprint

# Custom module imports
import functions.logDetails as logDetails
import functions.formatting as formatting
import functions.knownIssues as knownIssues
import functions.mainVersions as mainVersions
import functions.utils as utils

# Clear terminal based on OS.
userOS = os.name

# Import config.
with open("./config.json") as config:
    config = json.load(config)

# Import ids.
with open("./ids.json") as ids:
    ids = json.load(ids)

if userOS == 'nt':
    os.system('cls')
else:
    os.system('clear')

# Tell user that the script has started.
print(formatting.title('SCRIPT STATUS:'), '\n')

# Get all files.
dirFiles = lambda : os.listdir('./')

# Look for log file.
def getLog():
    fileList = dirFiles()
    r = re.compile("^(.*)RagePluginHook(.*).log$", re.I)
    searchedFiles = list(filter(r.match, fileList))
    if not searchedFiles:
        return None
    return searchedFiles[0]

logFile = getLog()

# Verify the log file exists.
if not logFile:
    print(formatting.statusUpdate('no log found', False))
    cprint(f"ERROR: There is no log in the current directory! Drop a log file in: \"{os.getcwd()}\"", 'red', attrs=['bold'])
    exit(1)
else:
    print(formatting.statusUpdate('found log', True), '\n')

# Open log and assign to var.
with open(f"./{logFile}", encoding="utf8") as log:
    logString = log.read()
    logSplit = logString.split('\n')

# Get plugin timeout threshold.
timeout = logDetails.pluginTimeout(logString)

if not timeout:
    timeout = '(None Set)'
    print(formatting.statusUpdate('no plugin timeout threshold found', False))
else:
    print(formatting.statusUpdate('plugin timeout threshold found', True))

# Get command line options.
commandLine = logDetails.commandLineArgs(logString)

if not commandLine:
    commandLine = '(None Set)'
    print(formatting.statusUpdate('no command line args found\n', False))
else:
    commandLine = ',\n'.join(list(dict.fromkeys(commandLine)))
    print(formatting.statusUpdate('command line args found\n', True))

# Check the log for known issues.
issues = knownIssues.check(config['issues'], logString)

if not issues:
    issues = [colored('(No Issues Found)', 'green', attrs=['bold'])]
    print(formatting.statusUpdate('no common issues found\n', True))
else:
    issues = [colored(x + '\n', 'red', attrs=['bold']) for x in issues]
    print(formatting.statusUpdate('common issues found\n', True))


# Check the user's GTA 5 version.
gtaVersion = mainVersions.gta(logString)

if not gtaVersion:
    print(formatting.statusUpdate('no gta5 version found', False))
    cprint(f"ERROR: There was an issue getting the GTA 5 version! Please report this to me (DarkVypr).", 'red', attrs=['bold'])
    exit(1)

compareGTAVersion = utils.compareVersion(gtaVersion, config['main']['gta'])

if compareGTAVersion:
    print(formatting.statusUpdate('old gta5 version found', False))
    gtaVersion = colored(f"GTA 5 version is out-of-date! Installed: {gtaVersion}, Latest: {config['main']['gta']}", 'red', attrs=['bold'])
else:
    print(formatting.statusUpdate('good gta5 version found', True))
    gtaVersion = colored(f"GTA 5 version is up-to-date! Installed: {gtaVersion}, Latest: {config['main']['gta']}", 'green', attrs=['bold'])


# Check the user's RAGE version.
rageVersion = mainVersions.rage(logString)

if not rageVersion:
    print(formatting.statusUpdate('no rage version found', False))
    cprint(f"ERROR: There was an issue getting the RAGE version! Please report this to me (DarkVypr).", 'red', attrs=['bold'])
    exit(1)

compareRageVersion = utils.compareVersion(rageVersion, config['main']['rage'])

if compareRageVersion:
    print(formatting.statusUpdate('old rage version found', False))
    rageVersion = colored(f"RAGEPluginHook version is out-of-date! Installed: {rageVersion}, Latest: {config['main']['rage']}", 'red', attrs=['bold'])
else:
    print(formatting.statusUpdate('good rage version found', True))
    rageVersion = colored(f"RAGEPluginHook version is up-to-date! Installed: {rageVersion}, Latest: {config['main']['rage']}", 'green', attrs=['bold'])


# Check the user's LSPDFR version.
lspdfrVersion = mainVersions.lspdfr(logString)

if not lspdfrVersion:
    print(formatting.statusUpdate('no lspdfr version found', False))
    cprint(f"ERROR: There was an issue getting the LSPDFR version! The user's game probably crashed before LSPDFR was able to load.", 'red', attrs=['bold'])
    exit(1)

compareLSPDFRVersion = utils.compareVersion(lspdfrVersion, config['main']['lspdfr'])

if compareLSPDFRVersion:
    print(formatting.statusUpdate('old lspdfr version found', False))
    lspdfrVersion = colored(f"LSPDFR version is out-of-date! Installed: {lspdfrVersion}, Latest: {config['main']['lspdfr']}", 'red', attrs=['bold'])
else:
    print(formatting.statusUpdate('good lspdfr version found', True))
    lspdfrVersion = colored(f"LSPDFR version is up-to-date! Installed: {lspdfrVersion}, Latest: {config['main']['lspdfr']}", 'green', attrs=['bold'])

# Check the user's RAGENativeUI version.
nativeuiVersion = mainVersions.nativeui(logString)

if not nativeuiVersion:
    print(formatting.statusUpdate('no RAGENativeUI version found\n', False))
    nativeuiVersion = colored(f"RAGENativeUI version was not found in log! Installed: {nativeuiVersion}, Latest: {config['main']['nativeui']}", 'yellow', attrs=['bold'])
else:
    comparenativeuiVersion = utils.compareVersion(nativeuiVersion, config['main']['nativeui'])

    if comparenativeuiVersion:
        print(formatting.statusUpdate('old RAGENativeUI version found\n', False))
        nativeuiVersion = colored(f"RAGENativeUI version is out-of-date! Installed: {nativeuiVersion}, Latest: {config['main']['nativeui']}", 'red', attrs=['bold'])
    else:
        print(formatting.statusUpdate('good RAGENativeUI version found\n', True))
        nativeuiVersion = colored(f"RAGENativeUI version is up-to-date! Installed: {nativeuiVersion}, Latest: {config['main']['nativeui']}", 'green', attrs=['bold'])