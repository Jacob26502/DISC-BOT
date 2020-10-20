import os
import discord
from PIL import Image
import io
import sched, time
from datetime import datetime
from discord.ext.commands import cooldown
from discord.ext import tasks, commands
import random as random
import asyncio
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
class DiscordBot():
    @bot.event
    async def on_ready():
        print(bot.user)
    @bot.command(name='args')
    async def emlist(ctx, *, arg):
        print("Doing:"+str(arg))
        eval(str(arg))


bot.run(os.environ.get('KEY'), reconnect=True)
