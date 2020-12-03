# bot.py
#################################################################
import os
import sys
import discord
import io
import sched, time
from datetime import datetime
from discord.ext.commands import cooldown
from discord.ext import tasks, commands
import random as random
from icalparse import parse_ical
from emojilist import elist
from wakari import urlshort
from mcstats import mcstat
from levelparams import levelparams
import asyncio
from dotenv import load_dotenv
from tinydb import TinyDB, Query, where
import json
import re
import math
import typing
from tinydb.operations import delete, increment, decrement, set
load_dotenv()
#################################################################
global lecturetime, ls
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
global GUILD
guildID = 760098399869206529
ls=elist()
c=False
global clok
global nekomode
nekomode=False

#################################################################
urlfile=open("urlkey.csv", mode="r").read().split("\n")
urlkey=[]
for x in urlfile:
    urlkey.append(x.split(","))
del urlkey[-1]
#################################################################

future =[]
tmpvar=""
lecturetime=False

global future6
#################################################################

db = TinyDB('db.json')
person = Query()
##DATABASE
## first is user ID, then count, then horny count, then last message time(lmsg)
####################################################################

def reactionno(list):
    for x in list:
        if x.emoji.id==764307177888284723:
            return x.count
###############################################################

print(time.time())
scheduler = sched.scheduler(time.time, time.sleep)
##################################################################
def richifier(future6):  ## future 5 is [unix,online delivery,course desc, course code]
    global lecturetime
    for count,each in enumerate(future6):        #adding +[course info url] at [4]
        for x in urlkey:
            if x[0]==each[3]:
                future6[count].append(x[1])
        if each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Friday":    ##adds context to each lecture
            future6[count][1]="Space Cadets, optional"
            future6[count].append("https://teams.microsoft.com/l/channel/19%3aa96eb5721aef41099e19690b93c27ab7%40thread.tacv2/Space%2520Cadets%2520(Fri%252016-18)?groupId=143e2cc4-76a6-42e4-95d9-a25c1afd59f6&tenantId=4a5378f9-29f4-4d3e-be89-669d03ada9d8")                                                    ##ALSO adds the link to slot [5]
        elif each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
            future6[count][1]="FAQ Session"
            future6[count].append("https://waa.ai/u6DT")
        elif each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Thursday":
            future6[count][1]="Labs"
            future6[count].append("https://waa.ai/u6D3")
        elif each[3]=="COMP1215" and (datetime.fromtimestamp(each[0]).strftime("%A")=="Friday" or datetime.fromtimestamp(each[0]).strftime("%A")=="Monday"):
            future6[count][1]="Excerise sheet help/Discussion"
            future6[count].append("https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_190675_1&mode=view")
        elif each[3]=="COMP1205"and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
            future6[count][1]="Group Project with Sarah (meeting now on BB)"
            future6[count].append("https://waa.ai/uNPW")
        elif each[3]=="COMP1205":
            future6[count][1]="see homepage for info (NO LINK TO MEETING (SHOULD BE ON TEAMS))"
            future6[count].append("https://waa.ai/udrj")
        elif each[3]=="COMP1203" and datetime.fromtimestamp(each[0]).strftime("%A")=="Friday":
            future6[count][1]="Q&A session/summarise the week's lectures"
            future6[count].append("https://blackboard.soton.ac.uk/webapps/collab-ultra/tool/collabultra?course_id=_191256_1&mode=cpview")
        elif each[3]=="COMP1203" and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
            future6[count][1]="To help with our RasPi coursework (ON THE BLACKBOARD)(STARTS AT 10AM not 9AM)(DONT CLICK THE LINK)"
            future6[count].append("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        else:
            continue
    return future6
###################################################################


###################################################################
class DiscordBot():
    global clok
    @bot.event
    async def on_ready():
        bot.add_cog(MyCog())
        #bot.add_cog(JAILSTUFF(bot))
        await bot.change_presence(status=discord.Status.online)    ##TODO: REMOVE this when going back online ##################
        print(bot.user)

#####################################################
    @bot.event
    async def on_message(message):
        #print(clok)
        ##return  ##TODO: REMOVE this when going back online #####################################################################################
        if message.author == bot.user or message.channel.id == 769348852591231027:
            return
        elif random.randint(0,6900) == 42:
            print("Someone got Lucky")
            await message.channel.send("Kettle-BOT is always watching")

        if (db.contains(person.id==str(message.author.id))):
            if (db.get(person.id==str(message.author.id)).get('lmsg')-round(time.time())<= -3):
                ##print("yay")
                db.update(increment('msgcount'), person.id==str(message.author.id))
                db.update(set('lmsg',round(time.time())),person.id==str(message.author.id))

        elif not (db.contains(person.id==str(message.author.id))):
            db.insert({'id': str(message.author.id), 'msgcount': 0, 'hornycount':0, 'lmsg':0})
            ##print("nay")
        if  "||" not in message.clean_content:
            await bot.process_commands(message)

        global nekomode
        if nekomode == True:
            await message.delete()
            print("NEKOMODE IS ON")
            buh=re.sub("n([aeiou])","ny\\1",re.sub("[lr]","w",re.sub("v","ff",message.clean_content,flags=re.IGNORECASE),flags=re.IGNORECASE),flags=re.IGNORECASE)
            embed1=discord.Embed(description=buh, color=0xff00aa)
            embed1.set_author(name=message.author.display_name,icon_url=message.author.avatar_url)
            ##embed1.timestamp(str((message.created_at).strftime('%Y-%m-%d %H:%M:%S')))
            await message.channel.send(embed=embed1)

####################################################################

    @bot.event
    async def on_member_remove(member):
        await bot.get_channel(769348852591231027).send("```User "+member.name+"/"+member.display_name +" Left at time: "+datetime.today().ctime()+"```")

    @bot.event
    async def on_member_join(member):
        await bot.get_channel(769348852591231027).send("```User "+member.name+" Joined at time: "+datetime.today().ctime()+"```")

#####################################################
    @bot.event
    async def on_message_delete(msgctx):
        if msgctx.author.bot == False:
            flist=[]
            for x in msgctx.attachments:
                flist.append(await x.to_file())
            await bot.get_channel(769348852591231027).send("```User "+msgctx.author.name+" deleted message:\n" + msgctx.content + "\n from channel: " + msgctx.channel.name + "\n at time: " + datetime.today().ctime()+"```\nIncluding Files:", files=flist)
####################################################################
    @bot.event
    async def on_message_edit(before,after):
        if before.author.bot == False:
            flist=[]
            for x in before.attachments:
                flist.append(await x.to_file())
            await bot.get_channel(769348852591231027).send("```User "+before.author.name+" edited message in:\n"+before.channel.name +"\nFrom:\n" +before.content +"\nTo: \n" +after.content+"\n at time: "+datetime.today().ctime()+"```\nIncluding Files:", files=flist)

##############################################################
    @bot.command(name="jail",pass_context=True,brief="(ADMIN) sends people to hell")
    async def jail(ctx,user: discord.Member):
        if ctx.author.guild_permissions.administrator==True:
            await user.add_roles(bot.get_guild(guildID).get_role(768969185467564033))
            await ctx.message.channel.send(user.name + " has been sent to Horny Jail™")
        else:
            print("Someone tried to jail")
    @bot.command(name="unjail",pass_context=True,brief="(ADMIN) releases people from Hell")
    async def jail(ctx,user: discord.Member):
        if ctx.author.guild_permissions.administrator==True:
            await user.remove_roles(bot.get_guild(guildID).get_role(768969185467564033))
            await ctx.message.channel.send(user.name + " has been released from Horny Jail™")
        else:
            print("Someone tried to unjail")
###############################################################################################################################################################################
    ##@cooldown(1,120)
    ##@bot.command(name="votejail",pass_context=True,brief="Communism in Action")
    async def votejail(ctx,user: discord.Member):   #TODO: make it work again
        test01 = await ctx.message.channel.send("User: "+ctx.message.author.name+"\nHas tried to Jail:"+user.name+"\nRemaining Votes Needed:8\nTime Left:300s")
        await test01.add_reaction(bot.get_emoji(764307177888284723))
        await asyncio.sleep(1)
        await JAILSTUFF.vjail.start(ctx,user)
#################################################################################################################################################################################
    @bot.command(name='emlist',brief="Admin only")
    async def emlist(ctx, *args):
        global ls
        ls=elist()
        print("emojilist reloaded")
######################################################
    @bot.command(name='cumlord',pass_context = True, brief="A fan request, don't ask",aliases=['coom'])
    async def cumlord(ctx):
        print("A coomer tried to Coom")
        c=False
        for x in ctx.message.author.roles:
            if x.id == 765936114841288855:
                c=True
                break
            else:
                pass
        if c==False:
            print("They Succeeded")
            await ctx.message.author.add_roles(bot.get_guild(guildID).get_role(765936114841288855))
            await ctx.message.channel.send(ctx.message.author.name + " has Coomed")
        else:
            await ctx.send("Sorry Coomer, you're spent!")
        c=False
#####################################################
    @cooldown(1,30)
    @bot.command(name='next',pass_context = True,brief="prints the next lectures and times (up to 5)")
    async def next(ctx, *args):
        if not args:
            no=0
        elif args[0].isdigit() != True:
            return
        else:
            no=int(args[0])-1
            if no >=5:
                no = 4
            elif no<0:
                no = 0
        string10=""
        for count,x in enumerate(richifier(parse_ical())):
            if count > no:
                continue
            else:
                string10=(string10+("Date: "+datetime.utcfromtimestamp(x[0]).strftime('%H:%M %d-%m-%Y')+"\nLecture: "+str(x[2]))+"\n")
        await ctx.message.channel.send(string10)
    @next.error
    async def next_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

#################################################

    @bot.command(name='flip',pass_context = True,brief="flips a coin (is definitely tails biased)")
    async def flip(ctx):
        if random.randint(0,99) < 48 :
            await ctx.message.channel.send("Heads")
        else:
            await ctx.message.channel.send("Tails")
########################################################
    @bot.command(name='do',pass_context = True,brief="Kettle-BOT will do anything for your love")
    async def do(ctx, *, arg):
        await ctx.message.channel.send("Kettle-BOT did "+ (ctx.message.clean_content)[4::])
#######################################################################

    @bot.command(name='bonk',pass_context = True,brief="Bonks someone(a mention)")
    async def bonk(ctx, user: discord.Member):
        await ctx.message.channel.send(user.display_name.replace("@","")+" was Bonked!!")
#######################################################################

    @bot.command(name='pp',brief="let it know that it helped")
    async def help(ctx):
        await ctx.message.channel.send("Kettle-BOT Helped!")

##############################################################

    @bot.command(name="whistle",pass_context = True,brief="Whistles in your VC, really annoying")
    async def whistle(ctx):
        global vc
        channel = ctx.author.voice.channel
        if(channel!=None):
            vc = await channel.connect()
            vc.play(discord.FFmpegOpusAudio(source='Kettle.mp3',options='-filter:a "volume=0.1"'))
            ##player.start()
            while vc.is_playing():
                await asyncio.sleep(1) #sleeps while playing
            await vc.disconnect()
        else:
            await ctx.send('User is not in a channel')
###################################################################


    @bot.command(name="degen",pass_context = True,brief="Plays a J-pop radio station non-stop")
    async def degen(ctx):
        global vc
        vcchannel = ctx.author.voice.channel
        if(vcchannel!=None):
            vc = await vcchannel.connect(timeout = 10.0)
            vc.play(discord.FFmpegPCMAudio(source='https://listen.moe/stream',before_options="-stream_loop -1",options='-filter:a "volume=0.2"'))
            ##player.start()
            while vc.is_playing():
                await asyncio.sleep(5)
                #sleeps while playing
            await vc.disconnect()
        else:
            await ctx.send('User is not in a channel')
###################################################################

    @bot.command(name="leave",pass_context = True,brief="leaves")
    async def leave(ctx):
        global vc
        await vc.disconnect()


###################################################################

#######################################################
    @bot.event
    async def on_raw_reaction_add(payload):
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if str(payload.emoji.id) == '764307177888284723':
            if (db.contains(person.id==str(msg.author.id))):
                        ##print("yay")
                    db.update(increment('hornycount'), person.id==str(msg.author.id))
            elif not (db.contains(person.id==str(msg.author.id))):
                db.insert({'id': str(msg.author.id), 'msgcount': 0, 'hornycount':0, 'lmsg':0})
        global ls
        for each in ls:
            if str(payload.message_id) == each[1]:  ##idk tbh
                if str(payload.emoji.id) == each[0] or payload.emoji.name == each[0]:
                    await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(int(each[2])))
                    print(payload.member.name + " " +each[3])
