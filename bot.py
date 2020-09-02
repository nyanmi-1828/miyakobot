from discord.ext import commands,tasks
import discord
import traceback
import random
import os
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
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

bot = commands.Bot(command_prefix='m!',help_command=None)
dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
BOT_TOKEN = os.environ['TOKEN']
purin_value = 0
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
dbx.files_download_to_file('src/miyakobot-spreadsheet.json', '/miyakobot/miyakobot-spreadsheet-f0f4058290d2.json', rev=None)
credentials = ServiceAccountCredentials.from_json_keyfile_name('src/miyakobot-spreadsheet.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = os.environ['SpreadSheet']
SPREADSHEET_KEY2 = os.environ['SpreadSheet2']
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
worksheet2 = gc.open_by_key(SPREADSHEET_KEY2).sheet1
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

@bot.event
async def on_reaction_add(reaction,user):
    global purin_value
    miya_talk = random.choice(talk_list)
    if user.bot == False and reaction.emoji == "🍮" and purin_value < 10:
        print(reaction.emoji)
        print(purin_value)
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
    embed = discord.Embed(title="エラー情報", description="", color=0x00ffff)
    embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
    embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
    embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
    embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
    embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
    embed.add_field(name="発生エラー", value=error, inline=False)
    await bot.get_channel(ch).send(embed=embed)
    await ctx.send(f"エラーが出たの エラー名:```{error}```")
        
# -------------------------------↑イベント処理↑-------------------------------
# -------------------------------↓コマンド処理↓-------------------------------       

@bot.command()
async def faq(ctx):
    embed = discord.Embed(title="よくある質問や出来事なの", description="詳しいことはここに書いてあるの: https://github.com/nyanmi-1828/miyakobot", color=0x00ffff)
    embed.add_field(name="エラーが出るの？", value=\
        "良かったら起こった状況とエラー名を管理者(Discord: nyanmi-1828#7675 Twitter: @nyanmi_23のDMに送ってほしいの)", inline=False)
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
# -----------------------------------ここから下画像処理用--------------------------------

# ----------------データ格納場--------------------
arena_chara_list = []
size_list = {
    'iPhoneXr':{'y1':238, 'y2':302, 'x':[[1168,1234],[1238,1304],[1308,1374],[1379,1445],[1448,1517]]}, \
    'xperia':{'y1':436, 'y2':556, 'x':[[1939,2060],[2067,2190],[2197,2318],[2327,2448],[2456,2576]]},\
    'Widescreen':{'y1':327, 'y2':416, 'x':[[1335,1424],[1431,1522],[1528,1618],[1625,1715],[1722,1811]]},\
    'iPad':{'y1':541, 'y2':636, 'x':[[1424,1519],[1527,1623],[1631,1726],[1733,1828],[1837,1932]]}
}
chara_list = {
    'aoi':'アオイ','hiyori':'ヒヨリ','io':'イオ','kaori_summer':'水着カオリ','kasumi_magical':'カスミ（マジカル）',\
    'kokkoro':'コッコロ','kurumi':'クルミ','kuuka':'クウカ','kyaru':'キャル','maho':'マホ',\
    'nozomi_christmas':'ノゾミ（クリスマス）','pecorine':'ペコリーヌ','pecorine_summer':'水着ペコリーヌ',\
    'rei_newyear':'正月レイ','rima':'リマ','rino':'リノ','saren_summer':'水着サレン',\
    'shinobu_halloween':'シノブ（ハロウィン）','tsumugi':'ツムギ','yukari':'ユカリ','yuki':'ユキ',\
    'tamaki':'タマキ','rin_deremas':'リン（デレマス）','pecorine_princess':'ペコリーヌ（プリンセス）','yui':'ユイ',\
    'runa':'ルナ','hatsune':'ハツネ','kokkoro_princess':'コッコロ（プリンセス）','mifuyu':'ミフユ','yuni':'ユニ',\
    'kuuka_ooedo':'クウカ（オーエド）','ruka':'ルカ','rin':'リン','ayumi':'アユミ'
}

# 画像比率分析用
Xr = round(1792/828, 2)
iPhone11 = round(2436/1125, 2)
Widescreen = round(1920/1080, 2)
iPad = round(2048/1536, 2)
img_shape_list = {'iPhoneXr': Xr, 'iPhoneXr': iPhone11, 'xperia': 2, 'Widescreen': Widescreen, 'iPad': iPad}
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

class Imagehashmanager(object):
    """
    imageハッシュ同士の比較や辞書のキーに使える
    """
    
    def __init__(self, binary_array: np.ndarray):
        self.hash = binary_array
    
    def __str__(self):
        return _binary_array_to_hex(self.hash.flatten())
    
    def __repr__(self):
        return repr(self.hash)
    
    def __sub__(self, other):
        if other is None:
            raise TypeError('Other hash must not be None.')
        if isinstance(other, Imagehashmanager):
            if self.hash.size != other.hash.size:
                raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.hash.shape)
            return np.count_nonzero(self.hash.flatten() != other.hash.flatten())
        elif isinstance(other, np.ndarray):
            if self.hash.size != other.size:
                raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.shape)
            return np.count_nonzero(self.hash.flatten() != other.flatten())
        else:
            raise TypeError(f'Other Invalid type:{type(other)}')
    
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Imagehashmanager):
            return np.array_equal(self.hash.flatten(), other.hash.flatten())
        elif isinstance(other, np.ndarray):
            return np.array_equal(self.hash.flatten(), other.flatten())
        else:
            raise TypeError(f'Other Invalid type:{type(other)}')
    
    def __ne__(self, other):
        if other is None:
            return False
        if not isinstance(other, Imagehashmanager):
            # ここ1次元ではない場合大丈夫か?
            return not np.array_equal(self.hash.flatten(), other)
        else:
            return not np.array_equal(self.hash.flatten(), other.hash.flatten())
    
    def __hash__(self):
        # this returns a 8 bit integer, intentionally shortening the information
        return sum([2 ** (i % 8) for i, v in enumerate(self.hash.flatten()) if v])
        # long ver
        # return sum([2 ** i for (i, v) in enumerate(self.hash.flatten()) if v])
        
