from inspect import getmembers
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

if userOS == 'nt':
    os.system('cls')
else:
    os.system('clear')

# Tell user that the script has started.
print(formatting.title('SCRIPT STATUS:'), '\n')

# Import config.
with open("./config.json") as config:
    config = json.load(config)

# Import ids.
with open("./ids.json") as ids:
    ids = json.load(ids)

print(formatting.statusUpdate('found config files', True))

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
userPlugins = utils.findPlugins(logString)
if not userPlugins:
    print(formatting.statusUpdate('no plugins found\n', False))
    cprint(f"SCRIPT END: No plugins were found in that log! Manual review is suggested.", 'yellow', attrs=['bold'])
    exit(0)
else:
    print(formatting.statusUpdate(f'{len(userPlugins)} plugin(s) found', True))

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

# Notify the user that the plugins were sorted and assigned correctly.
print(formatting.statusUpdate(f'{len(userPlugins)} plugin(s) checked for issues\n', True))

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
    print(formatting.statusUpdate(f'checking plugin version for: {plugin.name}, Installed: {plugin.version} - Latest: {plugin.latest}', True))

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



for i in upToDate:
    print("up", i)
print()
for i in outdated:
    print("out", i)
print()
for i in deprecated:
    print("dep", i)
print()
for i in ignored:
    print("ign", i)
print()
for i in incorrect:
    print("inc", i)