##########################################################
    @bot.event
    async def on_raw_reaction_remove(payload):
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        global ls
        for each in ls:
            if str(payload.message_id) == each[1]:
                if str(payload.emoji.id) == each[0] or str(payload.emoji.name)==each[0]:
                    await bot.get_guild(guildID).get_member(payload.user_id).remove_roles(bot.get_guild(guildID).get_role(int(each[2])))
                    print(bot.get_guild(guildID).get_member(payload.user_id).name + " " + each[4])


        if payload.user_id==msg.author.id:  ##if it's your message, don't add to leaderboard
            return


        if str(payload.emoji.id) == '764307177888284723':
            if (db.contains(person.id==str(msg.author.id))):
                        ##print("yay")
                    db.update(decrement('hornycount'), person.id==str(msg.author.id))
            elif not (db.contains(person.id==str(msg.author.id))):
                db.insert({'id': str(msg.author.id), 'msgcount': 0, 'hornycount':0, 'lmsg':0})

#####################################################################################
    @cooldown(1,120)
    @bot.command(name='leaderboard', brief = 'prints top 10 leaderbaords', aliases=['lboard'])
    async def leaderboard(ctx, *args):
        msg="```"
        lst1=[]
        ##print(db.all())
        print("leaderboard")
        list=db.all()
        slist = sorted(list,key=lambda x:x.get('msgcount'),reverse=True)
        for count,x in enumerate(slist):
            if x['id']=='267571848760393728':
                continue
            if count == 11:
                break
            nick = str(bot.get_guild(guildID).get_member(int(x['id'])).display_name.replace("@","").replace("`","'"))
            ##dlam=int((len(nick)/2))
            #if count == 10:
            #    dlam-=1
            #str(x['msgcount'])
            msg = str(msg) + str(("\n"+str(count)+". "+nick))
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
    @cooldown(1,120)
    @bot.command(name='hornyboard', brief = 'prints top 10 hornies', aliases=['hboard'])
    async def hornyboard(ctx, *args):
        msg="```"
        lst1=[]
        ##print(db.all())
        print("hornyboard")
        list=db.all()
        slist = sorted(list,key=lambda x:x.get('hornycount'),reverse=True)
        count101=0
        for x in slist:
            if x['id']=='267571848760393728' or x['id']=='762764960845004851':
                continue
            if count101 == 10:
                break
            count101+=1
            nick = str(bot.get_guild(guildID).get_member(int(x['id'])).display_name.replace("@","").replace("`","'"))
            ##dlam=int((len(nick)/2))
            #if count == 10:
            #    dlam-=1
            #str(x['msgcount'])
            msg = str(msg) + str(("\n"+str(count101)+". "+nick))
        msg = msg + "```"
        await ctx.message.channel.send(msg)



    @hornyboard.error
    async def hornyboard_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error
