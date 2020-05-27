import discord
from discord.ext import commands
import random
import glob
import asyncio

mp3_j_list = glob.glob('./mp3/joubutsu/*')
mp3_s_list = glob.glob('./mp3/speak/*')

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
    async def speak(self, ctx):
        voice_client = ctx.message.guild.voice_client
        channel = voice_state.channel
        global mp3_s_list
        mp3_s = random.choice(mp3_s_list)
        if not voice_client:
            await channel.connect()
        
        ffmpeg_audio_source = discord.FFmpegPCMAudio(mp3_s)
        voice_client.play(ffmpeg_audio_source)

    @commands.command()
    async def joubutsu(self,ctx):
        voice_client = ctx.message.guild.voice_client
        global mp3_j_list
        mp3_j = random.choice(mp3_j_list)
        vc = ctx.voice_client

        if not voice_client:
            await ctx.send("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ") 
            return
        if vc.is_playing():
            await ctx.send("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ") 
            return
        else:
            ffmpeg_audio_source = discord.FFmpegPCMAudio(mp3_j)
            voice_client.play(ffmpeg_audio_source)
            return
        

def setup(bot):
    bot.add_cog(Miyako(bot))