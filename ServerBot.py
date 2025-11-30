import subprocess
import os

ver = "3.0"
mainver = "1.9.3"
displayname='A.C.L.'
extendedErrMess = False

def os_selector():
    print(f"====ServerBot v{ver} Recovery Menu====")
    print("""Select Method: 
1 - Linux
2 - Windows
3 - Setup.sh
4 - Exit
""")
    sel = int(input('>>> '))
    if sel == 1:
        subprocess.run(['bash', 'Files/setup/setuplib.sh'])
    elif sel == 2:
        subprocess.run(['setup.bat'], shell=True)
    elif sel == 3:
        subprocess.run(['bash', 'setup.sh'])
    elif sel == 4:
        exit()
    else:
        print('Failed to run Script. Aborting Install...')
        exit()



try:
    import discord
    from discord.ext import commands
    from discord import *
    import datetime
    import psutil
    import asyncio
    import random
    import shutil
    import pyfiglet
    import platform
    from dotenv import load_dotenv
except Exception as exc:
    print(f"Error in importing Library's. Trying to install it and update pip3\nException: {exc}\n")
    os_selector()



#Baner
banner = pyfiglet.figlet_format("A . C . L .")
bluescreenface = pyfiglet.figlet_format(": (")
print(banner)
print('Advanced Channel Listener')


#Intents
intents = discord.Intents.default()
intents.message_content = True
status = [' ', f'{platform.system()} {platform.release()}', displayname]
choice = random.choice(status)
client = commands.Bot(command_prefix='.', intents=intents, activity=discord.Game(name=choice))
testbot_cpu_type = platform.processor() or 'Unknown'
accept_value = ['True', 'true', 'Enabled', 'enabled', '1', 'yes', 'Yes', 'YES', True]



try:
    load_dotenv()
    ############# token/intents/etc ################
    admin_usr = os.getenv('admin_usr')
    mod_usr = os.getenv('mod_usr')
    ################################################
except:
    print("CAN'T LOAD .env FILE!\nCreate .env file using setup.sh")



#Log_File
logs = open('Logs.txt', 'w')
def createlogs():
    logs.write(f"""S E R V E R  B O T
LOGS
Time: {datetime.datetime.now()}
Info: Remember to shut down bot by .ShutDown command or log will be empty.
=============================================================================\n\n""")
    logs.close()
createlogs()

#LogMessage
def logMessage(info):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    logs = open(f'{maindir}/Logs.txt', 'a', encoding='utf-8')
    logs.write(f'[{time}] {info}\n')
    logs.close()
#PrintMessage
def printMessage(info):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f'[{time}] {info}')



#Directory
maindir = os.getcwd()
SBbytes = os.path.getsize('ServerBot.py')



#Information/Errors
fileerror = "Error: File not found or don't exist"
filelarge = "Error: File too large"
copiedlog = f"Information[ServerLog]: Copied Log to {maindir}/Files"
ffmpeg_error = "FFmpeg is not installed or File not found"
voice_not_connected_error = "You must be connected to VC first!"
leave_error = "How can I left, when I'm not in VC?"
thread_error = "Something Happened. Try to type:\n.thread {NameWithoutSpaces} {Reason}\nIf no reason, type: None"
not_allowed = "You're not allowed to use this command."
SBservice = "Run post installation commands to enable ServerBot.service to start with system startup:\nsudo chmod 775 -R /BotDirectory/*\nsudo systemctl enable ServerBot <== Enables automatic startup\nsudo systemctl start ServerBot <== Optional (turns on Service)\nsudo systemctl daemon-reload <== if you're running this command second time\nREMEBER about Reading/Executing permissions for others!"
service_err = "Something went wrong.\nHave you added the service entries to the .env file?"
badsite = "Something went wrong.\nHave you typed the correct address?\n..Or maybe the website just doesn't exist?"
random_err = 'Something went wrong. Have you typed correct min/max values?'
    #A.C.L
ACL_notfounderr = "User history not found."
ACL_historynotfound = "Default message history does not exist."
ACL_nopermission = "You don't have permission to use ACL mode. This incident will be reported."
ACL_rm_all_success = "Cleared all saved message history."
ACL_rm_all_fail = "Can't clear all message history."
ACL_rm_user_fail = "Can't clear message history of the selected user. Does it even exist?"



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


