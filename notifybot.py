# bot.py
import os
import discord
from PIL import Image
import io
from icalparse import parse_ical
import sched, time
from datetime import datetime
from discord.ext import tasks, commands
##from discord.ext import bot
##TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = open("key.txt", "r").read()
GUILD = '760098399869206529'
intents = discord.Intents.all()
##client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='|',intents=intents)

######################################################
urlfile=open("urlkey.csv", mode="r").read().split("\n")
urlkey=[]
for x in urlfile:
    urlkey.append(x.split(","))
del urlkey[-1]
######################################################
print(time.time())
future =[]
tmpvar=""
scheduler = sched.scheduler(time.time, time.sleep)
class DiscordBot():

    @bot.event
    async def on_ready():
        bot.add_cog(MyCog())
        print(bot.user)
        guild01=bot.guilds[0]

    @bot.command(name='test')
    async def test(ctx, *args):
        global tmpvar
        tmpvar=str(args)
        print(tmpvar)
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


    @bot.event
    async def on_message(message):
        global tmpvar
        if message.author == bot.user:
            return
        if message.content.startswith('|alert'):
            embedVar = discord.Embed(title="Lecture Starting", description="Desc", color=0x00ff00)
            embedVar.add_field(name="Field1", value="hi", inline=False)
            embedVar.add_field(name="Field2", value="hi2", inline=False)
            await message.channel.send(tmpvar)
            ##await message.channel.send(embed=embedVar)
            ##await message.channel.send(sched_test())
        await bot.process_commands(message)

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.timecheck.start()

    def cog_unload(self):
        self.timecheck.cancel()

    @tasks.loop(seconds=1.0)
    async def createmsg(self):
        embedVar = discord.Embed(title="Lecture Starting", description="Desc", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.add_field(name="Field2", value="hi2", inline=False)
        await bot.get_channel(762778215286177824).send(embed=embedVar)
        self.createmsg.stop()

    @tasks.loop(seconds=60.0)
    async def timecheck(self):
        global future,future5
        future=parse_ical()
        future5=future[0:5]
        await self.richifier(future5)
            ##self.createmsg.start()

    async def richifier(self,future5):  ## future 5 is [unix,online delivery,course desc, course code]
        for count,each in enumerate(future5):        #adding +[course info url] at [4]
            for x in urlkey:
                if x[0]==each[3]:
                    future5[count].append(x[1])
            if each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Friday":
                future5[count][1]="Space Cadets"
            elif each[3]=="COMP1202" and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
                future5[count][1]="FAQ Session"
            elif each[3]=="COMP1215" and (datetime.fromtimestamp(each[0]).strftime("%A")=="Friday" or datetime.fromtimestamp(each[0]).strftime("%A")=="Monday"):
                future5[count][1]="Excerise sheet help/Discussion"
            elif each[3]=="COMP1205":
                future5[count][1]="see homepage for info"
            elif each[3]=="COMP1203" and datetime.fromtimestamp(each[0]).strftime("%A")=="Friday":
                future5[count][1]="Q&A session/summarise the week's lectures"
            elif each[3]=="COMP1203" and datetime.fromtimestamp(each[0]).strftime("%A")=="Monday":
                future5[count][1]="To help with our RasPi coursework"
            ##HERERERERERER



bot.run(TOKEN)
