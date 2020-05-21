from discord.ext import commands,tasks
import discord
import traceback
import random
import glob
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='m!',help_command=None)
BOT_TOKEN = os.environ['TOKEN']
purin_value = 0
cogs = [
    'cogs.help'
    'cogs.miyako'
    'cogs.slot'
]

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

@bot.event
async def on_ready():
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="m!helpでヘルプが見れるの めんどくさいから一回で覚えろなの"))

@bot.command()
async def talk(ctx):
    await ctx.send("プリンも無いのに動くわけないの")

@bot.command()
async def talktest(ctx):
    await ctx.send("プリンも無いのに動くわけないの\nテストなの")

@bot.command()
async def joubutsu(ctx):
    await ctx.send("ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")    

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
    if reaction.emoji == "🍮" and purin_value < 15:
        purin_value += 1
        await reaction.message.channel.send(miya_talk)
    elif purin_value == 15:
        await reaction.message.channel.send("こんなにプリンを食べたらミヤコ死んじゃうの…あ、もう死んでたの")
        purin_value = 0
    else:
        purin_value = 0
            
bot.run(BOT_TOKEN)
