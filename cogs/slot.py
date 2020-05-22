import discord
from discord.ext import commands
import random

class Slot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot  
    
    @commands.command()
    async def slot(self,ctx):
        slot_list = [':custard:', ':poultry_leg:', ':lemon:', ':salt:', ':candy:',':bowl_with_spoon:',':sake:']
        result_list = [
            "プリンが3つ揃ったの～♪プッチンプリンを買ってくるの！ちょうど3つなの！",
            "お肉が3つ揃ったの あのお姫様にあげてくるの！お礼はプリンでよろしくなの～",
            "レモンが3つ揃ったの 恵みの一滴なの",
            "塩が3つ揃ったの やめるの！塩をミヤコに振らないでなの～！成仏しちゃうの～！",
            "アメが3つ揃ったの あめちゃんなの",
            "ボウルとスプーンが3つ揃ったの これでプリンを作るの！3つ同時平行で大量生産なの～",
            "お酒が3つ揃ったの お酒が入ったお風呂は身を清められるらしいの… や、やめてなの！ミヤコを突っ込まないで欲しいの！"
        ]
        A = random.choice(slot_list)
        B = random.choice(slot_list)
        C = random.choice(slot_list)
        result = "%s%s%s" % (A, B, C)
        if A == B and B == C:
            await ctx.send(result + "\n" + result_list[slot_list.index(A)])
        elif A == B ^ B == C:
            await ctx.send(result + "\n" + "もうちょっとだったの！もう一回なの！")
        else:
            await ctx.send(result + "\n" + "はずれなの！もう一回なの！")
        
def setup(bot):
    bot.add_cog(Slot(bot))