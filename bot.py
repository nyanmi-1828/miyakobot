from discord.ext import commands,tasks
import discord
import traceback
import random
import os
import io
import asyncio
import datetime
import pytz
import csv
import math
import dropbox
import string
import cv2
from docopt import docopt
import glob
import logging
import sys
from PIL import Image
import numpy as np
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

bot = commands.Bot(command_prefix='m!',help_command=None)
dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
BOT_TOKEN = os.environ['TOKEN']
dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
dbx.files_download_to_file('src/miyakobot-spreadsheet.json', '/miyakobot/miyakobot-spreadsheet-f0f4058290d2.json', rev=None)
credentials = ServiceAccountCredentials.from_json_keyfile_name('src/miyakobot-spreadsheet.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = os.environ['SpreadSheet']
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

cogs = [
    'cogs.help',
    'cogs.miyako',
    'cogs.slot',
    'cogs.music',
    'cogs.event',
    'cogs.arena'
    ]
# cogs.help = helpコマンド
# cogs.miyako = miyako,talk,joubutsuなど細かいコマンド
# cogs.slot = slotコマンド
# cogs.music = music系コマンド　俺には分からん（コピペなので）
# cogs.event = event処理 on_readyとon_messageだけここにいます 
# cogs.arena = なんかcogじゃないとself使えんらしい m!arenaの画像処理系はこっち

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception:
        traceback.print_exc()

# srcにデータを全て格納済み
# プリンレシピ一覧
with open('src/pudding_recipe.txt', mode='r', encoding='utf-8') as recipe:
    recipe_list = recipe.read().split('\n')

# おみくじ一覧
with open('src/omikuji.txt', mode='r', encoding='utf-8') as omikuji:
    omikuji_list = omikuji.read().split('\n')

# ------------------------------↑前処理↑----------------------------------

def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

@bot.event
async def on_ready():
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="m!helpでヘルプが見れるの 分からないことがあればm!faqを使うの"))
    # loop.start()

@bot.event
async def on_message(message):
    with open('src/img.txt', mode='r', encoding='utf-8') as img:
        img_switch = img.read()
    if message.content.startswith("m!"):
        pass
    
    else:
        if message.author.bot:
            return
        if img_switch == "on" and message.attachments and message.channel.id == 715651349454389308:
            cha = 720140997765496912
            img_path = "img_" + randomname(8) + ".png"
            await message.attachments[0].save(img_path)
            await bot.get_channel(cha).send(file=discord.File(img_path))
            os.remove(img_path)
        if '🍮' in message.content:
            await message.channel.send('でっかいプリンなの！いただきますなの～♪')
    await bot.process_commands(message)


        
# -------------------------------↑イベント処理↑-------------------------------
# -------------------------------↓コマンド処理↓-------------------------------       

@bot.command()
async def faq(ctx):
    embed = discord.Embed(title="よくある質問や出来事なの", description="詳しいことはここに書いてあるの: https://github.com/nyanmi-1828/miyakobot", color=0x00ffff)
    embed.add_field(name="エラーが出るの？", value=\
        "良かったら起こった状況とエラー名を管理者(Discord: nyanmi-1828#7675 Twitter: @nyanmi_23)のDMに送ってほしいの", inline=False)
    embed.add_field(name="m!arenaで出るキャラが間違ってるの？", value="開発段階だから許してなの 間違った時の画像を送ってなの", inline=False)
    embed.add_field(name="m!arenaの使い方が分からないの？", value="https://github.com/nyanmi-1828/miyakobot を見てほしいの…", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['i'])
async def imgsend(ctx):

    with open('src/img.txt', mode='r', encoding='utf-8') as img:
        img_switch = img.read()

    if img_switch == "on":
        with open('src/img.txt', mode='w', encoding='utf-8') as switch:
            switch.write("off")
        await ctx.send("画像を送らないようにしたの")
    else:
        with open('src/img.txt', mode='w', encoding='utf-8') as switch2:
            switch2.write("on")
        await ctx.send("画像を送るようにしたの")
    
@bot.command()
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
        
@bot.command()
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

@bot.command()
async def pudding(ctx):
    purin = random.choice(recipe_list)
    await ctx.send(purin)

@bot.command()
async def omikuji(ctx):
    omikuji = random.choice(omikuji_list)
    await ctx.send(omikuji)


# 登録されてるチャンネルになぜか出力されないので止めてます
'''
@tasks.loop(seconds=60)
async def loop():
    await bot.wait_until_ready()
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    today = now.year * 10000 + now.month * 100 + now.day
    if now.strftime('%H:%M') == '05:00':

        # 今日のスケジュールを読み込み
        schedule_list = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')
        print(schedule_list)
        # 今日の日付をYYYYMMDD形式で取得→int型に変換
        embed = discord.Embed(title="**スケジュール**", description="忘れずにやるの～", color=0x00ffff)
        # startDate,endDateは"YYYYMMDD"で書く
        x = 0
        for y in range(len(schedule_list)):
            if int(schedule_list[x]['startDate']) <= today and today <= int(schedule_list[x]['endDate']):
                a = int(schedule_list[x]['startDate'])
                b = int(schedule_list[x]['endDate'])
                print(a)
                print(b)
                startDate_MMDD = a - math.floor(a/10000) * 10000
                startDateDay = startDate_MMDD - math.floor(startDate_MMDD/100) * 100
                startDateMonth = math.floor((startDate_MMDD - startDateDay)/100)
                endDate_MMDD = b - math.floor(b/10000) * 10000
                endDateDay = endDate_MMDD - math.floor(endDate_MMDD/100) * 100
                endDateMonth = math.floor((endDate_MMDD - endDateDay)/100)

                schedule_date = str(startDateMonth) + "月" + str(startDateDay) + "日 ～ " + str(endDateMonth) + "月" + str(endDateDay) + "日"
                embed.add_field(name=schedule_date, value=schedule_list[x]['eventName'], inline=False)
                
            x += 1

        # 吐き出し
        
        channel_list = []
        uploadpath_channel = "/miyakobot/schedule_channel.txt"
        with open('src/schedule_channel.txt', mode='wb') as schedule_channel:
            metadata, res = dbx.files_download(path=uploadpath_channel)
            schedule_channel.write(res.content)
        with open('src/schedule_channel.txt', mode='r', encoding='utf-8') as sc:
            channel_list = list(map(int,sc.read().split('\n')))
            
        for ch in channel_list:
            await bot.get_channel(ch).send("おはようなの～♪今日のスケジュールはこれ！なの！")
            await bot.get_channel(ch).send(embed=embed)
        
        channel_list.clear()
'''

bot.run(BOT_TOKEN)
