import discord
from discord.ext import commands
import random

class MiyakoR18(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def miyako-nsfw-r18(self,ctx):
    with open('./src/r18.txt', mode='r', encoding='utf-8') as r18:
        miyakor18_list = r18.read().split('\n')
    miyakor18 = random.choice(miyakor18_list)
    await ctx.send(miyakor18)

def setup(bot):
    bot.add_cog(MiyakoR18(bot))