#######################################################################################################################################################
    @bot.command(name='nekomode', brief = 'unleashes neko hell on earth', aliases=['bidenmode'])
    async def nekomode(ctx, *args):
        if ctx.message.author.guild_permissions.administrator==True:
            global nekomode
            nekomode = not nekomode
            print("nekomode HAS BEEN TOGGLED")

#####################################################################################
    @bot.command(name = 'shuffle', brief = 'shuffles text on spaces')
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
    @bot.command(name='id', brief = 'id get')
    async def id(ctx, *, arg):
        await ctx.message.channel.send(bot.get_guild(guildID).get_member(int(arg)).display_name)
######################################################################################
    @bot.command(name='depression',pass_context=True, brief = 'tells you percentage of messages compared to server total', aliases=['sad'], usage = "Input a mention, an ID or 'self'")
    async def depression(ctx, user: typing.Optional[discord.Member] = None, *args):
        try:
            if args[0] == "self":
                user = ctx.message.author
            elif user == None:
                try:
                    user = bot.get_guild(guildID).get_member(int(args))
                except (ValueError, TypeError):
                    await ctx.message.channel.send("Not an ID, please try again")
                    return
        except:
            pass

        count=0
        me=0
        for x in db.all():
            if int(x['id']) == user.id:
                me = int(x['msgcount'])
            count+= int(x['msgcount'])

        perc= round((me)/(count/100),2)
        await ctx.message.channel.send("Depression count: " + str(perc) + "%")


    #####################################################################################
    @bot.command(name='leadercompare',pass_context=True, brief = 'tells you percentage of messages compared to leader', aliases=['lcomp'], usage = "Input a mention, an ID or 'self'")
    async def depression(ctx, user: typing.Optional[discord.Member] = None, *args):
        try:
            if args[0] == "self":
                user = ctx.message.author
            elif user == None:
                try:
                    user = bot.get_guild(guildID).get_member(int(args))
                except (ValueError, TypeError):
                    await ctx.message.channel.send("Not an ID, please try again")
                    return
        except:
            pass

        count=0
        me=0
        for x in db.all():
            if int(x['id']) == user.id:
                me = int(x['msgcount'])
            if int(x['id']) == 267571848760393728:
                count = int(x['msgcount'])

        perc= round((me)/(count/100),2)
        await ctx.message.channel.send("Depression count: " + str(perc) + "%")

