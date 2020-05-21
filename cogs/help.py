import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="help")
    async def _help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="ヘルプ", description="コマンド一覧なの これを表示するたびに1プリンなの", color=0x00ffff)
            embed.add_field(name="**!help**", value="コマンドの説明を表示するの !help [コマンド名]で各コマンドの詳しい説明をしてやるの", inline=False) 
            embed.add_field(name="**!miyako**", value="ミヤコの画像を表示するの かわいいの", inline=False) 
            embed.add_field(name="**!talk**", value="喋らないの プリン🍮をくれたら喋っても良いの", inline=False) 
            embed.add_field(name="**!pudding**", value="プリンのレシピを貼るの 早く作れなの", inline=False) 
            embed.add_field(name="**!omikuji**", value="オマエの運勢を占ってやるの", inline=False) 
            embed.add_field(name="**!joubutsu**", value="や、やめてなの…", inline=False) 
            await ctx.send(embed=embed)

    @_help.command()
    async def miyako(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**!miyako**',value='ミヤコの画像を表示するの 可愛いの',inline=False)
        await ctx.send(embed=embed)
        
    @_help.command()
    async def talk(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**!talk**',value='喋らないの ミヤコに🍮とリアクションしてくれれば喋るの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def pudding(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**!pudding**',value='プリンのレシピを貼るの 登録されてるのは今の所5個だけなの',inline=False)
        await ctx.send(embed=embed)    
        
    @_help.command()
    async def omikuji(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**!omikuji**',value='ミヤコがオマエを占ってやるの シノブより精度がいいの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def joubutsu(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**!joubutsu**',value='や、やめるの…まだ成仏したくないの…お願いだからお経はやめてなの～！',inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))