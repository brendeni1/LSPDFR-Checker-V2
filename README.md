# Welcome To v2!

This is the less scuffed, scuffed version of [LSPDFR Update Checker v1](https://github.com/DarkVypr/LSPDFR-Update-Checker)! I've mostly changed the structure of the code -- bare with me as i'm still learning lol.

# Setting It Up

This program is relatively easy to set up. I personally just use it inside of VS code. If you don't know what VSC is/how to use it, that is on you to figure out. Once you have it opened in VS code, you can use the terminal to install these: `pip install requests packaging termcolor`.

If you have any further questions, make an issue here, or dm me on my LSPDFR profile. I will be adding to this readme with any steps that I forgot to state on setting this program up.

# Updating This Script

As I add new things, and develop new features to this program, you should naturally update it. Ironically, this update checker doesn't have an update checker, so you may need to check here periodically. I will eventually impliment some sort of version checker for this script; For now, it's just Coming Soon™...

# Checking a Log

To use this, all you have to do is place a **RagePluginHook.log** file in the root folder where the .py script file is. It uses logs to detect plugins[, and this is because it is meant to be mainly used on other's games. (LSPDFR support and yada-yada...)

# Configuration

In **config.json**, there are a few arrays which will affect how the program checks.

<h4><ins>Main</ins></h4>

The **"main"** array is used to specify some of the essential versions. These have to be manually updated each time their respective program is updated.

<h4><ins>Blacklist</ins></h4>

The **"blacklist"** array is used to blacklist a plugin which is either weirdly displayed (ie: "APIExample" and such...), or improperly versioned. For some reason, many plugin devs forget to update their assembly versions which causes the script to think that the plugin is outdated, when in reality it might be fine.

***Here is an example:***

![CodeRedCallouts' Bad Assembly Version](https://i.darkvypr.com/badplugin1.jpg)
![CodeRedCallouts' Version](https://i.darkvypr.com/badplugin2.jpg)

If you come across a plugin that is weird, just blacklist it.

<h4><ins>Hardcoded</ins></h4>

The **"hardcoded"** array is used for plugins that aren't on LCPDFR.com, and are widely used. An example of this is all of Bejoijo's plugins. It can also be used with plugins that use build numbers, *Section136Callouts* as an example.

<h4><ins>Deprecated</ins></h4>

The **"deprecated"** array is used for plugins that cause issues, are outdated and no longer supported, or have better alternatives. You can specify the reason for deprecation by adding a string to the JSON. If you would like no text, just put *null*. The text will show up right next to the plugin, example:

![Removal Example](https://i.darkvypr.com/depr-v2.jpg)

<h4><ins>Flags</ins></h4>

The **"flags"** array is used to check the log for common issues. As you can see, in the JSON there are 2 properties. "r" is a shorthand for RegExp, and it's purpose is simple. Any expression that is put in this field will be tested against the user's log. If there is a match, this means that a common error was found, and the program will display this at runtime. Whatever is in the "desc" field will be displayed. Example:

![Flag Example](https://i.darkvypr.com/issues-v2.jpg)

I have also added a new field to the flags parameter. The **"smart"** tag is useful when you have a RegExp that could match a broad term of issues. For example, in some logs, there will be a *"file not found"* issue. This is a bit vauge, and this feature is present to help. If you put a **RegExp** in the **smart** field, te script will check each inital match for that RegExp. It's hard to explain, and pictures speak 1000 words:

![Smart Flag Example](https://i.darkvypr.com/smart-flags.jpg)

Hope you can understand it better with that... 🤒

<h4><ins>Incorrect Installs</ins></h4>

Finally the **"incorrect"** array is used to check the log for plugins that aren't in the right folders. Some people mistakenly put **RAGENativeUI** among others into the `plugins/LSPDFR` folder. As we know, this is incorrect.

The "name" key is used for the plugin/dll name. It will be the trigger. If a plugin is found with this string, the user will be notified. The "path" key is used for the correct path that the plugin/script should be installed in. This is useful because some plugins are handled by RAGE, not LSPDFR, hence the `plugins/LSPDFR` directory being incorrect. Example:


![Incorrect Example](https://i.darkvypr.com/incr-v2.jpg)

# Adding an ID

In the **ids.json** file, the numbers next to all of the plugins correspond to the LCPDFR.com ID. The ID can be found here:

![LSPDFR ID location](https://i.darkvypr.com/lspdfr-id.jpeg)

Adding an ID is pretty self explanitory, just make sure that the plugin name is the same as the .dll name.

# Hash Converting

There is an included **hashConvert.py** file which pulls all its hashes from **hashes.json**. It's pretty basic, but quicker than googling I guess. This is useful when you get this error, or you find a GTAV hash in a log.

![Hash Error Example](https://i.darkvypr.com/hash-example.jpg)

# RAGENativeUI Versions

This script will also attempt to find the version of RNUI installed. It kind of works?... It requires a plugin to send the version inside of the log however. Popular callouts like Section136 and etc do this so it works 60% of the time.

# Results

Here is one of the various outputs you will see when checking a log:

![Example Check](https://i.darkvypr.com/test-check-v2.jpg)

You can run your own test log by using this file. It will produce the same results as above:

https://files.darkvypr.com/RagePluginHook-TestFile.log

Just save it as a .log file.