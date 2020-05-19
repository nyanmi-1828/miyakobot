import discord
import traceback
import random
import glob
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!',help_command=None)

BOT_TOKEN = os.environ['TOKEN']

# imgフォルダに入ってる画像のパスを全部取得
image_list = glob.glob('img/*')

purin_value = 0

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

@bot.event
async def on_ready():
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="!helpでヘルプが見れるの めんどくさいから一回で覚えろなの"))

@bot.command(name='help')
async def _help(ctx):
    embed=discord.Embed(title="ヘルプ", description="コマンド一覧なの これを表示するたびに1プリンなの", color=0x00ffff) 
    embed.add_field(name="!miyako", value="ミヤコの画像を表示するの かわいいの", inline=False) 
    embed.add_field(name="!talk", value="喋らないの プリン🍮をくれたら喋っても良いの", inline=False) 
    embed.add_field(name="!pudding", value="プリンのレシピを貼るの 早く作れなの", inline=False) 
    embed.add_field(name="!omikuji", value="オマエの運勢を占ってやるの", inline=False) 
    await ctx.send(embed=embed)

@bot.command()
async def talk(ctx):
    await ctx.send("プリンも無いのに動くわけないの")

@bot.command()
async def miyako(ctx):
    # image_listの中から1つ画像を選択
    img = random.choice(image_list)
    # 選択した画像を投稿
    await ctx.send(file=discord.File(img))

@bot.command()
async def pudding(ctx):
    purin = random.choice(recipe_list)
    await ctx.send(purin)

@bot.command()
async def omikuji(ctx):
    omikuji = random.choice(omikuji_list)
    await ctx.send(omikuji)

@bot.event
async def on_reaction_add(reaction,user):
    print("emoji")
    print(reaction.emoji)
    global purin_value
    print(purin_value)
    miya_talk = random.choice(talk_list)
    if reaction.emoji == "🍮" and purin_value < 10:
        purin_value += 1
        await reaction.message.channel.send(miya_talk)
    elif purin_value == 15:
        await reaction.message.channel.send("こんなにプリンを食べたらミヤコ死んじゃうの…あ、もう死んでたの")
        purin_value = 0
    else:
        pass
            
bot.run(BOT_TOKEN)