def dhash(image: np.ndarray, hashsize: int = 8):
    """
    8x8 = 64[bit]
    Difference Hash computation.
    following http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

    computes differences horizontally
    """
    assert image.shape[-1] in (1, 3)  # グレイスケールまたはRGBではない場合エラー、下のコードでもよい
    #     raise RuntimeError(f"Unknown format: shape={image.shape}")
    if hashsize < 2:
        raise ValueError("Hash size must be greater than or equal to 2")
    img = cv2.resize(image, (hashsize + 1, hashsize), interpolation=cv2.INTER_AREA)  # リサイズ
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if image.shape[2] == 3 else img  # 上の行と順番逆でもいいかも
    
    resized = np.asarray(img)
    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]
    
    # 念の為
    diff = np.asarray(diff, dtype=bool)
    return Imagehashmanager(diff)

hash_list = []
pattern = '%s/*.jpg'
comparing_dir_path = './data/save/'
comparing_files = glob.glob(pattern % (comparing_dir_path))
for comparing_file in comparing_files:
    img = cv2.imread(comparing_file)
    hash = dhash(img)
    hash_list.append(hash)

# 画像認識
def image_check(file_path):
    global arena_chara_list
    printname = ''
    # get parameters
    target_file_path = './data/crop/arena_pillow_crop_' + file_path + '.jpg'

    # setting
    img_size = (66, 64)
    channels = (0, 1, 2)
    mask = None
    hist_size = 256
    ranges = (0, 256)
    ret = {}

    # read target image
    target_img = cv2.imread(target_file_path)
    target_img = cv2.resize(target_img, img_size)
    
    hash = dhash(target_img)
    min_hash_list = [hash_list[i] - hash for i in range(len(hash_list))]
    for i in range(len(hash_list)):
        if min_hash_list[i] == min(min_hash_list):
            printname = comparing_files[i].replace('./data/save\\', '').replace('.jpg', '')
    
    arena_chara_list.append(printname)

# 複数の要素番号を取得
def my_index_multi(l, x):
    return [i for i, _x in enumerate(l) if _x == x]

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

    try:
        keys = keys_list[0]
    except IndexError:
        await ctx.send("画像が対応してない比率なの…")
        return

    # 多解像度対応用に変換
    try:
        resize_width = width_list[keys]
    except UnboundLocalError:
        await ctx.send("画像が対応してない比率なの…")
        return
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
    
    # 出力、判定用にまとめ
    chara_l = []
    t = 0
    for n in arena_chara_list:
        chara_l.append(chara_list[arena_chara_list[t]])
        t += 1
    chara_output = '、'.join(chara_l)
    
    # シートから編成を取得
    attackers = worksheet2.col_values(1)
    defenders = worksheet2.col_values(2)
    attack_index = my_index_multi(defenders, chara_output)

    # 取得した編成を一つにまとめる
    chara_counter = []
    y = 0
    for l in range(len(attack_index)):
        chara_counter.append(attackers[attack_index[y]])
        y += 1
    chara_counter_output = '\n'.join(chara_counter)

    if len(attack_index) == 0:
        await ctx.send(f"```{chara_output}``` に勝てる編成が見つからなかったの…")
    else:
        await ctx.send(f'```{chara_output}``` に勝てそうな編成が{len(attack_index)} つ見つかったの！```{chara_counter_output}``` で勝てると思うの！')

    arena_chara_list.clear()
    chara_output = None

bot.run(BOT_TOKEN)
