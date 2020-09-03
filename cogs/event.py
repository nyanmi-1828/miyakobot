import discord
from discord.ext import commands
import asyncio
import random

# 喋る言葉一覧
with open('./src/talk.txt', mode='r', encoding='utf-8') as talk:
    talk_list = talk.read().split('\n')

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.purin_value = 0

    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        if before.author.bot:
            return
        if '🍮' in before.content and not '🍮' in after.content:
            await after.channel.send('プリン返せなの～！')
        else:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        if message.author.bot:
            return
        if '🍮' in message.content:
            await message.channel.send('プリン返せなの～！')

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        miya_talk = random.choice(talk_list)
        if user.bot == False and reaction.emoji == "🍮" and self.purin_value < 10:
            print(reaction.emoji)
            print(self.purin_value)
            self.purin_value += 1
            await reaction.message.channel.send(miya_talk)
        elif self.purin_value == 10 and reaction.emoji == "🍮":
            await reaction.message.channel.send("こんなにプリンを食べたらミヤコ死んじゃうの…あ、もう死んでたの")
            self.purin_value = 0
        else:
            pass

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        ch = 713459691153391707
        embed = discord.Embed(title="エラー情報", description="", color=0x00ffff)
        embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
        embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
        embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
        embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
        embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
        embed.add_field(name="発生エラー", value=error, inline=False)
        await self.bot.get_channel(ch).send(embed=embed)
        await ctx.send(f"エラーが出たの エラー名:```{error}```")

def setup(bot):
    bot.add_cog(Event(bot))