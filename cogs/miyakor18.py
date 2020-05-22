import discord
from discord.ext import commands
import random

with open('./src/r18.txt', mode='r', encoding='utf-8') as r18:
    miyakor18_list = r18.read().split('\n')

class MiyakoR18(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def miyakor18(self,ctx):
        miyakor18_link = random.choice(miyakor18_list)
        await ctx.send(miyakor18_link)

def setup(bot):
    bot.add_cog(MiyakoR18(bot))