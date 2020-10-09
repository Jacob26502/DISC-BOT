# bot.py
import os
import discord
from PIL import Image
import io
from icalparse import parse_ical
import sched, time, datetime
from discord.ext import tasks, commands
##from discord.ext import bot
##TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = open("key.txt", "r").read()
GUILD = '760098399869206529'
intents = discord.Intents.all()
##client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='|',intents=intents)
######################################################
print(time.time())
tmpvar=""
scheduler = sched.scheduler(time.time, time.sleep)
class DiscordBot():

pr()
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
        timedelta=parse_ical()
        print(timedelta[1])
        if timedelta[1]<=6000:
            self.createmsg.start()




bot.run(TOKEN)
