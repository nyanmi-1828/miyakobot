import discord
from discord.ext import commands
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="help")
    async def _help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="ヘルプ", description="コマンド一覧なの", color=0x00ffff)
            embed.add_field(name="**m!help**", value="コマンドの説明を表示するの m!help [コマンド名]で各コマンドの詳しい説明をしてやるの", inline=False) 
            embed.add_field(name="**ここを見るとわかりやすいの**", value="https://github.com/nyanmi-1828/miyakobot", inline=False) 
            embed.add_field(name="**m!miyako**", value="ミヤコの画像を表示するの かわいいの", inline=False) 
            embed.add_field(name="**m!miyakor18**", value="サイテーなの ケーベツしたの", inline=False) 
            embed.add_field(name="**m!talk**", value="喋らないの プリン🍮をくれたら喋っても良いの", inline=False) 
            embed.add_field(name="**m!pudding**", value="プリンのレシピを貼るの 早く作れなの", inline=False) 
            embed.add_field(name="**m!omikuji**", value="オマエの運勢を占ってやるの", inline=False) 
            embed.add_field(name="**m!slot**", value="スロットが出来るの プリンが大当たりなの～♪", inline=False) 
            embed.add_field(name="**m!joubutsu**", value="や、やめてなの…", inline=False)
            embed.add_field(name="**m!join**", value="ボイスチャンネルに接続するの ミヤコが喋れるようになるの", inline=False)
            embed.add_field(name="**m!speak**", value="ミヤコが喋るの（未実装）", inline=False)
            embed.add_field(name="**m!leave**", value="ボイスチャンネルから切断するの ｽｰｰｰ…", inline=False)
            embed.add_field(name="**m!play**", value="m!play [URL]で音楽が流せるの 細かい説明はm!help playで見るの", inline=False)
            embed.add_field(name="**m!setschedule**", value="ミヤコが毎日のスケジュールをこのコマンドを打ったチャンネルに貼ってやるの(停止中)", inline=False)
            embed.add_field(name="**m!setscheduledelete**", value="上のコマンドで設定したチャンネルに送らなくなるの", inline=False)
            embed.add_field(name="**m!arena**", value="バトルアリーナの対抗編成を出してやるの", inline=False)
            await ctx.send(embed=embed)

    @_help.command()
    async def miyako(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!miyako**',value='ミヤコの画像を表示するの 可愛いの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def miyakor18(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!miyakor18**',value='貼らないの！期待するななの',inline=False)
        await ctx.send(embed=embed)
        
    @_help.command()
    async def talk(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!talk**',value='喋らないの ミヤコに🍮とリアクションしてくれれば喋るの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def pudding(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!pudding**',value='プリンのレシピを貼るの 登録されてるのは今の所5個だけなの',inline=False)
        await ctx.send(embed=embed)    
        
    @_help.command()
    async def omikuji(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!omikuji**',value='ミヤコがオマエを占ってやるの シノブより精度がいいの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def slot(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!slot**',value='スロットが出来るの 何かがそろう確率は49分の1、プリンは343分の1らしいの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def joubutsu(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!joubutsu**',value='や、やめるの…まだ成仏したくないの…お願いだからお経はやめてなの～！',inline=False)
        await ctx.send(embed=embed)
    
    @_help.command()
    async def play(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!play**',value='m!play [url]で音楽を再生できるの オマエが入ってるボイスチャンネルで流すの',inline=False)
        embed.add_field(name='**m!loop**',value='今のキューをループするの',inline=False)
        embed.add_field(name='**m!pause**',value='一時停止するの',inline=False)
        embed.add_field(name='**m!resume**',value='再開するの',inline=False)
        embed.add_field(name='**m!skip**',value='今の曲をとばして次の曲を流すの',inline=False)
        embed.add_field(name='**m!queue**',value='今のキューに入ってる曲を確認できるの',inline=False)
        embed.add_field(name='**m!np**',value='今の曲の名前を出すの',inline=False)
        embed.add_field(name='**m!volume**',value='音量を変えるの 0~100の値で指定してなの',inline=False)
        embed.add_field(name='**m!stop**',value='切断するの',inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def faq(ctx):
        embed = discord.Embed(title="よくある質問や出来事なの", description="詳しいことはここに書いてあるの: https://github.com/nyanmi-1828/miyakobot", color=0x00ffff)
        embed.add_field(name="エラーが出るの？", value=\
            "良かったら起こった状況とエラー名を管理者(Discord: nyanmi-1828#7675 Twitter: @nyanmi_23)のDMに送ってほしいの", inline=False)
        embed.add_field(name="m!arenaで出るキャラが間違ってるの？", value="開発段階だから許してなの 間違った時の画像を送ってなの", inline=False)
        embed.add_field(name="m!arenaの使い方が分からないの？", value="https://github.com/nyanmi-1828/miyakobot を見てほしいの…", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))