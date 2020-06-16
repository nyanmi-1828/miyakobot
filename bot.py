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
            await message.attachments[0].save("image.png")
            cha = 720140997765496912
            img_path = "image.png"
            await bot.get_channel(cha).send(file=discord.File(img_path))
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
    channel_write = '\n' + str(ctx.channel.id)
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
        x = 0 
        embed = discord.Embed(title="スケジュール", description="忘れずにやるの～", color=0x00ffff)
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
        i = 0
        for i in channel_list:
            ch = int(channel_list[n])
            await bot.get_channel(ch).send("おはようなの～♪今日のスケジュールはこれ！なの！")
            await bot.get_channel(ch).send(embed=embed)
            n += 1

bot.run(BOT_TOKEN)
