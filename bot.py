from discord.ext import commands,tasks
import discord
import traceback
import random
import os
from discord.ext import commands
import io
import aiohttp
import asyncio
import youtube_dl
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
from statistics import mean
from PIL import Image
import numpy as np
import random

bot = commands.Bot(command_prefix='m!',help_command=None)
dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
BOT_TOKEN = os.environ['TOKEN']
purin_value = 0
cogs = [
    'cogs.help',
    'cogs.miyako',
    'cogs.slot',
    'cogs.music'
    ]
# cogs.help = helpコマンド
# cogs.miyako = miyako,talk,joubutsuなど細かいコマンド
# cogs.slot = slotコマンド
# cogs.music = music系コマンド　俺には分からん

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

# 喋る言葉一覧
with open('src/talk.txt', mode='r', encoding='utf-8') as talk:
    talk_list = talk.read().split('\n')

# 秘密なの
with open('src/nsfw.txt', mode='r', encoding='utf-8') as nsfw:
    nsfw_list = nsfw.read().split('\n')

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

@bot.event
async def on_ready():
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="m!helpでヘルプが見れるの めんどくさいから一回で覚えろなの"))
    loop.start()

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

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if '🍮' in before.content and not '🍮' in after.content:
        await after.channel.send('プリン返せなの～！')
    else:
        pass

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    if '🍮' in message.content:
        await message.channel.send('プリン返せなの～！')

@bot.command()
async def imgsend(ctx):

    with open('src/img.txt', mode='r', encoding='utf-8') as img:
        img_switch = img.read()

    if img_switch == "on":
        with open('src/img.txt', mode='w', encoding='utf-8') as switch:
           switch.write("off")
        await ctx.send("画像を送らないようにしたの")
        return 
    else:
        with open('src/img.txt', mode='w', encoding='utf-8') as switch2:
           switch2.write("on")
        await ctx.send("画像を送るようにしたの")
        return
    
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
        return
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
        return
    else:
        await ctx.send("このチャンネルに送るようには設定されてないの！")
        return
    
@bot.command()
async def pudding(ctx):
    purin = random.choice(recipe_list)
    await ctx.send(purin)

@bot.command()
async def omikuji(ctx):
    omikuji = random.choice(omikuji_list)
    await ctx.send(omikuji)

@bot.command()
async def miyakonsfw(ctx):
    nsfw_link = random.choice(nsfw_list)
    await ctx.send(nsfw_link)

@bot.event
async def on_reaction_add(reaction,user):
    print("emoji")
    print(reaction.emoji)
    global purin_value
    print(purin_value)
    miya_talk = random.choice(talk_list)
    if user.bot == False and reaction.emoji == "🍮" and purin_value < 10:
        purin_value += 1
        await reaction.message.channel.send(miya_talk)
    elif purin_value == 10 and reaction.emoji == "🍮":
        await reaction.message.channel.send("こんなにプリンを食べたらミヤコ死んじゃうの…あ、もう死んでたの")
        purin_value = 0
    else:
        pass

@bot.event
async def on_command_error(ctx, error):
    ch = 713459691153391707
    embed = discord.Embed(title="エラー情報", description="", color=0xf00)
    embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
    embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
    embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
    embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
    embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
    embed.add_field(name="発生エラー", value=error, inline=False)
    await bot.get_channel(ch).send(embed=embed)
    await ctx.send("エラーが出たの")

@tasks.loop(seconds=60)
async def loop():
    await bot.wait_until_ready()
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    print(now.strftime('%H:%M'))

    d = datetime.date.today()
    today = d.year * 10000 + d.month * 100 + d.day

    if now.strftime('%H:%M') == '05:00':

        # 今日のスケジュールを読み込み
        with open('src/schedule.csv', encoding='UTF-8') as f:
            reader = csv.DictReader(f)
            schedule_list = [row for row in reader]
        print(schedule_list)
        # 今日の日付をYYYYMMDD形式で取得→int型に変換
        y = 0
        embed = discord.Embed(title="**スケジュール**", description="忘れずにやるの～", color=0x00ffff)
        # startDate,endDateは"YYYYMMDD"で書く
        for x in schedule_list:
            if int(schedule_list[y]['startDate']) <= today and today <= int(schedule_list[y]['endDate']):
                a = int(schedule_list[y]['startDate'])
                b = int(schedule_list[y]['endDate'])
                print(a)
                print(b)
                startDate_MMDD = a - math.floor(a/10000) * 10000
                startDateDay = startDate_MMDD - math.floor(startDate_MMDD/100) * 100
                startDateMonth = math.floor((startDate_MMDD - startDateDay)/100)
                endDate_MMDD = b - math.floor(b/10000) * 10000
                endDateDay = endDate_MMDD - math.floor(endDate_MMDD/100) * 100
                endDateMonth = math.floor((endDate_MMDD - endDateDay)/100)

                schedule_date = str(startDateMonth) + "月" + str(startDateDay) + "日 ～ " + str(endDateMonth) + "月" + str(endDateDay) + "日"
                embed.add_field(name=schedule_date, value=schedule_list[y]['eventName'], inline=False)
                y += 1
            else:
                y += 1

        # 吐き出し
        uploadpath_channel = "/miyakobot/schedule_channel.txt"
        dbx.files_download_to_file('src/schedule_channel.txt', uploadpath_channel, rev=None)
        with open('src/schedule_channel.txt', mode='r', encoding='utf-8') as schedule_channel:
            channel_list = schedule_channel.read().split('\n')
        n = 0
        for i in channel_list:
            ch = int(channel_list[n])
            await bot.get_channel(ch).send("おはようなの～♪今日のスケジュールはこれ！なの！")
            await bot.get_channel(ch).send(embed=embed)
            n += 1

