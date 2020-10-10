# bot.py
import os
import discord
from PIL import Image
import io
import urllib.request as urllib
import random as random
from icalparse import parse_ical
from discord.ext import tasks, commands
from checklist import elist
TOKEN = open("key.txt", "r").read()
GUILD = '760098399869206529'
##client = discord.Client()
##client = discord.Client(intents=intents)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
ical03=parse_ical()
ls=elist()
class DiscordBot():


    @bot.event
    async def on_ready():

        print(
            bot.user
        )

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if message.content.startswith('|test'):
            await message.channel.send("success")
    @bot.event
    async def on_raw_reaction_add(payload):

        for each in ls:
            if str(payload.message_id) == each[1]:  ##main tos
                if str(payload.emoji.id) == each[0] or payload.emoji.name == each[0]:
                    await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(int(each[2])))
                    print(payload.member.name + " " +each[3])



    @bot.event
    async def on_raw_reaction_remove(payload):
        guild=bot.guilds[0]

        for each in ls:
            if str(payload.message_id) == each[1]:
                if str(payload.emoji.id) == each[0] or str(payload.emoji.name)==each[0]:
                    await guild.get_member(payload.user_id).remove_roles(guild.get_role(int(each[2])))
                    print(guild.get_member(payload.user_id).name + " " + each[3])


bot.run(TOKEN)
