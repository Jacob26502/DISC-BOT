# bot.py
#################################################################
import asyncio
import os
import random as random
import re
import sched
import time
import typing
from datetime import datetime

import discord
from discord.ext import tasks, commands
from discord.ext.commands import cooldown
from dotenv import load_dotenv
from tinydb import TinyDB, Query
from tinydb.operations import increment, set

from emojilist import elist
from icalparse import parse_ical
from levelparams import levelparams, nextpercent, lvup
from mcstats import mcstat

load_dotenv()
#################################################################
global lecturetime, ls
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|', intents=intents)
global GUILD
guildID = 760098399869206529
ls = elist()
c = False
global clok
global nekomode
global nekohook
nekomode = ""
script_dir = os.path.dirname(__file__)
#################################################################
urlfile = open(os.path.join(script_dir,"urlkey.csv"), mode="r").read().split("\n")
urlkey = []
for x in urlfile:
    urlkey.append(x.split(","))
del urlkey[-1]
#################################################################

future = []
tmpvar = ""
global lecturetime
lecturetime = False

global future6
#################################################################
global db, person
db = TinyDB(os.path.join(script_dir,'db.json'))
person = Query()
global timers
timers = [[0,0000000]]

##DATABASE
## first is user ID, then count, then horny count, then last message time(lmsg)
####################################################################


######################################################################
def reactionno(list):
    for x in list:
        if x.emoji.id == 764307177888284723:
            return x.count


###############################################################

print(time.time())
scheduler = sched.scheduler(time.time, time.sleep)


##################################################################
def richifier(future6):  ## future 5 is [unix,online delivery,course desc, course code]
    global lecturetime
    for count, each in enumerate(future6):  # adding +[course info url] at [4]
        for x in urlkey:
            if x[0] == each[3]:
                future6[count].append(x[1])
        if each[3] == "COMP1201" and datetime.fromtimestamp(each[0]).strftime(
                "%A") == "Friday":  ##adds context to each lecture at [5]
            future6[count][1] = "Tutorial for worksheet"
            future6[count].append(str(
                "[On Blackboard](" + "https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_191254_1" + ")"))  ##ALSO adds the link to slot [5]
        elif each[3] == "COMP1201":
            future6[count][1] = "Normal Lecture"
            future6[count].append(
                "[On Blackboard](" + "https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_191254_1" + ")")
        elif each[3] == "COMP1204":
            future6[count][1] = "Normal Lecture"
            future6[count][2] = "COMP1204 - Data Management"
            future6[count].append(
                "[Hosted on Panopto, check here for link](" + "https://discord.com/channels/738368497738055743/803620960073678859" + ")")
        elif each[3] == "COMP1206":
            future6[count][1] = "Normal Lab"
            future6[count].append(
                "[Hosted on Panopto, check here for link](" + "https://ptb.discord.com/channels/738368497738055743/806252265026617359" + ")")
        elif each[3] == "COMP1216" and datetime.fromtimestamp(each[0]).strftime("%A") == "Monday":
            future6[count][1] = "Problem Class"
            future6[count].append(
                "[Normally on Teams](" + "https://teams.microsoft.com/l/channel/19%3a1fd7ea69486b493cae35cf70015dbaa4%40thread.tacv2/Problem%2520Classes?groupId=2b0f1a80-ac88-4cdd-9368-71d0b6566117&tenantId=4a5378f9-29f4-4d3e-be89-669d03ada9d8" + ")")
        elif each[3] == "COMP1216":
            future6[count][1] = "Normal Lecture"
            future6[count].append(
                "[On Blackboard](" + "https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_190676_1" + ")")
        else:
            future6[count][1] = "This is Brokey"
            future6[count].append("""[Don't Do It!](https://www.youtube.com/watch?v=dbn-QDttWqU)""")
            continue
    return future6


###################################################################


###################################################################
async def sololevel(param):
    await DiscordBot.sololevel(param)


