# AdvancedChannelListener

<a href="https://github.com/kamile320/AdvancedChannelListener/releases">![GitHub Release](https://img.shields.io/github/v/release/kamile320/AdvancedChannelListener)</a>
<a href="https://github.com/kamile320/AdvancedChannelListener/blob/main/LICENSE">![GitHub License](https://img.shields.io/github/license/kamile320/AdvancedChannelListener)</a>
<a href="">![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/kamile320/AdvancedChannelListener/total)</a>
<a href="https://github.com/kamile320/AdvancedChannelListener/commits/main/">![GitHub commits since latest release](https://img.shields.io/github/commits-since/kamile320/AdvancedChannelListener/latest)</a>

Discord Bot cog module that listens all available for the bot channels on Discord - you'll see every message sent on channels where the Bot is.<br><br>

A.C.L. saves every message sent on Discord server to files in directories named as ID of Discord User who just sent a message - with info about Server, Channel (and ID's of course).  
Bot also listens DM chats with him. Now you can know what is going on your Discord server and who's who. No more impersonating, hiding, etc.  
Everything works and creates automatically. Only thing you need to do is loading this module to supported Discord Bot that uses cogs - like [ServerBot](https://github.com/kamile320/serverbot).  
Basic functionality of admin privileges/security/etc that uses .env file works the same as in **ServerBot** - you can read about that in [ServerBot Manual](https://kamile320.github.io/ServerBot/manualEN.html).

**REMEBER** - Bot/Module saves every message sent on Discord Servers - this can break users privacy; you're using ACL at your own risk!  

I recommend you to put code below in your bot main file in your on_message async function - this will allow bot to use on_message functions from ACL module:
```
    for cog in client.cogs.values():
        if hasattr(cog, 'on_message_hook'):
            await cog.on_message_hook(message)
```


Table of known Discord Bots that supports ACL (v4.0+):  

| Discord Bot | Supported Since | Native / After modification above | Notes |
| - | - | - | - |
| [ServerBot](https://github.com/kamile320/serverbot) | v1.11.0+ | Native | Releases v1.8-v1.10.1 had ACL built-in main file (ACL v3.1 and older) |
