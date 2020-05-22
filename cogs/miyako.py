import discord
from discord.ext import commands
import random
import glob

class Miyako(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def miyako(self,ctx):
        image_list = glob.glob('../img/*')
        img = random.choice(image_list)
        await ctx.send(file=discord.File(img))

def setup(bot):
    bot.add_cog(Miyako(bot))