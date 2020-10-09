# bot.py
import os
import discord
from PIL import Image
import io
import urllib.request as urllib
import random as random
from icalparse import parse_ical
from discord.ext import tasks, commands

TOKEN = open("key.txt", "r").read()
GUILD = '760098399869206529'
##client = discord.Client()
##client = discord.Client(intents=intents)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='|',intents=intents)
ical03=parse_ical()

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

        if payload.message_id == 763433157516066846:  ##main tos
            if payload.emoji.name == "✅":
                await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(762809681634132018))
                print(payload.member.name + " Has just agreed")
                ##do the thing
            elif payload.emoji.name == "❌":  ##main tos
                await payload.member.edit(nick="I can't follow rules")
        elif payload.message_id == 763866695218495488:  ##event nite
            if payload.emoji.name == "🐸":
                await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(763860300784730193))
                print(payload.member.name + " Joined Event Night")
        elif payload.message_id == 764154569680617512:  ##trains
            if payload.emoji.name == "🧦":
                await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(764155263200264212))
                print(payload.member.name + " Joined Femboy")



    @bot.event
    async def on_raw_reaction_remove(payload):
        guild=bot.guilds[0]
        if payload.message_id == 763433157516066846:   ##main tos
            if payload.emoji.name == "✅":
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(762809681634132018))
            elif payload.emoji.name == "❌":
                await guild.get_member(payload.user_id).edit(nick=None)


        if payload.message_id == 763866695218495488:  ##event nite
            if payload.emoji.name == "🐸":
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(763860300784730193))
                print(guild.get_member(payload.user_id).name + " Left Event Night")


        if payload.message_id == 764154569680617512:  ##trains
            if payload.emoji.name == "🧦":
                await guild.get_member(payload.user_id).remove_roles(guild.get_role(764155263200264212))
                print(guild.get_member(payload.user_id).name + " Left Femboy")



bot.run(TOKEN)
