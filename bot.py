import discord
import traceback
import random
import glob
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

DEVELOPER_ID = '711371885300023356'
TOKEN = 'NzExMzcxODg1MzAwMDIzMzU2.XsDv8A.l5piPx0hMkHJCF3sz62JN7SFkdM'

# imgフォルダに入ってる画像のパスを全部取得
image_list = glob.glob('img/*')

# プリンレシピ一覧
recipe_list = []
recipe_list.append('https://www.kurashiru.com/recipes/33a876db-a731-46fb-a9bb-505b3d5d294c')
recipe_list.append('https://www.youtube.com/watch?v=3jI-PRAZ4Y8')
recipe_list.append('https://www.youtube.com/watch?v=m_g6jePKNTQ')
recipe_list.append('https://www.youtube.com/watch?v=iFe-YsJ8Ts0')

# おみくじ一覧
omikuji_list = []
omikuji_list.append("姫吉なの　プリンパーティーなの～♪")
omikuji_list.append("大吉なの　プリンが美味しい一日になるの")
omikuji_list.append("中吉なの　せっかくいい運勢なんだからプリンおごってなの")
omikuji_list.append("小吉なの　プリンが食べられそうな一日なの　早くよこすの")
omikuji_list.append("吉なの　よりよい運勢のためにミヤコにプリンをお供えするの")
omikuji_list.append("末吉なの　いいからプリンをよこすの")
omikuji_list.append("凶なの　ミヤコにプリンをあげないと呪われるの")
omikuji_list.append("大凶なの　死ねなの")

# 喋る言葉一覧
talk_list = []
talk_list.append("ウィーン。プリンを食べたらプリンを食べるパワーがみなぎってきたの。早くよこすの")
talk_list.append("ぱくっ。ん～♪なめらかなの～♪")
talk_list.append("やっぱりプッチンプリンは良いの。味もコンセプトも良いの。しかも3個入りなの。ぷっち～んなの～♪")
talk_list.append("牛乳プリンは甘過ぎなくてデザートにぴったりなの～♪主食？もちろん主食もプリンなの～♪")
talk_list.append("森永牛乳プリンのパッケージに描かれてるマスコットキャラ、「ホモちゃん」って言うらしいの…")
talk_list.append("焼プリンは表面のガリガリが美味しいの～♪")
talk_list.append("かぼちゃプリン？邪道なの…")

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
    embed.add_field(name="!talk", value="喋らないの プリンをくれたら喋っても良いの", inline=True) 
    embed.add_field(name="!pudding", value="プリンのレシピを貼るの 早く作れなの", inline=True) 
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
    omi = random.choice(omikuji_list)
    await ctx.send(omi)

@bot.event
async def on_reaction_add(reaction,user):
    print("emoji")
    print(reaction.emoji)
    miya_talk = random.choice(talk_list)
    if reaction.emoji == "🍮" and purin_value < 10:
        purin_value += 1
        await reaction.message.channel.send(miya_talk)
        elif purin_value == 10:
            await ctx.send("こんなにプリンを食べたらミヤコ死んじゃうの…あ、もう死んでたの")
            purin_value = 0
            else:
                pass

bot.run(TOKEN)