# -------------------------------------ここから下画像処理用------------------------------------------------

# ----------------データ格納場--------------------
arena_chara_list = []
size_list = {
    'iPhoneXr':{'y1':238, 'y2':302, 'x':[[1168,1234],[1238,1304],[1308,1374],[1379,1445],[1448,1517]]}, \
    'xperia':{'y1':436, 'y2':556, 'x':[[1939,2060],[2067,2190],[2197,2318],[2327,2448],[2456,2576]]},\
    'Widescreen':{'y1':327, 'y2':416, 'x':[[1335,1424],[1431,1522],[1528,1618],[1625,1715],[1722,1811]]},\
    'iPad':{'y1':541, 'y2':636, 'x':[[1424,1519],[1527,1623],[1631,1726],[1733,1828],[1837,1932]]}
            }

# 画像比率分析用
Xr = round(1792/828, 2)
Widescreen = round(1920/1080, 2)
iPad = round(2048/1536, 2)
img_shape_list = {'iPhoneXr': Xr, 'xperia': 2, 'Widescreen': Widescreen, 'iPad': iPad}
width_list = {'iPhoneXr': 1792, 'xperia': 2880, 'Widescreen': 1920, 'iPad': 2048}
im = None
# ----------------データ格納場--------------------

# 値から辞書型リストのキーを取得
def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

# 各キャラ画像切り抜き
def cropping(x1,y1,x2,y2,name):
    global im
    img_size = (66, 64)
    im_crop = im.crop((x1, y1, x2, y2))
    img_path = 'data/crop/arena_pillow_crop_' + name + '.jpg'
    im_crop.save(img_path, quality=95)
    
    img = cv2.imread(img_path)
    img = cv2.resize(img,img_size)
    cv2.imwrite(img_path,img)

# 画像認識
def image_check(file_path):
    global arena_chara_list
    # get parameters
    target_file_path = './data/crop/arena_pillow_crop_' + file_path + '.jpg'
    comparing_dir_path = './data/save/'

    # setting
    img_size = (66, 64)
    channels = (0, 1, 2)
    mask = None
    hist_size = 256
    ranges = (0, 256)
    ret = {}

    # get comparing files
    pattern = '%s/*.jpg'
    comparing_files = glob.glob(pattern % (comparing_dir_path))
    if len(comparing_files) == 0:
        logging.error('no files.')

    # read target image
    target_file_name = os.path.basename(target_file_path)
    target_img = cv2.imread(target_file_path)
    target_img = cv2.resize(target_img, img_size)

    for comparing_file in comparing_files:
        comparing_file_name = os.path.basename(comparing_file)

        tmp = []
        for channel in channels:
            # calc hist of target image
            target_hist = cv2.calcHist([target_img], [channel], mask, [hist_size], ranges)

            # read comparing image
            comparing_img_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                comparing_file,
            )
            comparing_img = cv2.imread(comparing_img_path)
            # calc hist of comparing image
            comparing_hist = cv2.calcHist([comparing_img], [channel], mask, [hist_size], ranges)

            # compare hist
            tmp.append(cv2.compareHist(target_hist, comparing_hist, 0))

        # mean hist
        ret[comparing_file] = mean(tmp)

    # sort
    result_list = []
    for k, v in sorted(ret.items(), reverse=True, key=lambda x: x[1]):
        logging.info('%s: %f.' % (k, v))
        result_list.append(k)

    printname_old = result_list[0]
    printname = printname_old.replace('./data/save\\', '').replace('.jpg', '')
    print(printname)
    arena_chara_list.append(printname)

@bot.command()
async def arena_tes(ctx):
    img_path = "data/image/arena_test.jpg"
    await ctx.message.attachments[0].save(img_path)

# botのコマンド部分
@bot.command()
async def arena(ctx):
    global width_list
    global size_list
    global img_shape_list
    global arena_chara_list
    global im
    
    img_path = "data/image/arena_test.jpg"
    channel = ctx.message.channel
    await ctx.send("画像を送ってなの～")
    # 画像が送られてくるまで待つ
    def check(msg):
        return msg.author == ctx.message.author and msg.attachments

    receive_msg = await ctx.bot.wait_for('message',check=check)
    await receive_msg.attachments[0].save(img_path)
    
    img = cv2.imread(img_path)
    img_height,img_width,_ = img.shape

    # 読み込んだ画像の比率
    img_shape = round(img_width/img_height, 2)
    
    # 比率から機種を判別
    keys_list = get_keys_from_value(img_shape_list, img_shape)
    keys = keys_list[0]

    # 多解像度対応用に変換
    resize_width = width_list[keys]
    resize_height = resize_width / img_width * img_height
    img = cv2.resize(img,(int(resize_width),int(resize_height)))
    cv2.imwrite(img_path,img)

    im = Image.open('data/image/arena_test.jpg')
    y1 = size_list[keys]['y1']
    y2 = size_list[keys]['y2']
    x = size_list[keys]['x']
    cropping(x[0][0],y1,x[0][1],y2,"p1")
    cropping(x[1][0],y1,x[1][1],y2,"p2")
    cropping(x[2][0],y1,x[2][1],y2,"p3")
    cropping(x[3][0],y1,x[3][1],y2,"p4")
    cropping(x[4][0],y1,x[4][1],y2,"p5")

    image_check("p1")
    image_check("p2")
    image_check("p3")
    image_check("p4")
    image_check("p5")

    await ctx.send(arena_chara_list)
    arena_chara_list.clear()

bot.run(BOT_TOKEN)
