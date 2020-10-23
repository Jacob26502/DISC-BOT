import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
class DiscordBot():
    @bot.event
    async def on_ready():
        print(bot.user)
    @bot.command(name='evil', description="an eval command why god")
    async def evil(ctx, *, arg):
        if ctx.message.channel.id == 762719747963748362:
            print("Doing:"+arg)
            await eval(str(arg))
            await ctrx.message.delete()
        else:
            await ctx.send("Sounds like Mischief to me!")

bot.run(os.environ.get("DISCORD_BOT_SECRET"), reconnect=True)