class DiscordBot():
    global clok

    @bot.event
    async def on_ready():
        bot.add_cog(MyCog())
        await bot.change_presence(
            status=discord.Status.online)  ##TODO: REMOVE this when going back online ##################
        print(bot.user)

    ############################################################

    async def sololevel(id):
        msgno = (db.get(person.id == str(id)).get('msgcount'))
        if int(id) == 267571848760393728 or int(id) == 235088799074484224:
            return
        if int(msgno) < 100:
            return

        print("levelling: " + bot.get_guild(guildID).get_member(int(id)).display_name)
        member00 = bot.get_guild(guildID).get_member(int(id))
        memberlv = levelparams(int(msgno))
        currentlv = 0
        ids = []
        if member00 is None:
            db.remove(person.id == str(id))
            return
        for each in member00.roles:
            ids.append(each.id)
        if 776845468126019594 in ids:
            currentlv = 1
        elif 776856319261016074 in ids:
            currentlv = 2
        elif 776856505269092403 in ids:
            currentlv = 3
        elif 776856581551292448 in ids:
            currentlv = 4
        elif 776856620981944331 in ids:
            currentlv = 5
        else:
            currentlv = 0
        if currentlv == memberlv:
            return
        elif memberlv == 0:
            return
        elif memberlv == 1:
            await member00.add_roles(bot.get_guild(guildID).get_role(776845468126019594))
            print(bot.get_guild(guildID).get_member(int(id)).display_name + "  levelled up from " + str(
                currentlv) + " to " + str(memberlv))
        elif memberlv == 2:
            await member00.remove_roles(bot.get_guild(guildID).get_role(776845468126019594))
            await member00.add_roles(bot.get_guild(guildID).get_role(776856319261016074))
            print(bot.get_guild(guildID).get_member(int(id)).display_name + "  levelled up from " + str(
                currentlv) + " to " + str(memberlv))
        elif memberlv == 3:
            await member00.remove_roles(bot.get_guild(guildID).get_role(776856319261016074))
            await member00.add_roles(bot.get_guild(guildID).get_role(776856505269092403))
            print(bot.get_guild(guildID).get_member(int(id)).display_name + "  levelled up from " + str(
                    currentlv) + " to " + str(memberlv))
        elif memberlv == 4:
            await member00.remove_roles(bot.get_guild(guildID).get_role(776856505269092403))
            await member00.add_roles(bot.get_guild(guildID).get_role(776856581551292448))
            print(bot.get_guild(guildID).get_member(int(id)).display_name + "  levelled up from " + str(
                currentlv) + " to " + str(memberlv))
        elif memberlv == 5:
            await member00.remove_roles(bot.get_guild(guildID).get_role(776856581551292448))
            await member00.add_roles(bot.get_guild(guildID).get_role(776856620981944331))
            print(bot.get_guild(guildID).get_member(int(id)).display_name + "  levelled up from " + str(
                currentlv) + " to " + str(memberlv))
        else:
            print("Go cry to mommy")

    #####################################################
    @bot.event
    async def on_message(message):
        # print(clok)
        if message.author == bot.user or message.channel.id == 769348852591231027  or (message.webhook_id):  # or (not message.author.guild_permissions.administrator): ##TODO: UNDO AFTER CHANGES
            #print("ignored")
            return
        elif random.randint(0, 6900) == 42:
            print("Someone got Lucky")
            await message.channel.send("Kettle-BOT is always watching")

        if message.author.id == 267571848760393728 and ("==" in message.clean_content):
            await message.channel.send("True")
        if message.author.id == 267571848760393728 and ("!=" in message.clean_content):
            await message.channel.send("False")

        if (db.contains(person.id == str(message.author.id))):
            if (db.get(person.id == str(message.author.id)).get('lmsg') - round(time.time()) <= -5):
                db.update(increment('msgcount'), person.id == str(message.author.id))
                db.update(set('lmsg', round(time.time())), person.id == str(message.author.id))

        elif not (db.contains(person.id == str(message.author.id))):
            db.insert({'id': str(message.author.id), 'msgcount': 0, 'hornycount': 0, 'lmsg': 0})
        if "||" not in message.clean_content:
            await bot.process_commands(message)

        if lvup(int(db.get(person.id == str(message.author.id)).get('msgcount'))) == True:
            print("levelling")
            embed = discord.Embed(description=str(message.author.mention) + " " + "(" + str(
                message.author.display_name) + ") " + " has levelled up from " + str(
                int(levelparams(db.get(person.id == str(message.author.id)).get('msgcount'))) - 1) + " to " + str(
                levelparams(db.get(person.id == str(message.author.id)).get('msgcount'))), color=0xff00aa)

            embed.set_author(name=message.author.display_name)
            embed.set_thumbnail(url=str(message.author.avatar_url))
            await bot.get_channel(768156094715265124).send(embed=embed)
            await sololevel(int(message.author.id))





        global nekomode
        if nekomode == str(message.channel.id):
            await message.delete()
            print("NEKOMODE IS ON IN: "+ nekomode )
            buh = re.sub("n([aeiou])", "ny\\1",re.sub("[lr]", "w", re.sub("v", "ff", message.clean_content, flags=re.IGNORECASE),flags=re.IGNORECASE), flags=re.IGNORECASE)
            ##embed1.timestamp(str((message.created_at).strftime('%Y-%m-%d %H:%M:%S')))
            attatches=[]
            for x in message.attachments:
                await asyncio.sleep(2)
                attatches.append(await x.to_file(use_cached=True))

            global nekohook
            await nekohook.send(content=buh,username=message.author.display_name,avatar_url=message.author.avatar_url,files=attatches)

    ####################################################################

    @bot.event
    async def on_member_remove(member):
        await bot.get_channel(769348852591231027).send(
            "```User " + member.name + "/" + member.display_name + " Left at time: " + datetime.today().ctime() + "```")

    @bot.event
    async def on_member_join(member):
        await bot.get_channel(769348852591231027).send(
            "```User " + member.name + " Joined at time: " + datetime.today().ctime() + "```")

    #####################################################
    @bot.event
    async def on_message_delete(msgctx):
        if msgctx.author.bot == False:
            flist = []
            for x in msgctx.attachments:
                flist.append(await x.to_file())
            await bot.get_channel(769348852591231027).send(
                "```User " + msgctx.author.name + " deleted message:\n" + msgctx.content + "\n from channel: " + msgctx.channel.name + "\n at time: " + datetime.today().ctime() + "```\nIncluding Files:",
                files=flist)

    ####################################################################
    @bot.event
    async def on_message_edit(before, after):
        if before.author.bot == False:
            flist = []
            for x in before.attachments:
                flist.append(await x.to_file())
            await bot.get_channel(769348852591231027).send(
                "```User " + before.author.name + " edited message in:\n" + before.channel.name + "\nFrom:\n" + before.content + "\nTo: \n" + after.content + "\n at time: " + datetime.today().ctime() + "```\nIncluding Files:",
                files=flist)

    ##############################################################

    ###############################################################################################################################################################################

    #################################################################################################################################################################################
    @bot.command(name='emlist', brief="Admin only", hidden=True)
    async def emlist(ctx, *args):
        global ls
        ls = elist()
        print("emojilist reloaded")

    ######################################################

    #####################################################
    @cooldown(1, 30)
    @bot.command(name='next', pass_context=True, brief="prints the next lectures and times (up to 5)")
    async def next(ctx, *args):
        if not args:
            no = 0
        elif args[0].isdigit() != True:
            return
        else:
            no = int(args[0]) - 1
            if no >= 5:
                no = 4
            elif no < 0:
                no = 0
        string10 = ""
        for count, x in enumerate(richifier(parse_ical())):
            if count > no:
                continue
            else:
                string10 += (("Date: " + datetime.utcfromtimestamp(x[0]).strftime(
                    '%H:%M %d-%m-%Y') + "\nLecture: " + str(x[2])) + "\n\n")
        await ctx.message.channel.send(string10)

    @next.error
    async def next_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    #################################################

    @bot.command(name='flip', pass_context=True, brief="flips a coin (is definitely tails biased)")
    async def flip(ctx):
        if random.randint(0, 99) < 48:
            await ctx.message.channel.send("Heads")
        else:
            await ctx.message.channel.send("Tails")

    ########################################################
    @bot.command(name='do', pass_context=True, brief="Kettle-BOT will do anything for your love")
    async def do(ctx, *, arg):
        await ctx.message.channel.send("Kettle-BOT did " + (ctx.message.clean_content)[4::])

    #######################################################################

    @bot.command(name='bonk', pass_context=True, brief="Bonks someone(a mention)")
    async def bonk(ctx, user: discord.Member):
        await ctx.message.channel.send(user.display_name.replace("@", "") + " was Bonked!!")

    #######################################################################

    @bot.command(name='pp', brief="let it know that it helped", hidden=True)
    async def help(ctx):
        await ctx.message.channel.send("Kettle-BOT Helped!")

    ##############################################################

    @bot.command(name="whistle", pass_context=True, brief="Whistles in your VC, really annoying")
    async def whistle(ctx):
        global vc
        channel = ctx.author.voice.channel
        if (channel != None):
            vc = await channel.connect()
            vc.play(discord.FFmpegOpusAudio(source=os.path.join(script_dir,'Kettle.mp3'), options='-filter:a "volume=0.1"'))
            ##player.start()
            while vc.is_playing():
                await asyncio.sleep(1)  # sleeps while playing
            await vc.disconnect()
        else:
            await ctx.send('User is not in a channel')

    ###################################################################

    @bot.command(name="jpop", pass_context=True, brief="Plays a J-pop radio station non-stop")
    async def degen(ctx):
        global vc
        vcchannel = ctx.author.voice.channel
        if (vcchannel != None):
            vc = await vcchannel.connect(timeout=10.0)
            vc.play(discord.FFmpegPCMAudio(source='https://listen.moe/stream', before_options="-stream_loop -1",
                                           options='-filter:a "volume=0.2"'))
            ##player.start()
            while vc.is_playing():
                await asyncio.sleep(5)
                # sleeps while playing
            await vc.disconnect()
        else:
            await ctx.send('User is not in a channel')

    ###################################################################

    @bot.command(name="leave", pass_context=True, aliases=["dc"], brief="leaves")
    async def leave(ctx):
        global vc
        await vc.disconnect()

    ###################################################################

    #######################################################
    @bot.event
    async def on_raw_reaction_add(payload):
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        global ls
        for each in ls:
            if str(payload.message_id) == each[1]:  ##idk tbh
                if str(payload.emoji.id) == each[0] or payload.emoji.name == each[0]:
                    await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(int(each[2])))
                    print(payload.member.name + " " + each[3])

    ##########################################################
    @bot.event
    async def on_raw_reaction_remove(payload):
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        global ls
        for each in ls:
            if str(payload.message_id) == each[1]:
                if str(payload.emoji.id) == each[0] or str(payload.emoji.name) == each[0]:
                    await bot.get_guild(guildID).get_member(payload.user_id).remove_roles(
                        bot.get_guild(guildID).get_role(int(each[2])))
                    print(bot.get_guild(guildID).get_member(payload.user_id).name + " " + each[4])

        if payload.user_id == msg.author.id:  ##if it's your message, don't add to leaderboard
            return

    #####################################################################################
    @cooldown(1, 120)
    @bot.command(name='leaderboard', brief='prints top 10 leaderbaords', aliases=['lboard'])
    async def leaderboard(ctx, *args):
        msg = "```"
        lst1 = []
        print("leaderboard")
        list = db.all()
        slist = sorted(list, key=lambda x: x.get('msgcount'), reverse=True)
        for count, x in enumerate(slist):
            if x['id'] == '267571848760393728':
                continue
            if count == 21:
                break
            nick = str(bot.get_guild(guildID).get_member(int(x['id'])).display_name.replace("@", "").replace("`", "'"))
            ##dlam=int((len(nick)/2))
            # if count == 10:
            #    dlam-=1
            # str(x['msgcount'])
            msg = str(msg) + str(("\n" + str(count) + ". " + nick))
        msg = msg + "```"
        await ctx.message.channel.send(msg)

    @leaderboard.error
    async def leaderboard_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    ######################################################################################################################################################

    #######################################################################################################################################################
    @bot.command(name='nekomode', brief='unleashes neko hell on earth', aliases=['bidenmode'], hidden=True)
    async def nekomode(ctx, *args):
        print("HELP")
        if ctx.message.author.id == 267571848760393728:
            global nekomode
            if nekomode == "":
                nekomode = str(ctx.message.channel.id)
                global nekohook
                nekohook = await ctx.message.channel.create_webhook(name="Nekohook")
                await ctx.message.channel.edit(slowmode_delay=3)
                await asyncio.sleep(1)

            else:
                for x in await ctx.message.channel.webhooks():
                    if x.name== "Nekohook":
                        await x.delete()
                await ctx.message.channel.edit(slowmode_delay=0)
                nekomode=""

            print("nekomode HAS BEEN TOGGLED")

    #####################################################################################
    @bot.command(name='shuffle', brief='shuffles text on spaces')
    async def shuffle(ctx, *args):

        str01 = args
        str02 = random.sample(str01, len(str01))
        msg = ""
        for x in args:
            if "@" in list(x):
                await ctx.message.channel.send("thank <@!333335442747424799> & <@!112831555310772224> for this one")
                return
        for x in str02:
            msg = (msg + " " + x)
        await ctx.message.channel.send(msg)
    ########################################################################################

    @bot.command(name='timer', brief='Countdown Timer',usage='2h:1d:3m        would be 1 day 2 hours 3 minutes (can use s/m/h/d with a number separated by colons)')
    async def timer(ctx, *args):
        global timers
        inp = args[0].split(":")
        secs = 0

        for x in inp:
                    num=abs(x[0:-1])
            if x[-1] == "s":
                secs += int(num)
            elif x[-1] == "m":
                secs += (60 * num)
            elif x[-1] == "h":
                secs += (3600 * num)
            elif x[-1] == "d":
                secs += (86400 * num)
        print(secs)
        timers.append([int(time.time())+secs, ctx.message.author.id])
        ctx.message.channel.send("Timer Set!")



    @bot.command(name='timeReset', brief='''hidden, don't ask''', aliases=[''], hidden=True)
    async def timeReset(ctx, *args):
        if ctx.message.author.id == 267571848760393728:
            global timers
            timers = [[0,0000000]]




    ########################################################################################
    @bot.command(name='id', brief='id get')
    async def id(ctx, *, arg):
        await ctx.message.channel.send(
            bot.get_guild(guildID).get_member(int(arg)).display_name.replace("@", "Fuck you "))

    ######################################################################################
    @bot.command(name='server%', pass_context=True, brief='tells you percentage of messages compared to server total',
                 aliases=['sad'], usage='leave empty for self, Input, an ID or ''''self''''')
    async def depression(ctx, *args):
        user = None
        try:
            if not args:
                user = ctx.message.author
            elif args[0] == "self":
                user = ctx.message.author
            elif user == None:
                if args[0] == "762764960845004851":
                    await ctx.message.channel.send("*whistles faintly*")
                    return
                try:
                    user = bot.get_guild(guildID).get_member(int(args[0]))
                except (ValueError, TypeError):
                    await ctx.message.channel.send("Not an ID, please try again")
                    return
        except:
            pass


        count = 0
        me = 0
        for x in db.all():
            if int(x['id']) == user.id:
                me = int(x['msgcount'])
            count += int(x['msgcount'])

        perc = round((me) / (count / 100), 2)
        await ctx.message.channel.send("Depression count: " + str(perc) + "%")

    #####################################################################################
    @bot.command(name='leadercompare', pass_context=True, brief='tells you percentage of messages compared to leader',
                 aliases=['lcomp'], usage='leave empty for self, Input, an ID or ''''self''''')
    async def depression(ctx, *args):
        user = None
        try:
            if not args:
                user = ctx.message.author
            elif args[0] == "self":
                user = ctx.message.author
            elif user == None:
                if args[0] == "762764960845004851":
                    await ctx.message.channel.send("*whistles faintly*")
                    return
                try:
                    user = bot.get_guild(guildID).get_member(int(args[0]))
                except (ValueError, TypeError):
                    await ctx.message.channel.send("Not an ID, please try again")
                    return
        except:
            pass


        slist2 = sorted(db.all(), key=lambda x: x.get('msgcount'), reverse=True)
        s2 = slist2[0]
        count = 0
        me = 0
        for x in db.all():
            if int(x['id']) == user.id:
                me = int(x['msgcount'])
            if int(x['id']) == int(s2['id']):
                count = int(x['msgcount'])

        perc = round((me) / (count / 100), 2)
        await ctx.message.channel.send("Depression count: " + str(perc) + "%")

    #####################################################################################
    @bot.command(name='level', brief='ADMIN, updates all user levels', aliases=['leveller'], hidden=True)
    async def level(ctx):

        if ctx.author.guild_permissions.administrator != True:
            return
        slist = sorted(db.all(), key=lambda x: x.get('msgcount'), reverse=True)
        for x in slist:
            if int(x['id']) == 267571848760393728 or int(x['id']) == 235088799074484224:
                continue
            if int(x['id']) < 100:
                break

            # await asyncio.sleep(0.2)
            print("levelling: " + x['id'])
            member00 = bot.get_guild(guildID).get_member(int(x['id']))
            memberlv = levelparams(int(x['msgcount']))
            currentlv = 0
            ids = []
            if member00 is None:
                db.remove(person.id == x['id'])
                continue
            for each in member00.roles:
                ids.append(each.id)
            if 776845468126019594 in ids:
                currentlv = 1
            elif 776856319261016074 in ids:
                currentlv = 2
            elif 776856505269092403 in ids:
                currentlv = 3
            elif 776856581551292448 in ids:
                currentlv = 4
            elif 776856620981944331 in ids:
                currentlv = 5
            else:
                currentlv = 0
            if currentlv == memberlv:
                continue
            elif memberlv == 0:
                continue
            elif memberlv == 1:
                await member00.add_roles(bot.get_guild(guildID).get_role(776845468126019594))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name + "  levelled up from " + str(
                    currentlv) + " to " + str(memberlv))
            elif memberlv == 2:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776845468126019594))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856319261016074))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name + "  levelled up from " + str(
                    currentlv) + " to " + str(memberlv))
            elif memberlv == 3:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776856319261016074))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856505269092403))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name + "  levelled up from " + str(
                    currentlv) + " to " + str(memberlv))
            elif memberlv == 4:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776856505269092403))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856581551292448))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name + "  levelled up from " + str(
                    currentlv) + " to " + str(memberlv))
            elif memberlv == 5:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776856581551292448))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856620981944331))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name + "  levelled up from " + str(
                    currentlv) + " to " + str(memberlv))
            else:
                print("Go cry to mommy")

    @bot.command(name='progress', brief='leave empty for self, Input, an ID or ''''self''''', aliases=['prog'])
    async def progress(ctx, *args):
        user = None
        try:
            if not args:
                user = ctx.message.author
            elif args[0] == "self":
                user = ctx.message.author
            elif user == None:
                if args[0] == "762764960845004851":
                    await ctx.message.channel.send("*whistles faintly*")
                    return
                try:
                    user = bot.get_guild(guildID).get_member(int(args[0]))
                except (ValueError, TypeError):
                    await ctx.message.channel.send("Not an ID, please try again")
                    return
        except:
            pass




        percent = (round(nextpercent(db.get(person.id == str(user.id)).get('msgcount')) * 100, 1))
        next_lvl = levelparams(db.get(person.id == str(user.id)).get('msgcount'))
        level = next_lvl
        next_lvl += 1

        bar = "["
        for x in range(round(int(percent) / 5)):
            bar += str("▇")
        while len(bar) < 21:
            bar += str("—")
        bar += str("]")
        if next_lvl > 5:
            percent = 42.0
            next_lvl = "∞"
        embed1 = discord.Embed(description=str(percent) + """% towards level """ + str(next_lvl) + "!",
                               color=0xff00aa).add_field(name="Bar:", value=bar, inline=True)

        embed1.set_author(name=user.display_name)
        embed1.set_thumbnail(url=str(user.avatar_url))
        await ctx.channel.send(embed=embed1)





    @bot.command(name='test')
    async def test(ctx, *args):
        print(args)
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
#####################################################################################
#####################################################################################

