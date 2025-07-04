import subprocess
import os

ver = "2.0"
mainver = "1.7"

def os_selector():
    print(f"====ServerBot v{ver} Recovery Menu====")
    print("""Select Method: 
1 - Linux
2 - Windows
3 - Setup.sh
4 - Exit
""")
    sel = int(input(">>> "))
    if sel == 1:
        subprocess.run(["bash", 'Files/setup/setuplib.sh'])
    elif sel == 2:
        subprocess.run(['setup.bat'], shell=True)
    elif sel == 3:
        subprocess.run(['bash', 'setup.sh'])
    elif sel == 4:
        exit()
    else:
        print('Failed to run Script. Aborting Install')


try:
    import discord
    from discord.ext import commands
    from discord import *
    import datetime
    import psutil
    import requests
    import asyncio
    import random
    import shutil
    import pyfiglet
    import platform
    from dotenv import load_dotenv
except Exception as exc:
    print(f"Error in importing Library's. Trying to install it and update pip3\nException: {exc}\n")
    os_selector()

#AdvancedChannelListener
def aclcheck():
    if os.path.exists(f'{maindir}/ACL') == True:
        print("ACL check OK")
    else:
        print("ACL not found.\nCreating...")
        try:
            os.makedirs(f'{maindir}/ACL')
        except:
            print('Cannot create ACL directory.')



