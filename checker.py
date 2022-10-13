import os
import re
import json
from termcolor import colored, cprint

# Custom module imports
import functions.logDetails as logDetails
import functions.formatting as formatting
import functions.knownIssues as knownIssues
import functions.mainVersions as mainVersions
import functions.utils as utils
import functions.display as display

# Clear terminal based on OS.
clearscreen = lambda userOS : os.system('cls') if userOS == 'nt' else os.system('clear')

userOS = os.name
clearscreen(userOS)

# Import config.
with open("./config.json") as config:
    config = json.load(config)

# Import ids.
with open("./ids.json") as ids:
    ids = json.load(ids)

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
    cprint(f"ERROR: There is no log in the current directory! Drop a log file in: \"{os.getcwd()}\"", 'red', attrs=['bold'])
    exit(1)

# Open log and assign to var.
with open(f"./{logFile}", encoding="utf8") as log:
    logString = log.read()
    logSplit = logString.split('\n')

# Get plugin timeout threshold.
timeout = logDetails.pluginTimeout(logString)

if not timeout:
    timeout = f"{colored('Plugin Timeout Threshold:', 'green', attrs=['bold'])} (None Set)"
else:
    timeout = f"{colored('Plugin Timeout Threshold:', 'green', attrs=['bold'])} {timeout}"

# Get command line options.
commandLine = logDetails.commandLineArgs(logString)

if not commandLine:
    commandLine = f"{colored('Command Line Arguments:', 'green', attrs=['bold'])}: (None Set)"
else:
    commandLine = colored("Command Line Arguments (New Line Delimited):\n", 'green', attrs=['bold']) + ',\n'.join(list(dict.fromkeys(commandLine)))

# Print log details to user.
display.details(commandLine, timeout)

# Check the log for known issues.
issues = knownIssues.check(config['issues'], logString)

if not issues:
    issues = [colored('(No Issues Found)', 'green', attrs=['bold'])]
else:
    issues = [colored(x, 'red', attrs=['bold']) for x in issues]

# Print issues in log to user.
display.knownIssues(issues)

# Check the user's GTA 5 version.
gtaVersion = mainVersions.gta(logString)

if not gtaVersion:
    cprint(f"ERROR: There was an issue getting the GTA 5 version! Please report this to me (DarkVypr).", 'red', attrs=['bold'])
    exit(1)

compareGTAVersion = utils.compareVersion(gtaVersion, config['main']['gta'])

if compareGTAVersion:
    gtaVersion = colored(f"GTA 5 version is out-of-date! Installed: {gtaVersion}, Latest: {config['main']['gta']}", 'red', attrs=['bold'])
else:
    gtaVersion = colored(f"GTA 5 version is up-to-date! Installed: {gtaVersion}, Latest: {config['main']['gta']}", 'green', attrs=['bold'])


# Check the user's RAGE version.
rageVersion = mainVersions.rage(logString)

if not rageVersion:
    cprint(f"ERROR: There was an issue getting the RAGE version! Please report this to me (DarkVypr).", 'red', attrs=['bold'])
    exit(1)

compareRageVersion = utils.compareVersion(rageVersion, config['main']['rage'])

if compareRageVersion:
    rageVersion = colored(f"RAGEPluginHook version is out-of-date! Installed: {rageVersion}, Latest: {config['main']['rage']}", 'red', attrs=['bold'])
else:
    rageVersion = colored(f"RAGEPluginHook version is up-to-date! Installed: {rageVersion}, Latest: {config['main']['rage']}", 'green', attrs=['bold'])

# Print GTA and RAGE Version to user.
display.gtaRage(gtaVersion, rageVersion)

# Check the user's LSPDFR version.
lspdfrVersion = mainVersions.lspdfr(logString)

if not lspdfrVersion:
    cprint(f"\nERROR: There was an issue getting the LSPDFR version! The user's game probably crashed before LSPDFR was able to load.", 'red', attrs=['bold'])
    exit(1)

compareLSPDFRVersion = utils.compareVersion(lspdfrVersion, config['main']['lspdfr'])

if compareLSPDFRVersion:
    lspdfrVersion = colored(f"LSPDFR version is out-of-date! Installed: {lspdfrVersion}, Latest: {config['main']['lspdfr']}", 'red', attrs=['bold'])
else:
    lspdfrVersion = colored(f"LSPDFR version is up-to-date! Installed: {lspdfrVersion}, Latest: {config['main']['lspdfr']}", 'green', attrs=['bold'])

# Check the user's RAGENativeUI version.
nativeuiVersion = mainVersions.nativeui(logString)

if not nativeuiVersion:
    nativeuiVersion = colored(f"RAGENativeUI version was not found in log! Installed: {nativeuiVersion}, Latest: {config['main']['nativeui']}", 'yellow', attrs=['bold'])
else:
    comparenativeuiVersion = utils.compareVersion(nativeuiVersion, config['main']['nativeui'])

    if comparenativeuiVersion:
        nativeuiVersion = colored(f"RAGENativeUI version is out-of-date! Installed: {nativeuiVersion}, Latest: {config['main']['nativeui']}", 'red', attrs=['bold'])
    else:
        nativeuiVersion = colored(f"RAGENativeUI version is up-to-date! Installed: {nativeuiVersion}, Latest: {config['main']['nativeui']}", 'green', attrs=['bold'])

