import discord
import traceback
import random
import glob
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

DEVELOPER_ID = '711371885300023356'
TOKEN = 'NzExMzcxODg1MzAwMDIzMzU2.XsDv8A.l5piPx0hMkHJCF3sz62JN7SFkdM'

# imgフォルダに入ってる画像のパスを全部取得
image_list = glob.glob('img/*')
recipe_list = []
recipe_list.append('https://www.kurashiru.com/recipes/33a876db-a731-46fb-a9bb-505b3d5d294c')
recipe_list.append('https://www.youtube.com/watch?v=3jI-PRAZ4Y8')
recipe_list.append('https://www.youtube.com/watch?v=m_g6jePKNTQ')
recipe_list.append('https://www.youtube.com/watch?v=iFe-YsJ8Ts0')

@bot.event
async def on_ready():
    
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="!helpでヘルプが見れるの　めんどくさいから一回で覚えろなの"))

@bot.command(name='talk')
async def hello(ctx):
    await ctx.send("プリンも無いのに動くわけないの")

@bot.command()
async def help(ctx):
    await ctx.send("```!talk : 喋らないの　プリンをくれたら喋ってやるの\n!miyako : ミヤコの画像を貼ってやるの\n!pudding : プリンのレシピを貼るの　作れなの```")

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

@bot.event
async def on_reaction_add(reaction,user):
    print("emoji")
    print(reaction.emoji)
    if reaction.emoji == "🍮":
        await reaction.message.channel.send('ウィーン。プリンを食べたらプリンを食べるパワーがみなぎってきたの。早くよこすの')

bot.run(TOKEN)