def userLog(usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
    if os.path.exists(f'{maindir}/ACL/{usr_id}/message.txt') == True:
        usrmessage = open(f'{maindir}/ACL/{usr_id}/message.txt', 'a')
        usrmessage.write(f'[{srv}({srv_id}) / {chnl}({chnl_id})] {usr}({usr_id}): {usrmsg}\n')
        usrmessage.close()
    else:
        print("[ACL] New user detected. Creating new entry...")
        os.makedirs(f'{maindir}/ACL/{usr_id}')
        usrmessage = open(f'{maindir}/ACL/{usr_id}/message.txt', 'a')
        usrmessage.write(f'[{srv}({srv_id}) / {chnl}({chnl_id})] {usr}({usr_id}): {usrmsg}\n')
        usrmessage.close()



def channelLog(usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
    print(f"[Message//{srv}/{chnl}] {usr}: {usrmsg}")
    if os.path.exists(f'{maindir}/ACL/default/message.txt') == True:
        usrmessage = open(f'{maindir}/ACL/default/message.txt', 'a')
        usrmessage.write(f"[Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
        usrmessage.close()
    else:
        print("[ACL] Default message history not detected. Creating new entry...")
        os.makedirs(f'{maindir}/ACL/default')
        usrmessage = open(f'{maindir}/ACL/default/message.txt', 'a')
        usrmessage.write(f"[Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
        usrmessage.close()




#Baner
banner = pyfiglet.figlet_format("A . C . L .")
bluescreenface = pyfiglet.figlet_format(": (")
print(banner)
print('Advanced Channel Listener')

#Intents
intents = discord.Intents.default()
intents.message_content = True
status = [' ', f'{platform.system()} {platform.release()}']
choice = random.choice(status)
client = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name=choice))


try:
    load_dotenv()
    ####### token/intents/etc ##########
    admin_usr = os.getenv('admin_usr')
    mod_usr = os.getenv('mod_usr')
    ####################################
except:
    print("CAN'T LOAD .env FILE!\nCreate .env file using setup.sh")


#Log_File
logs = open('Logs.txt', 'w')
def createlogs():
    logs.write(f"""S E R V E R  B O T
LOGS
Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
Info: Remember to shut down bot by .ShutDown command or log will be empty.
=============================================================================\n\n""")
    logs.close()
createlogs()


#Directory
maindir = os.getcwd()
SBbytes = os.path.getsize('ServerBot.py')


#Information/Errors
fileerror = "Error: File not found or don't exist"
filelarge = "Error: File too large"
copiedlog = f"Information[ServerLog]: Copied Log to {maindir}/Files"
thread_error = "Something Happened. Try to type:\n.thread {NameWithoutSpaces} {Reason}\nIf no reason, type: None"
not_allowed = "You're not allowed to use this command."
SBservice = "Run post installation commands to enable ServerBot.service to start with system startup:\nsudo chmod 777 -R /BotDirectory/*\nsudo systemctl enable ServerBot <== Enables automatic startup\nsudo systemctl start ServerBot <== Optional (turns on Service)\nsudo systemctl daemon-reload <== if you're running this command second time\nREMEBER about Reading/Executing permissions for others!"
sctlerr = "Something went wrong.\n'sctl' directory with service entries exists?"
sctlmade = "Created 'sctl' directory for systemctl service entry."
badsite = "Something went wrong.\nHave you typed the correct address?\n..Or maybe the website just doesn't exist? "

ACLnotfounderr = "User history not found."
ACLhistorynotfound = "Default message history does not exist."
ACLnopermission = "You don't have permission to use ACL mode. This incident will be reported."

#ClientEvent
@client.event
async def on_ready():
    print(f'Logged as {client.user}')
    print(f'Welcome in A.C.L. v{ver}')
    aclcheck()
    print('Bot runtime: ', datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    print('=' *40)

#AdvancedChannelListener
@client.event
async def on_message(message):

    #Username
    username = str(message.author).split('#')[0]
    #UserMessage
    user_message = str(message.content)
    #Channel
    try:
        channel = str(message.channel.name)
    except AttributeError:
        channel = str(message.channel)
    #Server
    try:
        server = str(message.guild.name)
    except AttributeError:
        server = str(message.guild)
    #UserID
    userid = message.author.id
    #ChannelID
    channelid = message.channel.id
    #ServerID
    try:
        serverid = message.guild.id
    except AttributeError:
        serverid = "DM"


    channelLog(username, user_message, channel, server, userid, channelid, serverid)
    userLog(username, user_message, channel, server, userid, channelid, serverid)

    await client.process_commands(message)



        #Commands

    #Basic
#1
@client.command(name='botbanner', help='Shows Bots Banner')
async def banner(ctx):
    await ctx.send(f'```{banner}```')

#2
@client.command(name='banner', help='Shows your text as Banner')
async def banner1(ctx, *, text):
    banner1 = pyfiglet.figlet_format(text)
    await ctx.send(f'```{banner1}```')

#3
@client.command(name='badge')
async def badge(ctx, member: discord.Member):
    user_flags = member.public_flags.all()
    badges = [flag.name for flag in user_flags]
    await ctx.send(f'{member} has the following badges: {", ".join(badges)}')
    #Basic-END

        #BotInfo
#1
@client.command(name='manual', help="Sends HTML manual\n'web' - for showing manual in browser\n'local' to download HTML manual from Discord")
async def manual(ctx, type):
    try:
        if type == 'web':
            await ctx.send("ServerBot user Manual [PL](https://Kamile320.github.io/ServerBot/manual.html) [EN](https://Kamile320.github.io/ServerBot/manualEN.html)")
        elif type == 'local':
            await ctx.send(file=discord.File(f'{maindir}/manualEN.html'))
        else:
            await ctx.send("Wrong type.\nChoose 'web' for showing manual in browser\nor 'local' to download .html from Discord")
    except:
        await ctx.send(f"Can't open manualEN.html")

#2
@client.command(name='credits', help='Shows Credits')
async def credits(ctx):
    await ctx.send(f"""
***Advanced Channel Listener***
Version: {ver}
Based on: ServerBot v{mainver}
Created By: *Kamile320*.

Source: ```https://github.com/kamile320/AdvancedChannelListener```
Discord Server: [Here](https://discord.gg/UMtYGAx5ac)
""")

#3
@client.command(name='time', help='Shows local time')
async def time(ctx):
    now = datetime.datetime.now()
    await ctx.send(now.strftime('%d.%m.%Y, %H:%M:%S'))

#4
@client.command(name='ping', help='Pings the Bot')
async def ping(ctx):
    await ctx.send(f':tennis: Pong! ({round(client.latency * 1000)}ms)')
        
#5
@client.command(name='release', help='Shows last changes of Bot functions/Changelog')
async def newest_update(ctx):
    await ctx.send(f"""
[ACL v{ver}]
    Changelog:
- Bot saves every message to directories named as User ID who just send something
- New command: .ACL [getusr/get history]
- Updated printed date format in Logs.txt

To see older releases, find 'updates.txt' in folder 'Files'
""")
        #BotInfo-END



        #AdminOnly
#1
@client.command(name='ShutDown', help='Turns Off the Bot')
async def ShutDown(ctx):
    if str(ctx.message.author.id) in admin_usr:
        print("Information[ShutDown]: Started turning off the Bot")
        try:
            print("Information[ShutDown]: Saving Logs.txt...")
            src = open(f'{maindir}/Logs.txt', 'r')
            logs = open(f'{maindir}/Files/Logs.txt', 'a')
            append = f"\n\n{src.read()}"
            logs.write(append)
            logs.close()
            src.close()
            print("Logs.txt saved successfully.")
        except:
            print("Error occurred while saving log.")
        print("Information[ShutDown]: Shutting Down...")
        await ctx.send(f'ClosingBot.')
        await asyncio.sleep(1)
        await ctx.send(f'ClosingBot..')
        await asyncio.sleep(1)
        await ctx.send(f'ClosingBot...')
        await asyncio.sleep(1)
        exit()
    else:
        await ctx.reply(not_allowed)

#2
@client.command(name='copylog', help='Copies Bot Log file\nappend -> adds new value to older in Files/Logs.txt\nreplace -> clears old Files/Logs.txt and adds new content\nclearall -> clears all Logs')
async def copylog(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'append':
            try:
                src = open(f'{maindir}/Logs.txt', 'r')
                logs = open(f'{maindir}/Files/Logs.txt', 'a')
                append = f"\n\n{src.read()}"
                logs.write(append)
                logs.close()
                src.close()
                await ctx.send('Appending logs to Files/Logs.txt succeed.')
            except:
                await ctx.send(f"Error occurred while copying log.")
        elif mode == 'replace':
            try:
                src_path = fr"{maindir}/Logs.txt"
                dst_path = fr"{maindir}/Files/Logs.txt"
                shutil.copy(src_path, dst_path)
                print(copiedlog)
                await ctx.send(f'Successfully replaced Files/Logs.txt content.')
            except:
                await ctx.send("Error occurred while copying log. Maybe folder doesn't exist?")
        elif mode == 'clearall':
            try:
                l1 = open(f"{maindir}/Logs.txt", 'w')
                l1.write("")
                l1.close()
                l2 = open(f"{maindir}/Files/Logs.txt", 'w')
                l2.write("")
                l2.close()
                await ctx.send("Successfully cleared Logs.")
            except:
                await ctx.send("Can't clear logs.")
        else:
            await ctx.send("Wrong copylog mode.")        
    else:
        await ctx.reply(not_allowed)

#3
@client.command(name="bash", help="Runs Bash like scripts on hosting computer (Linux only)\nUses .sh extensions\nBest to work with .touch command")
async def bash(ctx, file):
    if str(ctx.message.author.id) in admin_usr:
        try:
            subprocess.run(["bash", file])
        except:
            await ctx.send(f'Failed to run Script')
    else:
        await ctx.reply(not_allowed)

#4
@client.command(name='rebuild', help='Rebuilds files and directories')
async def rebuild(ctx):
    if str(ctx.message.author.id) in admin_usr:
        await ctx.send('Trying to rebuild files...')
        try:
            os.chdir(maindir)
            logs1 = open('Logs.txt', 'w')
            logs1.close()

            os.makedirs(f'{maindir}/Files')
            os.chdir(f'{maindir}/Files')
            updates = open('updates.txt', 'w')
            updates.close()
            logs2 = open('Logs.txt', 'w')
            logs2.close()
            
            os.makedirs(f'{maindir}/setup')
            os.chdir(maindir)
            await ctx.send("Success.\nRebuilded Files with no content")
        except:
            await ctx.send("Can't rebuild files.")
    else:
        await ctx.reply(not_allowed)

#5
@client.command(name="mkshortcut", help="Creates a shortcut on your Desktop. (Linux (Ubuntu 22.04 based) only)\nType: .mkshortcut [Name of your Desktop Folder (Desktop/Pulpit etc.)]")
async def shrtct(ctx, desk):
    if str(ctx.message.author.id) in admin_usr:
        try:
            home_dir = os.path.expanduser('~')
            os.chdir(home_dir)
            os.chdir(desk)
            shrt = open('ServerBot.sh', 'w')
            shrt.write(f'cd {maindir}\npython3 ServerBot.py')
            shrt.close()
            os.chdir(maindir)
            await ctx.send('Done.')
            
            print(f"Information[mkshortcut]: Created desktop shortcut ({home_dir})")
            logs = open(f'{maindir}/Logs.txt', 'a')
            logs.write(f"Information[mkshortcut]: Created desktop shortcut ({home_dir})\n")
            logs.close()
        except:
            await ctx.send('Something went wrong, please try again.')
    else:
        await ctx.send(not_allowed)

#6
@client.command(name="mksysctlstart", help="Adds ServerBot to systemctl to start with system startup (Bot needs to be running as root)\nMode:\n'def' -> creates default autorun entry (python3)\n'venv' -> creates autorun entry that uses python virtual environment created by setup.sh (mkvenv.sh)\n.venv hides in ServerBot main directory\nIt's recommended to save bot files into main (root) directory (/ServerBot) with full permissions (chmod 777 recursive). Without full permissions to bot files, systemctl startup will not work.")
async def mksysctlstart(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if mode == 'def':
                try:
                    await ctx.send("Making autorun.sh file..")
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 ServerBot.py")
                        auto.close()
                        await ctx.send('Done.')

                        print(f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)

                        print(f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except:
                    await ctx.send('Got 1 error (or more) while creating systemctl entry.')
            elif mode == 'venv':
                try:
                    await ctx.send('Making autorun.sh file..')
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f'#!/bin/bash\ncd {maindir}\n.venv/bin/python3 ServerBot.py')
                        auto.close()
                        await ctx.send('Done.')

                        print(f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)
                    
                        print(f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except:
                    await ctx.send('Got 1 error (or more) while creating systemctl entry.')
        except:
            await ctx.send(f"""```{bluescreenface}``` Unexpected problem ocurred""")
    else:
        await ctx.send(not_allowed)

#7
@client.command(name='service', help="Lists active/inactive services. To add service entry, enter service name in .env file (service_list)\nUses systemctl\n\nlist -> lists entries in '.env' file\nstatus -> lists service entries and checks if they're active")
async def service(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if mode == 'list':
                try:
                    listdir_env = os.getenv('service_list')
                    listdir = [item.strip() for item in listdir_env.split(',')]
                    await ctx.send(f'**Service Entries:**')
                    for file in listdir:
                        await ctx.send(file)
                except:
                    await ctx.send(sctlerr)

            elif mode == 'status':
                try:
                    listdir_env = os.getenv('service_list')
                    listdir = [item.strip() for item in listdir_env.split(',')]
                    await ctx.send("**Service Activity:**")
                    for file in listdir:
                        await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl is-active {file}'])}```")
                except:
                    await ctx.send(sctlerr)

            elif mode == 'status-detailed':
                try:
                    listdir_env = os.getenv('service_list')
                    listdir = [item.strip() for item in listdir_env.split(',')]
                    await ctx.send("**Service Activity:**")
                    for file in listdir:
                        await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl status {file}'])}```")
                except:
                    await ctx.send(sctlerr)

            else:
                await ctx.send("Incorrect mode.")
        except:
            await ctx.send('Something went wrong.')
    else:
        await ctx.send(not_allowed)

#8
@client.command(name='pingip', help='Pings selected IPv4 address.')
async def pingip(ctx, ip):
    if str(ctx.message.author.id) in admin_usr:
        try:
            ipaddr = ip
            await ctx.send(f"```{subprocess.getoutput([f'ping {ipaddr} -c 1'])}```")
        except:
            await ctx.send('Something went wrong')
    else:
        await ctx.send(not_allowed)
        #AdminOnly-END



        #ACL
#1
@client.command(name='ACL', help='Manage A.C.L. users messages saved history\ngetusr - shows User history by User ID\nget history - history of all saved messages')
async def ACL(ctx, mode, *, value):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'getusr':
            try:
                await ctx.send(file=discord.File(f'{maindir}/ACL/{value}/message.txt'))
            except:
                await ctx.send(ACLnotfounderr)
        elif mode == 'get' and value == 'history':
            try:
                await ctx.send(file=discord.File(f'{maindir}/ACL/default/message.txt'))
            except:
                await ctx.send(ACLhistorynotfound)
        else:
            await ctx.send('Wrong mode.')
    else:
        await ctx.send(ACLnopermission)
        print(f"Information[ACL]: User {ctx.message.author.id} tried to use !ACL command without permission.\nSee {maindir}/ACL/{ctx.message.author.id} for more information.\n")
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f"Information[ACL]: User {ctx.message.author.id} tried to use !ACL command without permission.\nSee {maindir}/ACL/{ctx.message.author.id} for more information.\n")
        logs.close()
        #ACL-END


        #ModeratorOnly
#1
@client.command(name='testbot', help='Tests some functions of Host and Bot')
async def testbot(ctx):
    if str(ctx.message.author.id) in mod_usr:
        teraz = datetime.datetime.now()
        await ctx.send(f"""
***S e r v e r  B o t***  *test*:
====================================================
Time: **{teraz.strftime('%d.%m.%Y, %H:%M:%S')}**
Bot name: **{client.user}**
ACL Version: **{ver}**
Base version: **{mainver}**
CPU Usage: **{psutil.cpu_percent()}** (%)
CPU Count: **{psutil.cpu_count()}**
CPU Type: **{platform.processor()}ㅤ**
RAM Usage: **{psutil.virtual_memory().percent}** (%)
Ping: **{round(client.latency * 1000)}ms**
OS Test (Windows): **{psutil.WINDOWS}**
OS Test (MacOS): **{psutil.MACOS}**
OS Test (Linux): **{psutil.LINUX}**
OS Version: **{platform.version()}**
OS Kernel: **{platform.system()} {platform.release()}**
Bot Current Dir: **{os.getcwd()}**
Bot Main Dir: **{maindir}**
File size: **{os.path.getsize(f'{maindir}/ServerBot.py')}**
Floppy: **{os.path.exists('/dev/fd0')}**
====================================================""")
    else:
        await ctx.send(not_allowed)

#2
@client.command(name='delete', help='Deletes set amount of messages (eg. .delete 6 => will delete 6 messages)')
async def delete(ctx, amount: int = 0):
    if str(ctx.message.author.id) in mod_usr:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f'Deleted {len(deleted)} message(s)')
        print(f"Information[delete]: Deleted {len(deleted)} messages using '.delete' on channel: {ctx.channel.name}")
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f"Information[delete]: Deleted {len(deleted)} messages using '.delete' on channel: {ctx.channel.name}\n")
        logs.close()
    else:
        await ctx.reply(not_allowed)

#3
@client.command(name='cleaner', help='Cleans channel from last 100 messages')
async def cleaner(ctx):
    if str(ctx.message.author.id) in mod_usr:
        deleted = await ctx.channel.purge(limit=100)
        await ctx.channel.send(f'[Cleaner] deleted max amount of messages ({len(deleted)})')
        print(f"Information[cleaner]: Deleted {len(deleted)} messages using '.cleaner' on channel: {ctx.channel.name}")
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f"Information[cleaner]: Deleted {len(deleted)} messages using '.cleaner' on channel: {ctx.channel.name}\n")
        logs.close()
    else:
        await ctx.reply(not_allowed)

#4
@client.command(name="webreq", help="Sends website request codes and headers\n.webreq {get/getheader} {website}")
async def webreq(ctx, mode, *, web):
    if str(ctx.message.author.id) in mod_usr:
        try:
            if mode == 'get':
                try:
                    rq = requests.get(web)
                    await ctx.reply(f"Response: {rq.status_code}")
                except:
                    await ctx.reply(badsite)
            elif mode == 'getheader':
                try:
                    rq = requests.get(web)
                    await ctx.reply(f"Website Header:\n{rq.headers}")
                except:
                    await ctx.reply(badsite)
            else:
                await ctx.reply('')
        except:
            await ctx.reply("Wrong mode.")
    else:
        await ctx.reply(not_allowed)

#5
@client.command(name='kick', help='Kicks Members')
async def kick(ctx, member: discord.Member, *, reason=None):
    kicked = f'Information[Server/Members]: Kicked {member}. Reason: {reason}\n'
    if str(ctx.message.author.id) in mod_usr:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked **{member}**')
        print(kicked)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(kicked)
        logs.close()
    else:
        await ctx.reply(not_allowed)

#6
@client.command(name='ban', help='Bans Members')
async def ban(ctx, member: discord.Member, *, reason=None):
    banned = f'Information[Server/Members]: Banned {member}. Reason: {reason}\n'
    if str(ctx.message.author.id) in mod_usr:
        await member.ban(reason=reason)
        await ctx.send(f'Banned **{member}**')
        print(banned)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(banned)
        logs.close()
    else:
        await ctx.reply(not_allowed)

        #ModeratorOnly-END



        #FileManager/Directory
#1
@client.command(name='cd', help="Changes directory\nYou can go back by .dir <return>")
async def chdir(ctx, *, directory):
    try:
        os.chdir(directory)
        await ctx.send(f"changed directory to {os.getcwd()}")
    except:
        await ctx.send("You can't go to this directory; make it or enter existing one")

#2
@client.command(name='dir', help='Directory commands \n.dir <mode> \n   mode: \nreturn -> Goes back to main dir\ncheck -> checks dir that you are in\nlist -> list of files and directories in your dir\nlistall -> same but easier to read')
async def dir(ctx, *, mode):
    if mode == 'return':#
        os.chdir(maindir)
        await ctx.send(f'Returned to main directory ({maindir})')

    elif mode == 'check':#
        await ctx.send(f'You are here: {os.getcwd()}')

    elif mode == 'list':#
        listdir = os.listdir()
        await ctx.send(f'Files in this directory:\n{listdir}')

    elif mode == 'listall':#
        listdir = os.listdir()
        await ctx.send(f'Files in this directory:')
        for file in listdir:
            await ctx.send(file)

#3      
@client.command(name='file', help='Commands for file/directory creating, deleting etc.\n.file <mode> <filename> \n    mode:\nopen -> opens file (REMEMBER to add extension (.py/.png/etc))\nmakedir -> creates directory (folder)\nchksize -> checks the size of selected file')
async def file(ctx, mode, *,filename):
    if mode == 'open':#
        try:
            await ctx.send(file=discord.File(filename))
        except:
            await ctx.send(fileerror)
    elif mode == 'mkdir':#
        try:
            os.makedirs(filename)
            await ctx.send("Created new directory. Use '.dir list' to check this")
        except:
            await ctx.send("Can't create directory.")
    elif mode == 'size':#
        try:
            size = os.path.getsize(filename)
            await ctx.send(f'Size of {filename} is {size} bytes')
        except:
            await ctx.send('Error')
    elif mode == 'create':#
        try:
            mkfile = open(filename, 'wt')
            mkfile.close()
            await ctx.send("Created new empty file. Use '.dir list' to check this")
        except:
            await ctx.send("Can't create file.")
    else:
        await ctx.send('Incorrect mode/filename')

#4
@client.command(name='touch', help='Creates files with selected extension and content.\nGo to selected directory and use .touch command')
async def makefile(ctx, name, *, content):
    try:
        directory = os.getcwd()
        mkfile = open(name, 'wt')
        mkfile.write(content)
        mkfile.close()

        created = f'Created file {name}, in directory {directory}.\nContent: {content}'
        await ctx.send(f'Created file {name}, in directory {directory}.')
        print(created)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f'Information[FileManager]: {created}\n')
        logs.close()
    except:
        await ctx.send(f'Something went wrong while creating file.')
        #FileManager/Directory-END



        #Links_and_Servers
#1
@client.command(name='dscserv', help='Shows link to Discord Server')
async def dscserv(ctx):
    await ctx.send(os.getenv('dscserv_link'))

#3
@client.command(name='addbot', help='Shows Link to add Bot to other Servers\nstable -> sends link to stable version\ntesting -> sends link to testing version')
async def addbot(ctx, version):
    if version == "stable":
        await ctx.reply(os.getenv('addstable'))
    elif version == "testing":
        await ctx.reply(os.getenv('addtesting'))
    else:
        await ctx.send("Wrong value, try again.")

        #Links_and_Servers-END

try:
    client.run(os.getenv('TOKEN'))
except:
    print("Can't load Bot Token!\nEnter valid Token in '.env' file!")