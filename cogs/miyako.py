import discord
from discord.ext import commands
import random
import glob

with open('./src/r18.txt', mode='r', encoding='utf-8') as r18:
    miyakor18_list = r18.read().split('\n')

class Miyako(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def miyako(self,ctx):
        image_list = glob.glob('./img/*')
        img = random.choice(image_list)
        await ctx.send(file=discord.File(img))

    @miyako.command()
    async def nsfw-r18(self,ctx):
        global miyakor18_list
        miyakor18 = random.choice(miyakor18_list)
        await ctx.send(miyakor18)

def setup(bot):
    bot.add_cog(Miyako(bot))