class MyCog(commands.Cog):

    def __init__(self):
        global lecturetime
        lecturetime=False
        global clok
        self.index = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.clock.start()

    #########################################################################################
    def cog_unload(self):
        self.timecheck.cancel()
        self.clock.cancel()

    ##########################################################################################

    @tasks.loop(seconds=1.0)
    async def clock(self):
        global clok
        global timers
        clok = int(round(time.time()))
        global nekomode
        if self.count1 < 10:
            self.count1 += 1
        else:
            #await self.editmcstat()
            self.count1 = 0
        if self.count2 < 60:
            self.count2 += 1
        else:
            await self.timecheck()
            self.count2 = 0


        for x in timers:
            if clok == x[0]:
                user = bot.get_user(x[1])
                await user.send("Your timer is up!")

    ###################################################################################

    @tasks.loop(count=None)
    async def createmsg(self, futurenow):
        global lecturetime
        embedVar = discord.Embed(
            title=("Lecture: " + futurenow[2] + "  in " + str(round(((time.time() - futurenow[0]) / 60))) + "mins"),
            description=futurenow[1], color=0x16C500)
        x = str("[" + str(futurenow[3]) + "]" + "(" + str(futurenow[4]) + ")")
        embedVar.add_field(name="Course Notes Homepage", value=x, inline=False)
        y = futurenow[5]
        embedVar.add_field(name="Online Lecture Location", value=y, inline=False)
        if futurenow[3] == "COMP1201":
            embedVar.set_thumbnail(url="https://i.imgur.com/9xkxKdk.png")
        elif futurenow[3] == "COMP1204":
            embedVar.set_thumbnail(url="https://i.imgur.com/uALzttv.png")
        elif futurenow[3] == "COMP1206":
            embedVar.set_thumbnail(url="https://i.imgur.com/o5GP9aT.png")
        elif futurenow[3] == "COMP1216":
            embedVar.set_thumbnail(url="https://i.imgur.com/9JwDYfS.png")
        else:
            embedVar.set_thumbnail(url="https://i.imgur.com/8LQCEa7.png")
        await bot.get_channel(764657412585816084).send(content="""Dear <@&764601237986738197>, """, embed=embedVar)
        await asyncio.sleep(600)
        lecturetime=False
        self.createmsg.stop()

    #####################################################################################################

    async def timecheck(self):
        global future, future5, lecturetime, future6
        future = []
        future = parse_ical()
        future = richifier(future)

        if (future[0][0] - int(time.time()) <= 600) and future[0][0] - int(time.time()) > 0 and lecturetime == False:
            lecturetime = True
            print("lecture")
            self.createmsg.start(future[0])
        else:
            print(future[0][0] - int(time.time()))
            pass

    ###############################################################################################

    async def editmcstat(self):
        mc = mcstat()
        ebvar = discord.Embed(title=("Minecraft server Stats"), description="Running: " + mc[3], color=0x16C500)

        ebvar.add_field(name="Online?", value=mc[0], inline=False)
        ebvar.add_field(name="IP:", value=mc[2], inline=False)
        mplay = ""
        if mc[1].get("list") == None:
            mplay = "Empty);_"
            ebvar.add_field(name="Players:", value="0/" + str(mc[1].get("max")), inline=False)
        else:
            for each in mc[1].get("list"):
                mplay += str(each) + "\n"
            ebvar.add_field(name="Players:", value=str(mc[1].get("online")) + "/" + str(mc[1].get("max")), inline=False)
        ebvar.add_field(name="List:", value=mplay[:-1], inline=False)
        ebvar.add_field(name="Last Updated", value=datetime.now().strftime("%H:%M:%S"), inline=False)
        msg = await bot.get_channel(760099567391342653).fetch_message(767124576542785556)
        await msg.edit(content=None, embed=ebvar)


####################################################################################
bot.run(os.environ.get("DISCORD_BOT_SECRET"), reconnect=True)
