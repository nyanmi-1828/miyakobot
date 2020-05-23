from discord.ext import commands,tasks
import discord
import traceback
import random
import glob
import os
from discord.ext import commands
import io
import aiohttp

bot = commands.Bot(command_prefix='m!',help_command=None)
BOT_TOKEN = os.environ['TOKEN']
purin_value = 0
cogs = [
    'cogs.help',
    'cogs.miyako',
    'cogs.slot'
    ]
# cogs.help = helpコマンド
# cogs.miyako = miyako,talk,joubutsuなど細かいコマンド
# cogs.slot = slotコマンド

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
    await bot.change_presence(activity=discord.Game(name="メンテナンス中なの　少しコマンドが使えなくなるの"))

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
    if user.bot == False and reaction.emoji == "🍮" and purin_value < 15:
        purin_value += 1
        await reaction.message.channel.send(miya_talk)
    elif purin_value == 15:
        await reaction.message.channel.send("こんなにプリンを食べたらミヤコ死んじゃうの…あ、もう死んでたの")
        purin_value = 0
    else:
        pass

@bot.event
async def on_message(message):
    if message.content.startswith("m!"):
        pass
    
    else:
        if message.author.bot:
            return
        if '🍮' in message.content:
            await message.channel.send('でっかいプリンなの！いただきますなの～♪')

@bot.event
async def on_message_edit(before, after):
    if message.content.startswith("m!"):
        pass

    else:  
        if message.author.bot:
            return
        if '🍮' in before.content and not '🍮' in after.content:
            await message.channel.send('プリン返せなの～！')
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
    m = await bot.get_channel(ch).send(embed=embed)
    await ctx.send(f"エラーが出たの")
            
bot.run(BOT_TOKEN)