#####################################################################################
    @bot.command(name='level', brief = 'ADMIN, updates all user levels', aliases=['leveller'])
    async def level(ctx):

        if ctx.author.guild_permissions.administrator != True:
            return
        slist = sorted(db.all(),key=lambda x:x.get('msgcount'),reverse=True)
        for x in slist:
            if int(x['id'])==267571848760393728 or int(x['id'])==235088799074484224:
                continue
            if int(x['id']) < 100:
                break

            await asyncio.sleep(0.2)
            print("levelling: " + x['id'])
            ulevel=0
            member00=bot.get_guild(guildID).get_member(int(x['id']))
            memberlv=levelparams(int(x['msgcount']))
            currentlv=0
            ids = []
            if member00 is None:
                db.remove(person.id == x['id'])
                continue
            for each in member00.roles:
                ids.append(each.id)
            if 776845468126019594 in ids:
                currentlv=1
            elif 776856319261016074 in ids:
                currentlv=2
            elif 776856505269092403 in ids:
                currentlv=3
            elif 776856581551292448 in ids:
                currentlv=4
            elif 776856620981944331 in ids:
                currentlv=5
            else:
                currentlv=0
            if currentlv==memberlv:
                continue
            elif memberlv==0:
                continue
            elif memberlv == 1:
                await member00.add_roles(bot.get_guild(guildID).get_role(776845468126019594))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name+"  levelled up from " +str(currentlv) + " to "+str(memberlv))
            elif memberlv == 2:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776845468126019594))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856319261016074))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name+"  levelled up from " +str(currentlv) + " to "+str(memberlv))
            elif memberlv == 3:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776856319261016074))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856505269092403))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name+"  levelled up from " +str(currentlv) + " to "+str(memberlv))
            elif memberlv == 4:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776856505269092403))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856581551292448))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name+"  levelled up from " +str(currentlv) + " to "+str(memberlv))
            elif memberlv == 5:
                await member00.remove_roles(bot.get_guild(guildID).get_role(776856581551292448))
                await member00.add_roles(bot.get_guild(guildID).get_role(776856620981944331))
                print(bot.get_guild(guildID).get_member(int(x['id'])).display_name+"  levelled up from " +str(currentlv) + " to "+str(memberlv))
            else:
                print("Go cry to mommy")
