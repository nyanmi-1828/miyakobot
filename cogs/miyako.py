import discord
from discord.ext import commands
import random
import glob

with open('src/r18.txt', mode='r', encoding='utf-8') as r18:
    miyakor18_list = r18.read().split('\n')

class Miyako(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group()
    async def miyako(self,ctx):
        if ctx.invoked_subcommand is None:
            image_list = glob.glob('./img/*')
            img = random.choice(image_list)
            await ctx.send(file=discord.File(img))

    @miyako.command()
    async def nsfw-r18(self,ctx):
        global miyakor18_list
        miyakor18 = random.choice(miyakor18_list)
        await ctx.send(miyakor18)

    @commands.command()
    async def talk(self,ctx):
        await ctx.send("プリンも無いのに動くわけないの")
    
    @commands.command()
    async def joubutsu(self,ctx):
        await ctx.send("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ") 
        
    

def setup(bot):
    bot.add_cog(Miyako(bot))