#MessageLogging
def userLog(usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
    if os.path.exists(f'{maindir}/ACL/{usr_id}/message.txt') == True:
        usrmessage = open(f'{maindir}/ACL/{usr_id}/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f'[{srv}({srv_id}) / {chnl}({chnl_id})] {usr}({usr_id}): {usrmsg}\n')
        usrmessage.close()
    else:
        print("[ACL] New user detected. Creating new entry...")
        os.makedirs(f'{maindir}/ACL/{usr_id}')
        usrmessage = open(f'{maindir}/ACL/{usr_id}/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f'[{srv}({srv_id}) / {chnl}({chnl_id})] {usr}({usr_id}): {usrmsg}\n')
        usrmessage.close()


def channelLog(usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
    print(f"[Message//{srv}/{chnl}] {usr}: {usrmsg}")
    if os.path.exists(f'{maindir}/ACL/default/message.txt') == True:
        usrmessage = open(f'{maindir}/ACL/default/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f"[Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
        usrmessage.close()
    else:
        print("[ACL] Default message history not detected. Creating new entry...")
        os.makedirs(f'{maindir}/ACL/default')
        usrmessage = open(f'{maindir}/ACL/default/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f"[Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
        usrmessage.close()



#ClientEvent
@client.event
async def on_ready():
    print(f'Logged as {client.user}')
    print(f'Welcome in A.C.L. v{ver}')
    print('Bot runtime: ', datetime.datetime.now())
    print('=' *40)


#Advanced Channel Listener
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
        #Chat
#1
@client.command(name='botbanner', help='Shows Bots Banner')
async def banner(ctx):
    await ctx.send(f'```{banner}```')

#2
@client.command(name='banner', help='Shows your text as Banner')
async def banner1(ctx, *, text):
    banner1 = pyfiglet.figlet_format(text)
    await ctx.send(f'```{banner1}```')

        #BotInfo
#1
@client.command(name='manual', help="Sends HTML manual\n'web' - see manual in browser\n'local' - download HTML manual from Discord")
async def manual(ctx, type):
    try:
        if type == 'web':
            await ctx.send("ServerBot user Manual [PL](https://Kamile320.github.io/ServerBot/manualPL.html) [EN](https://Kamile320.github.io/ServerBot/manualEN.html)")
        elif type == 'local':
            await ctx.send(file=discord.File(f'{maindir}/manualEN.html'))
        else:
            await ctx.send("Wrong type.\nChoose 'web' to read manual in browser or 'local' to download .html from Discord")
    except:
        await ctx.send(f"Something went wrong. Try again.")

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
@client.command(name='release', help='Shows last changes of Bot functions/Changelog')
async def newest_update(ctx):
    await ctx.send(f"""
[ACL v{ver}]
    Changelog:
- Updated ACL base to ServerBot v1.9.3

To see older releases, find 'updates.txt' in 'Files' directory.
""")



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
@client.command(name='bash', help='Runs Bash like scripts on hosting computer (Linux only)\nUses .sh extensions\nBest to work with .touch command')
async def bash(ctx, file):
    if str(ctx.message.author.id) in admin_usr:
        try:
            subprocess.run(['bash', file])
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
            
            os.makedirs(f'{maindir}/Files/setup')
            os.makedirs(f'{maindir}/Media')
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
            
            message = f"Information[mkshortcut]: Created desktop shortcut ({home_dir})"
            printMessage(message)
            logMessage(message)
        except:
            await ctx.send('Something went wrong, please try again.')
    else:
        await ctx.send(not_allowed)

#6
@client.command(name="mksysctlstart", help="Adds ServerBot to systemctl to start with system startup (Bot needs to be running as root)\nMode:\n'def' -> creates default autorun entry (python3)\n'venv' -> creates autorun entry that uses python virtual environment created by setup.sh (mkvenv.sh)\n.venv directory is located in the ServerBot main directory\nIt's recommended to save bot files into main (root) directory (/ServerBot) with 775 permissions (chmod 775 recursive). Without these permissions to bot files, systemctl startup will not work. Do not place bot in your home dir.")
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

                        message = f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        sys.close()
                        await ctx.send('Done!')
                        await ctx.send(SBservice)

                        message = f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except Exception as error:
                    await ctx.send(f'Got 1 error (or more) while creating systemctl entry.\nPossible cause: {error}')
            elif mode == 'venv':
                try:
                    await ctx.send('Making autorun.sh file..')
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f'#!/bin/bash\ncd {maindir}\n.venv/bin/python3 ServerBot.py')
                        auto.close()
                        await ctx.send('Done.')

                        message = f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)
                    
                        message = f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except Exception as error:
                    await ctx.send(f'Got 1 error (or more) while creating systemctl entry.\nPossible cause: {error}')
        except:
            await ctx.send(f"""```{bluescreenface}``` Unexpected problem ocurred""")
    else:
        await ctx.send(not_allowed)



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
DisplayName: **{displayname}**
CPU Usage: **{psutil.cpu_percent()}** (%)
CPU Count: **{psutil.cpu_count()}**
CPU Type: **{testbot_cpu_type}**
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
        
        message = f"Information[delete]: Deleted {len(deleted)} messages using '.delete' on channel: {ctx.channel.name}"
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(not_allowed)

#3
@client.command(name='cleaner', help='Cleans channel from last 100 messages')
async def cleaner(ctx):
    if str(ctx.message.author.id) in mod_usr:
        deleted = await ctx.channel.purge(limit=100)
        await ctx.channel.send(f'[Cleaner] deleted max amount of messages ({len(deleted)})')
        
        message = f"Information[cleaner]: Deleted {len(deleted)} messages using '.cleaner' on channel: {ctx.channel.name}"
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(not_allowed)

#4
@client.command(name='kick', help='Kicks Members')
async def kick(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in mod_usr:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked **{member}**')
        
        kicked = f'Information[Server/Members]: Kicked {member}. Reason: {reason}\n'
        printMessage(kicked)
        logMessage(kicked)
    else:
        await ctx.reply(not_allowed)

#5
@client.command(name='ban', help='Bans Members')
async def ban(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in mod_usr:
        await member.ban(reason=reason)
        await ctx.send(f'Banned **{member}**')
        
        banned = f'Information[Server/Members]: Banned {member}. Reason: {reason}\n'
        printMessage(banned)
        logMessage(banned)
    else:
        await ctx.reply(not_allowed)



        #FileManager/Directory - only for Admins (and Mods in the future)
#1
@client.command(name='cd', help="Changes directory\nYou can go back by .dir <return>")
async def chdir(ctx, *, directory):
    if str(ctx.message.author.id) in admin_usr:
        try:
            os.chdir(directory)
            await ctx.send(f"changed directory to {os.getcwd()}")
        except:
            await ctx.send("You can't go to this directory; make it or enter existing one")
    else:
        await ctx.send(not_allowed)

#2
@client.command(name='dir', help='Directory commands \n.dir <mode> \n   mode: \nreturn -> Goes back to main dir\ncheck -> checks dir that you are in\nlist -> list of files and directories in your dir\nlistall -> same but easier to read')
async def dir(ctx, *, mode):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'return':#
            os.chdir(maindir)
            await ctx.send(f'Returned to main directory ({maindir})')

        elif mode == 'check':#
            await ctx.send(f'You are here: {os.getcwd()}')

        elif mode == 'list':#
            listdir = os.listdir()
            await ctx.send(f'Files in **{os.getcwd()}**:\n{", ".join(listdir)}')

        elif mode == 'listall':#
            listdir = os.listdir()
            files_dir = '\n'.join(listdir)
            await ctx.send(f'Files in **{os.getcwd()}**:\n{files_dir}')
    else:
        await ctx.send(not_allowed)

#3      
@client.command(name='file', help='Commands for file/directory creating, deleting etc.\n.file <mode> <filename> \n    mode:\nopen -> opens file (REMEMBER to add extension (.py/.png/etc))\nmakedir -> creates directory (folder)\nchksize -> checks the size of selected file')
async def file(ctx, mode, *,filename):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'open':#open
            try:
                await ctx.send(file=discord.File(filename))
            except:
                await ctx.send(fileerror)
            
        elif mode == 'mkdir':#mkdir
            try:
                os.makedirs(filename)
                await ctx.send("Created new directory. Use '.dir list' to check this")
            except:
                await ctx.send("Can't create directory.")
                print()
            
        elif mode == 'size':#size
            try:
                size = os.path.getsize(filename)
                await ctx.send(f'Size of {filename} is {size} bytes')
            except:
                await ctx.send('Error')
            
        elif mode == 'create':#create
            try:
                mkfile = open(filename, 'wt')
                mkfile.close()
                await ctx.send("Created new empty file. Use '.dir list' to check this")
            except:
                await ctx.send("Can't create file.")
            
        else:#else
            await ctx.send('Incorrect mode/filename')
    else:
        await ctx.send(not_allowed)

#4
@client.command(name='touch', help='Creates files with selected extension and content.\nGo to selected directory and use .touch command')
async def makefile(ctx, name, *, content):
    if str(ctx.message.author.id) in admin_usr:
        try:
            directory = os.getcwd()
            mkfile = open(name, 'wt')
            mkfile.write(content)
            mkfile.close()

            await ctx.send(f'Created file {name}, in directory {directory}.')
            
            message = f'Information[FileManager]: Created file {name}, in directory {directory}.\nContent: {content}'
            printMessage(message)
            logMessage(message)
        except:
            await ctx.send(f'Something went wrong while creating file.')
    else:
        await ctx.send(not_allowed)
        #FileManager/Directory-END


        
        #AdvancedChannelListener
#1
@client.command(name='ACL', help='Manage A.C.L. users messages saved history\ngetusr - shows User history by User ID\nget history - history of all saved messages\nclear [all/user_id] - removes all saved messages or only messages of selected user')
async def ACL(ctx, mode, *, value):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'getusr':
            try:
                await ctx.send(file=discord.File(f'{maindir}/ACL/{value}/message.txt'))
            except:
                await ctx.send(ACL_notfounderr)
        elif mode == 'get' and value == 'history':
            try:
                await ctx.send(file=discord.File(f'{maindir}/ACL/default/message.txt'))
            except:
                await ctx.send(ACL_historynotfound)
        elif mode == 'clear':
            if value == 'all':
                try:
                    shutil.rmtree(f'{maindir}/ACL/')
                    await ctx.send(ACL_rm_all_success)
                    message = f"Information[ACL]: {ACL_rm_all_success} Command executed by: {ctx.author.id}\n"
                    print(message)
                    log = open(f'{maindir}/Logs.txt', 'a')
                    log.write(message)
                    log.close()
                except Exception as exc:
                    if extendedErrMess:
                        await ctx.send(f"{ACL_rm_all_fail} \nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_all_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to clear all message history but failed. \nException: \n{exc}\n"
                    print(message)
                    log = open(f'{maindir}/Logs.txt', 'a')
                    log.write(message)
                    log.close()
            else:
                try:
                    shutil.rmtree(f'{maindir}/ACL/{value}')
                    await ctx.send(f"Cleared message history of <@{value}>.")
                    log = open(f'{maindir}/Logs.txt', 'a')
                    log.write(f"Information[ACL]: User {ctx.message.author.id} cleared message history of {value}.\n")
                    log.close()
                except Exception as exc:
                    if extendedErrMess:
                        await ctx.send(f"{ACL_rm_user_fail} \nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_user_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to clear message history of {value} but failed. \nException: \n{exc}\n"
                    print(message)
                    log = open(f'{maindir}/Logs.txt', 'a')
                    log.write(message)
                    log.close()
        else:
            await ctx.send("Wrong mode. See '.help ACL' for more info")
    else:
        await ctx.send(ACL_nopermission)
        message = f"Information[ACL]: User {ctx.message.author.id} tried to use .ACL command without permission.\nSee {maindir}/ACL/{ctx.message.author.id} for more information.\n"
        print(message)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(message)
        logs.close()
        #AdvancedChannelListener-END



        #Test_Commands
#1
#@client.command(name='test', help='test', tts=True)
#async def test(ctx):
#    await ctx.send(f'test {ctx.author.mention}')

#2
#@client.command(name='ServerKiller', help="Don't use this")
#async def kill(ctx):
#    while True:
#        await ctx.send('@everyone')
#
        #Test_Commands-END



################################################ S L A S H   C O M M A N D S ###########################################################################################
#1
@client.tree.command(name='testbot', description='Tests some functions of Bot')
async def testbot(interaction):
    if str(interaction.user.id) in mod_usr:
        teraz = datetime.datetime.now()
        await interaction.response.send_message(f"""
    ***S e r v e r  B o t***  *test*:
    ====================================================
    Time: **{teraz.strftime('%d.%m.%Y, %H:%M:%S')}**
    Bot name: **{client.user}**
    ACL Version: **{ver}**
    Base version: **{mainver}**
    DisplayName: **{displayname}**
    CPU Usage: **{psutil.cpu_percent()}** (%)
    CPU Count: **{psutil.cpu_count()}**
    CPU Type: **{testbot_cpu_type}**
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
        await interaction.response.send_message(not_allowed)
################################################ S L A S H   C O M M A N D S  - E N D #######################################################################################

try:
    client.run(os.getenv('TOKEN'))
except Exception as err:
    print(f"Can't load Bot Token!\nEnter valid Token in '.env' file!\nPossible cause: {err}")