# Print LSPDFR and NATIVEUI Version to user.
display.lspdfrNative(lspdfrVersion, nativeuiVersion)

# Plugin class.
class Plugin:
    def __init__(self, name, version, id, culture, publicKeyToken):
        self.name = name
        self.version = version
        self.id = id
        self.culture = culture
        self.publicKeyToken = publicKeyToken
        self.hardcoded = False
        self.latest = None
    def getVersion(self):
        parsed = utils.parseVersion(self.version)
        return parsed

# Get the user's plugins and their details.
userPlugins = utils.findPlugins(logString, logSplit)
if not userPlugins:
    cprint(f"\nSCRIPT END: No plugins were found in that log! Manual review is suggested.", 'yellow', attrs=['bold'])
    exit(0)
else:
    print(formatting.section(f"Found Plugins ({len(userPlugins)}):", True))
    print(formatting.statusUpdate(f'{len(userPlugins)} plugin(s) found\n', True))

# Parse the user's plugins into classes.
userPluginClasses = []
for i in userPlugins:
    id = utils.getID(ids, i[0])
    userPluginClasses.append(Plugin(i[0], i[1], id, i[2], i[3]))

userPlugins = userPluginClasses

# "deprecated" is for the "remove these plugins" section, and "badPlugins" is for plugins that will error out if checked -- never use them.
deprecated = []
badPlugins = []
ignored = []
incorrect = []

# Loop through all of the plugins to check if they are incorrectly installed. Append those to a list for later use if so.
for plugin in userPlugins:
    for i in config["incorrect"]:
        if plugin.name == i["name"]:
            badPlugins.append(plugin.name)
            incorrect.append(f"{plugin.name}, Current Folder: GTAV/plugins/LSPDFR - Correct Folder: {i['path']}" if i[
                'path'] else f"{plugin.name}, Current Folder: GTAV/plugins/LSPDFR - Correct Folder: [Unknown]")

# Loop through all of the plugins to check if they are blacklisted. Append those to a list for later use if so.
for plugin in userPlugins:
    if plugin.name in badPlugins:
        continue
    if plugin.name in config["blacklist"]:
        badPlugins.append(plugin.name)
        ignored.append(f"{plugin.name}, (Ignore because: Blacklisted)")

# Loop through all of the plugins to check if they are deprecated. Append those to a list for later use if so.
for plugin in userPlugins:
    if plugin.name in badPlugins:
        continue
    if plugin.name in config["deprecated"]:
        if config["deprecated"][plugin.name]:
            deprecated.append(f'{plugin.name}, {config["deprecated"][plugin.name]}')
        else:
            deprecated.append(plugin.name)
        badPlugins.append(plugin.name)
        continue

# Loop through all of the plugins to check if they have an ID. Append those to a list for later use if so.
for plugin in userPlugins:
    if plugin.name in badPlugins or config["hardcoded"].get(plugin.name):
        continue
    if not plugin.id:
        badPlugins.append(plugin.name)
        ignored.append(f"{plugin.name}, (Ignore because: No ID Available)")

# Iterate through all of the plugins and assign their versions.
for plugin in userPlugins:
    if plugin.name in badPlugins:
        continue

    if plugin.name in config["hardcoded"]:
        plugin.latest = config["hardcoded"][plugin.name]
        plugin.hardcoded = True
        continue

    latest = utils.getLatest(plugin.id)

    if not latest:
        badPlugins.append(plugin.name)
        ignored.append(f"{plugin.name}, (Ignore Because: Latest Version Not Assigned From API)")
        continue
    
    plugin.latest = latest

# Iterate through all of the plugins and check/compare their versions.
upToDate = []
outdated = []

for plugin in userPlugins:
    print(formatting.statusUpdate(f'checking plugin version for: {plugin.name}, Installed: {plugin.version} - Latest: {plugin.latest}', True), flush=True)

    pluginString = f"{plugin.name}, Installed: {plugin.version} - Latest: {plugin.latest}"
    if plugin.name in badPlugins:
        continue
    
    if plugin.hardcoded:
        pluginString += f" {colored('[HARDCODED]', 'yellow')}"
    
    check = utils.compareVersion(plugin.version, plugin.latest)

    if check:
        outdated.append(pluginString)
        continue

    upToDate.append(pluginString)

# Get lengths of arrays for display selection and general info.
lenUpToDate = len(upToDate)
lenOutdated = len(outdated)
lenDeprecated = len(deprecated)
lenIgnored = len(ignored)
lenIncorrect = len(incorrect)

# Print up-to-date plugins if applicable.
display.upToDate(upToDate, lenUpToDate)

# Print out-of-date plugins if applicable.
 
# Print deprecated plugins if applicable.
display.deprecated(deprecated, lenDeprecated)
 
# Print incorrectly installed plugins if applicable.
display.incorrect(incorrect, lenIncorrect)
 
# Print ignored plugins if applicable.
display.ignored(ignored, lenIgnored)