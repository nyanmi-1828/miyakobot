import discord
from discord.ext import commands
import random
import glob
import asyncio
import os
import io
import asyncio
import datetime
import pytz
import csv
import math
import dropbox
import glob
import logging
import sys
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

mp3_j_list = glob.glob('./mp3/joubutsu/*')
mp3_s_list = glob.glob('./mp3/speak/*')
dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
dbx.files_download_to_file('src/miyakobot-spreadsheet.json', '/miyakobot/miyakobot-spreadsheet-f0f4058290d2.json', rev=None)
credentials = ServiceAccountCredentials.from_json_keyfile_name('src/miyakobot-spreadsheet.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = os.environ['SpreadSheet']
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

# srcにデータを全て格納済み
# プリンレシピ一覧
with open('src/pudding_recipe.txt', mode='r', encoding='utf-8') as recipe:
    recipe_list = recipe.read().split('\n')

# おみくじ一覧
with open('src/omikuji.txt', mode='r', encoding='utf-8') as omikuji:
    omikuji_list = omikuji.read().split('\n')

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
        
    @commands.command()
    async def pudding(ctx):
        purin = random.choice(recipe_list)
        await ctx.send(purin)

    @commands.command()
    async def omikuji(ctx):
        omikuji = random.choice(omikuji_list)
        await ctx.send(omikuji)
        
    @commands.command()
    async def setschedule(ctx):
        channel_write = '\n' + str(ctx.channel.id)
        channel = str(ctx.channel.id)
        print(channel)

        uploadpath_channel = "/miyakobot/schedule_channel.txt"
        dbx.files_download_to_file('src/schedule_channel.txt', uploadpath_channel, rev=None)
        with open('src/schedule_channel.txt', mode='r', encoding='utf-8') as cha:
            channel_list = cha.read().split('\n')

        if channel in channel_list:
            await ctx.send("もうこのチャンネルに送るよう設定されてるの！")
        else:
            with open('src/schedule_channel.txt', mode='a', encoding='utf-8') as channel_set:
                channel_set.write(channel_write)
            with open('src/schedule_channel.txt', 'rb') as f:
                dbx.files_upload(f.read(), uploadpath_channel, mode=dropbox.files.WriteMode.overwrite)
            await ctx.send("このチャンネルにスケジュールを送るようにしたの！")
            
    @commands.command()
    async def setscheduledelete(ctx):
        channel = str(ctx.channel.id)
        print(channel)

        uploadpath_channel = "/miyakobot/schedule_channel.txt"
        dbx.files_download_to_file('src/schedule_channel.txt', uploadpath_channel, rev=None)
        with open('src/schedule_channel.txt', mode='r', encoding='utf-8') as cha:
            channel_list = cha.read().split('\n')

        if channel in channel_list:
            channel_list.remove(channel)
            s = '\n'.join(channel_list)
            with open('src/schedule_channel.txt', mode='w', encoding='utf-8') as channel_set:
                channel_set.write(s)
            with open('src/schedule_channel.txt', 'rb') as f:
                dbx.files_upload(f.read(), uploadpath_channel, mode=dropbox.files.WriteMode.overwrite)
            await ctx.send("このチャンネルに送らないようにしたの～")
        else:
            await ctx.send("このチャンネルに送るようには設定されてないの！")
        

def setup(bot):
    bot.add_cog(Miyako(bot))