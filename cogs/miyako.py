import discord
from discord.ext import commands
import random

class Miyako(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    # imgフォルダに入ってる画像のパスを全部取得
    image_list = glob.glob('img/*')
    
    @commands.command()
    async def miyako(self,ctx):
        # image_listの中から1つ画像を選択
        img = random.choice(image_list)
        # 選択した画像を投稿
        await ctx.send(file=discord.File(img))

def setup(bot):
    bot.add_cog(Miyako(bot))