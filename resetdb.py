from tinydb import TinyDB, Query, where
import os
import sys
import discord
import io
import sched, time
import asyncio
from dotenv import load_dotenv
from tinydb.operations import delete, increment, decrement, set
from discord.ext.commands import cooldown
from discord.ext import tasks, commands
import json
load_dotenv()
db = TinyDB('db.json')
person = Query()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
out = open("OUTPUT.txt", "w", encoding='utf-8')
class DiscordBot():
    global clok



    async def rem_lvl():
        guild=bot.get_guild(760098399869206529)

        for member00 in guild.members:
            await asyncio.sleep(0.2)
            print(member00.name)
            await member00.remove_roles(guild.get_role(776856319261016074))##LVL2
            await member00.remove_roles(guild.get_role(776856505269092403))##LVL3
            await member00.remove_roles(guild.get_role(776856581551292448))##LVL4
            await member00.remove_roles(guild.get_role(776856620981944331))##LVL5

    async def makefile():
        guild=bot.get_guild(760098399869206529)
        var=""
        for x in sorted(db.all(),key=lambda x:x.get('msgcount'),reverse=True):
            abc = guild.get_member(int(x['id']))
            print((x['id']) + " " + str(abc))
            var = (var + str(x['id']) + "," + str(abc.name) + ", " + str(x['msgcount'])+"\n")
        print(var)
        out.write(var)
        out.close()


    @bot.event
    async def on_ready():
        #bot.add_cog(JAILSTUFF(bot))
        await bot.change_presence(status=discord.Status.dnd)    ##TODO: REMOVE this when going back online ##################
        print(bot.user)
        await DiscordBot.makefile()
        await DiscordBot.rem_lvl()
        db.update(set('msgcount',100),person.msgcount>=100)
        db.update(set('hornycount',0))
bot.run(os.environ.get("DISCORD_BOT_SECRET"), reconnect=True)