#####################################################################################
#####################################################################################

class MyCog(commands.Cog):
    def __init__(self):
        global clok
        self.index = 0
        self.timecheck.start()
        self.editmcstat.start()
        self.clock.start()
#########################################################################################
    def cog_unload(self):
        self.timecheck.cancel()
        self.editmcstat.cancel()
        self.clock.cancel()
##########################################################################################
    @tasks.loop(count=None)
    async def createmsg(self,futurenow):
        global lecturetime
        embedVar = discord.Embed(title=("Lecture: "+ futurenow[2] + "  in "+str(round(((time.time()-futurenow[0])/60)))+ "mins"), description=futurenow[1], color=0x16C500)
        embedVar.add_field(name="Course Homepage", value="[HERE]"+"("+("https://waa.ai/"+urlshort(str(futurenow[4])))+")", inline=False)
        embedVar.add_field(name="Online Lecture Location", value="[Click here to go to the Lecture (if available)]"+"("+("https://waa.ai/"+urlshort(str(futurenow[5])))+")", inline=False)
        if futurenow[3]=="COMP1202":
            embedVar.set_thumbnail(url="https://i.imgur.com/eRgMUFx.png")
            embedVar.add_field(name="For more info please go to", value="""<#764590654448861185>""", inline=False)
        elif futurenow[3]=="COMP1203":
            embedVar.set_thumbnail(url="https://i.imgur.com/TR6iwwz.png")
            embedVar.add_field(name="For more info please go to", value="""<#764590676049395723>""", inline=False)
        elif futurenow[3]=="COMP1205":
            embedVar.set_thumbnail(url="https://i.imgur.com/3l2tbv7.gif")
            embedVar.add_field(name="For more info please go to", value="""<#764590696128446484>""", inline=False)
        elif futurenow[3]=="COMP1215":
            embedVar.set_thumbnail(url="https://i.imgur.com/bFvcT3Y.png")
            embedVar.add_field(name="For more info please go to", value="""<#764590723545694248>""", inline=False)
        else:
            embedVar.set_thumbnail(url="https://i.imgur.com/8LQCEa7.png")
            embedVar.add_field(name="For more info please go to", value="""<#762719395763322960>""", inline=False)
        await bot.get_channel(764657412585816084).send(content="""Dear <@&764601237986738197>,""",embed=embedVar)
        await asyncio.sleep(600)
        lecturetime=False
        self.createmsg.stop()
