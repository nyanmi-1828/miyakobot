import discord
from discord.ext import commands
import random
import glob
import asyncio

class Miyako(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def miyako(self,ctx):
        image_list = glob.glob('./img/*')
        img = random.choice(image_list)
        await ctx.send(file=discord.File(img))
    
    @commands.command()
    async def miyakor18(self,ctx):
        await ctx.send("14歳にそんなの求めるなんて、変態なの…？")

    @commands.command()
    async def talk(self,ctx):
        msg = await ctx.send("プリンも無いのに動くわけないの")
        await msg.add_reaction('🍮')
    
    @commands.command()
    async def joubutsu(self,ctx):
        voice_client = ctx.message.guild.voice_client
        mp3_j_list = glob.glob('./mp3/joubutsu/*')
        mp3_j = random.choice(mp3_j_list)

        if not voice_client:
            await ctx.send("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ") 
            return
        else:
            ffmpeg_audio_source = discord.FFmpegPCMAudio(mp3_j)
            voice_client.play(ffmpeg_audio_source)
            return
        

def setup(bot):
    bot.add_cog(Miyako(bot))