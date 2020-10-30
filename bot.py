# bot.py
#################################################################
import os
import sys
import discord
from PIL import Image
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
import asyncio
from dotenv import load_dotenv
load_dotenv()
#################################################################
global lecturetime, ls
GUILD = '760098399869206529'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
ls=elist()
c=False
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


def reactionno(list):
    for x in list:
        if x.emoji.id==764307177888284723:
            return x.count







#############################################################
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
            future6[count][1]="Space Cadets"
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
            future6[count][1]="To help with our RasPi coursework (doesn't exist yet so no URL)"
            future6[count].append("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        else:
            continue
    return future6
###################################################################






###################################################################
class DiscordBot():
    @bot.event
    async def on_ready():
        bot.add_cog(MyCog())
        print(bot.user)
#####################################################
    @bot.event
    async def on_message_delete(msgctx):
        if msgctx.author.bot == False:
            #print(msgctx.author.bot)
            #print(msgctx.author.id)
            await bot.get_channel(769348852591231027).send("```User "+msgctx.author.name+" deleted message:\n" + msgctx.content + "\n from channel: " + msgctx.channel.name + "\n at time: " + datetime.today().ctime()+"```")
##############################################


#
    # @cooldown(1,600)
    # @bot.event
    # async def on_typing(channel,user,when):
        # if user.id == 139113990537216000:
            # await channel.send("Warning, Avery am about to type!")



####################################################################
    @bot.event
    async def on_message_edit(before,after):
        if before.author.bot == False:
            await bot.get_channel(769348852591231027).send("```User "+before.author.name+" edited message in:\n"+before.channel.name +"\nFrom:\n" +before.content +"\nTo: \n" +after.content+"\n at time: "+datetime.today().ctime()+"```")

##############################################################
    @bot.command(name="jail",pass_context=True,brief="sends people to hell")
    async def jail(ctx,user: discord.Member):
        if ctx.author.guild_permissions.administrator==True:
            await user.add_roles(bot.get_guild(int(GUILD)).get_role(768969185467564033))
            await ctx.message.channel.send(user.name + " has been sent to Horny Jail™")
        else:
            print("Someone tried to jail")
    @bot.command(name="unjail",pass_context=True,brief="releases people from Hell")
    async def jail(ctx,user: discord.Member):
        if ctx.author.guild_permissions.administrator==True:
            await user.remove_roles(bot.get_guild(int(GUILD)).get_role(768969185467564033))
            await ctx.message.channel.send(user.name + " has been released from Horny Jail™")
        else:
            print("Someone tried to unjail")
###########################################################
    @cooldown(1,60)
    @bot.command(name="votejail",pass_context=True,brief="Communism in action")
    async def votejail(ctx,user: discord.Member):
        test01 = await ctx.message.channel.send("User: "+ctx.message.author.name+"\nHas tried to Jail:"+user.name+"\nRemaining Votes Needed:8\nTime Left:300s")
        await test01.add_reaction(bot.get_emoji(764307177888284723))
        id=test01.id
        count=300
        while count != -1:
            test01=await bot.get_channel(ctx.message.channel.id).fetch_message(id)
            rno=int(reactionno(test01.reactions))-1
            count -=1
            await asyncio.sleep(1)
            await test01.edit(content=("User: "+ctx.message.author.name+"\nHas tried to Jail:"+user.name+"\nRemaining Votes Needed:"+str(8-rno) +"\nTime Left:"+str(count)+"s"))
            print(rno)
            if rno>=8:
                await user.add_roles(bot.get_guild(int(GUILD)).get_role(768969185467564033))
                break
        if count ==0:
            return
        countdown=300
        while countdown != -1:
            await test01.edit(content=("User: "+ctx.message.author.name+"\nHas Successfully Jailed:"+user.name+"\nTime Left:"+str(countdown)+"s"))
            countdown -=1
            await asyncio.sleep(1)
            if countdown==0:
                await user.remove_roles(bot.get_guild(int(GUILD)).get_role(768969185467564033))
                return
######################################################
    @bot.command(name='emlist',brief="refreshes internal emojilist")
    async def emlist(ctx, *args):
        global ls
        ls=elist()
        print("emojilist reloaded")
######################################################
    @bot.command(name='cumlord',pass_context = True, brief="you can cum, i guess")
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
            await ctx.message.author.add_roles(bot.get_guild(int(GUILD)).get_role(765936114841288855))
            await ctx.message.channel.send(ctx.message.author.name + " has Coomed")
        c=False
#####################################################
    @cooldown(1,600)
    @bot.command(name='next5',pass_context = True,brief="prints the next 5 lectures and times at UTC")
    async def next5(ctx):
        for x in richifier(parse_ical()):
            await ctx.message.channel.send("Date: "+datetime.utcfromtimestamp(x[0]).strftime('%Y-%m-%d %H:%M:%S')+"\nLecture: "+str(x[2]))
#################################################

    @bot.command(name='flip',pass_context = True,brief="flips a coin (is definitely tails biased)")
    async def flip(ctx):
        if random.randint(0,1) == 1:
            await ctx.message.channel.send("Heads")
        else:
            await ctx.message.channel.send("Tails")
########################################################
    @bot.command(name='do',pass_context = True,brief="Kettle-BOT will do anything for your love")
    async def do(ctx, *, arg):
        await ctx.message.channel.send("Kettle-BOT did "+ (ctx.message.clean_content)[4::])
#######################################################################

    @bot.command(name='bonk',pass_context = True,brief="Bonks someone")
    async def bonk(ctx, user: discord.Member):
        await ctx.message.channel.send(user.name+" was Bonked!!")
#######################################################################

    @bot.command(name='pp',brief="let it know that it helped")
    async def help(ctx):
        await ctx.message.channel.send("Kettle-BOT Helped!")

##############################################################

    @bot.command(name="whistle",pass_context = True,brief="Whistles in your VC")
    async def whistle(ctx):
        channel = ctx.author.voice.channel
        if(channel!=None):
            vc = await channel.connect()
            vc.play(discord.FFmpegOpusAudio(executable="C:/DISC BOT/bin/ffmpeg.exe",source='Kettle.mp3'))
            ##player.start()
            while vc.is_playing():
                await asyncio.sleep(1) #sleeps while playing
            await vc.disconnect()
        else:
            await bot.say('User is not in a channel')
###################################################################
    @bot.command(name='evil', brief="an eval command why god")
    async def evil(ctx, *, arg):

        if ctx.message.channel.id == 762719747963748362:
            await ctx.message.delete()
            print("Doing:"+arg)
            await eval(arg)
        else:
            await ctx.message.delete()
            await ctx.send("Sounds like Mischief to me!")

###################################################################



###################################################################

#####################################################
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        elif random.randint(0,6900) == 42:
            print("Someone got Lucky")
            await message.channel.send("Kettle-BOT is always watching")
        await bot.process_commands(message)
#######################################################
    @bot.event
    async def on_raw_reaction_add(payload):

        for each in ls:
            if str(payload.message_id) == each[1]:  ##idk tbh
                if str(payload.emoji.id) == each[0] or payload.emoji.name == each[0]:
                    await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(int(each[2])))
                    print(payload.member.name + " " +each[3])
##########################################################
    @bot.event
    async def on_raw_reaction_remove(payload):
        guild=bot.guilds[0]

        for each in ls:
            if str(payload.message_id) == each[1]:
                if str(payload.emoji.id) == each[0] or str(payload.emoji.name)==each[0]:
                    await guild.get_member(payload.user_id).remove_roles(guild.get_role(int(each[2])))
                    print(guild.get_member(payload.user_id).name + " " + each[4])
#####################################################################################

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.timecheck.start()
        self.editmcstat.start()
#########################################################################################
    def cog_unload(self):
        self.timecheck.cancel()
##########################################################################################
    @tasks.loop(count=None)
    async def createmsg(self,futurenow):
        global lecturetime
        embedVar = discord.Embed(title=("Lecture: "+ futurenow[2] + "  in "+str(round(((time.time()-futurenow[0])/60)))+ "mins"), description=futurenow[1], color=0x16C500)
        embedVar.add_field(name="Dear, ", value="""<@&764601237986738197>""", inline=False)
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
        await bot.get_channel(764657412585816084).send(embed=embedVar)
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







####################################################################################
bot.run(os.environ.get("DISCORD_BOT_SECRET"), reconnect=True)