#####################################################################################################

    @tasks.loop(seconds=60.0)
    async def timecheck(self):
        global lecturetime
        global future,future5,lecturetime,future6
        future=[]
        future=parse_ical()
        future=richifier(future)
        #print(future)
        if future[0][0]-int(time.time())<=600 and future[0][0]-int(time.time())>0 and lecturetime==False:
            lecturetime=True
            print("lecture")
            self.createmsg.start(future[0])
        else:
            pass
###############################################################################################

    @tasks.loop(seconds=10.0)
    async def editmcstat(self):
        mc=mcstat()
        ebvar = discord.Embed(title=("Minecraft server Stats"), description="Running: "+ mc[3], color=0x16C500)


        ebvar.add_field(name="Online?", value=mc[0], inline=False)
        ebvar.add_field(name="IP:", value=mc[2], inline=False)
        mplay =""
        if mc[1].get("list")== None:
            mplay="No Players_"
            ebvar.add_field(name="Players:", value="0 out of "+str(mc[1].get("max"))+ " online.", inline=False)
        else:
            for each in mc[1].get("list"):
                mplay+= str(each) + "\n"
            ebvar.add_field(name="Players:", value=str(mc[1].get("online"))+" out of "+str(mc[1].get("max"))+ " online.", inline=False)
        ebvar.add_field(name="List:", value=mplay[:-1], inline=False)
        ebvar.add_field(name="Last Updated", value = datetime.now().strftime("%H:%M:%S"), inline=False)
        msg=await bot.get_channel(760099567391342653).fetch_message(767124576542785556)
        await msg.edit(content = None, embed=ebvar)

    @tasks.loop(seconds=1.0)
    async def clock(self):
        global clok
        clok = int(round(time.time()))


class JAILSTUFF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=1.0, count=299)
    async def vjail(ctx,user):
        print(user)
        count=300
        test01 = await ctx.fetch_message(ctx.message.id)
        print(test01.reactions)
        rno=int(reactionno(test01.reactions))-1
        count -=1
        await test01.edit(content=("User: "+ctx.message.author.name+"\nHas tried to Jail:"+user.name+"\nRemaining Votes Needed:"+str(8-rno) +"\nTime Left:"+str(count)+"s"))
        print(rno)
        if rno>=5:
                await user.add_roles(bot.get_guild(guildID).get_role(768969185467564033))
                JAILSTUFF.vjail.stop()
    # @tasks.loop(seconds=1.0, count=299)
    # async def vunjail(self, ctx, user):



####################################################################################
bot.run(os.environ.get("DISCORD_BOT_SECRET"), reconnect=True)
