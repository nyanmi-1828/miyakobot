import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="help")
    async def _help(self, ctx):
        if ctx.invoked_subcommand is None:
            page = 0
            i = 0
            embed1 = discord.Embed(title="ヘルプ", description="コマンド一覧の1ページ目なの ネタ系コマンドなの", color=0x00ffff)
            embed1.add_field(name="**m!help**", value="コマンドの説明を表示するの m!help [コマンド名]で各コマンドの詳しい説明をしてやるの", inline=False) 
            embed1.add_field(name="**m!miyako**", value="ミヤコの画像を表示するの かわいいの", inline=False) 
            embed1.add_field(name="**m!miyakor18**", value="サイテーなの ケーベツしたの", inline=False) 
            embed1.add_field(name="**m!talk**", value="喋らないの プリン🍮をくれたら喋っても良いの", inline=False) 
            embed1.add_field(name="**m!pudding**", value="プリンのレシピを貼るの 早く作れなの", inline=False) 
            embed1.add_field(name="**m!omikuji**", value="オマエの運勢を占ってやるの", inline=False) 
            embed1.add_field(name="**m!slot**", value="スロットが出来るの プリンが大当たりなの～♪", inline=False) 
            embed1.add_field(name="**m!joubutsu**", value="や、やめてなの…", inline=False)
            embed2 = discord.Embed(title="ヘルプ", description="コマンド一覧の2ページ目なの VC系コマンドなの", color=0x00ffff)
            embed2.add_field(name="**m!join**", value="ボイスチャンネルに接続するの ミヤコが喋れるようになるの", inline=False)
            embed2.add_field(name="**m!speak**", value="ミヤコが喋るの（未実装）", inline=False)
            embed2.add_field(name="**m!leave**", value="ボイスチャンネルから切断するの ｽｰｰｰ…", inline=False)
            embed2.add_field(name="**m!play**", value="m!play [URL]で音楽が流せるの 細かい説明はm!help playで見るの", inline=False)
            embed2.add_field(name="**m!joubutsu**", value="ぶ、VCに入ってるとミヤコの声が聞こえるの…でもやめてなの…", inline=False)
            embed3 = discord.Embed(title="ヘルプ", description="コマンド一覧の3ページ目なの 便利系コマンドなの", color=0x00ffff)
            embed3.add_field(name="**m!setschedule**", value="ミヤコが毎日のスケジュールをこのコマンドを打ったチャンネルに貼ってやるの", inline=False)
            embed3.add_field(name="**m!setscheduledelete**", value="上のコマンドで設定したチャンネルに送らなくなるの", inline=False)
            embed3.add_field(name="**m!arena**", value="バトルアリーナの対抗編成を出してやるの", inline=False)
            msg = await ctx.send(embed=embed1)
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")
            
            def check(reaction, user):
                return user == message.author and (str(reaction.emoji) == '◀' or str(reaction.emoji) == '▶')
            
            while i == 0:
                try:
                    reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await msg.remove_reaction("◀")
                    await msg.remove_reaction("▶")
                    break
                else:
                    if str(reaction.emoji) == '◀':
                        page -= 1
                    elif str(reaction.emoji) == '▶':
                        page += 1
                    
                    if page == 0:
                        page = 3
                    elif page == 4:
                        page = 1
                    
                    if page == 1:
                        await msg.edit(embed=embed1)
                    elif page == 2:
                        await msg.edit(embed=embed2)
                    elif page == 3:
                        await msg.edit(embed=embed3)
                
    @_help.command()
    async def miyako(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!miyako**',value='ミヤコの画像を表示するの 可愛いの',inline=False)
        await ctx.send(embed=embed)

    @_help.command()
    async def miyakor18(self,ctx):
        embed=discord.Embed(title="ヘルプ",color=0x00ffff)
        embed.add_field(name='**m!miyakor18**',value='貼らないの！ …m!miyakonsfwでしょうがないから貼ってやるの オマエならやらないと信じてるの',inline=False)
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

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))