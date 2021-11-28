import discord
from discord.ext import commands
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from niconico_dl import NicoNicoVideoAsync
import re
import os

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""

class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""
    
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'venv/bot/videos/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester, site_type):
        super().__init__(source)
        self.requester = requester
        self.site_type = site_type

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop):
        if (m := re.search('www.nicovideo.jp/watch/sm([0-9]+)', search)) or (m := re.search('sp.nicovideo.jp/watch/sm([0-9]+)', search)) or (m := re.search('nico.ms/sm([0-9]+)', search)):
            sm_id = m.groups()[0]
            url = "https://www.nicovideo.jp/watch/sm" + sm_id
            data = dict()
            async with NicoNicoVideoAsync(url) as nico:
                data_dict = await nico.get_info()
                data = {"title": data_dict["video"]["title"], "webpage_url": url}
                await ctx.send(f'```ini\n[{data["title"]} をQueueに追加したの]\n```')
            return SiteTypeClass(data["title"],ctx.author,data["webpage_url"],"niconico")
        else:
            loop = loop or asyncio.get_event_loop()
            
            to_run = partial(ytdl.extract_info, url=search, download=False)
            data = await loop.run_in_executor(None, to_run)

            if 'entries' in data:
                data = data['entries'][0]

            # 一番音質いい奴流す
            formats = [
                format_
                for format_ in data['formats']
                if format_['acodec'] == 'opus'
            ]
            formats = sorted(formats, key=lambda x: x['asr'], reverse=True)
            formats = sorted(formats, key=lambda x: x['abr'], reverse=True)
            best_audio_url = formats[0]['url']

            await ctx.send(f'```ini\n[{data["title"]} をQueueに追加したの]\n```')

            return cls(discord.FFmpegPCMAudio(best_audio_url), data=data, requester=ctx.author, site_type="youtube")

class NicoNicoSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.FFmpegPCMAudio, *, title, requester):
        super().__init__(source)
        self.title = title
        self.requester = requester

class SiteTypeClass:
    def __init__(self, title, requester, web_url, site_type):
        self.site_type = site_type
        self.title = title
        self.requester = requester
        self.web_url = web_url

class Mp3Source(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.FFmpegPCMAudio, *, title, requester, path):
        super().__init__(source)
        self.title = title
        self.path = path
        self.requester = requester
        self.site_type = "local"
        
class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'loop')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None
        self.loop = asyncio.Event()

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            try:
                async with timeout(300): 
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                if self in self._cog.players.values():
                    return await self.destroy(self._guild)
                return
            # if self.loop.is_set():
            #     await self.queue.put(source)
            if source.site_type == "local":
                source.volume = self.volume
                self.current = source
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
                self.np = await self._channel.send(f'今流している曲なの: `{source.title}`'
                                                        f' `{source.requester}` のリクエストなの')
                await self.next.wait()
                source.cleanup()
                self.current = None
            elif source.site_type == "niconico":
                url = source.web_url
                async with NicoNicoVideoAsync(url) as nico:
                    link = await nico.get_download_link()
                    niconico_source = discord.FFmpegPCMAudio(link, **ffmpegopts)
                    source = NicoNicoSource(niconico_source, title=source.title, requester=source.requester)
                    source.volume = self.volume
                    self.current = source
                    self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
                    self.np = await self._channel.send(f'今流している曲なの: `{source.title}`'
                                                        f' `{source.requester}` のリクエストなの')
                    await self.next.wait()
                    source.cleanup()
                    self.current = None
            elif source.site_type == "youtube":
                source.volume = self.volume
                self.current = source

                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
                self.np = await self._channel.send(f'今流している曲なの: `{source.title}`'
                                                   f' `{source.requester}` のリクエストなの')
                await self.next.wait()
                source.cleanup()
                self.current = None

    async def destroy(self, guild: discord.Guild):
        if guild.voice_client:
            await self._channel.send("曲流さないなら抜けるの")
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('プライベートメッセージでこのコマンドは使えないの！')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('ボイスチャンネルに接続するときにエラーが起きたの '
                           'オマエがボイスチャンネルに先に入る必要があるの！')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player
    
    def del_player(self, ctx):
        try:
            del self.players[ctx.guild.id]
        except KeyError:
            pass

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            if not ctx.guild:
                raise commands.NoPrivateMessage
                return
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send('オマエがボイスチャンネルに先に入る必要があるの！あるいは指定してなの')
                return

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            if not channel == None:
                try:
                    await vc.move_to(channel)
                    await ctx.send(f'**{channel}** に入ったの～')
                    return
                except asyncio.TimeoutError:
                    await ctx.send('<{channel}> に移動しようとしたけどタイムアウトしたの')
                    return
        else:
            if not channel == None:
                try:
                    await channel.connect()
                    await ctx.send(f'**{channel}** に入ったの～')
                    return
                except asyncio.TimeoutError:
                    await ctx.send('<{channel}> に接続しようとしたけどタイムアウトしたの')
                    return

    @commands.command(name='play', aliases=['sing','p'])
    async def play_(self, ctx, *, search: str = None):
        if search is None:
            return await ctx.send("`m!play [url]`の形式で入力すれば再生してやるの　検索機能はないの")
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        try:
            async with timeout(20):
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
                await player.queue.put(source)
        except Exception as e:
            await ctx.send(f"多分なんかエラー起きたの```{str(e)}```")
        
    @commands.command(aliases=['mp3','pmp3','singmp3'])
    async def playmp3(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("mp3ファイルを送れなの")
            try:
                message = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.attachments, timeout=300)
            except asyncio.TimeoutError:
                return
            else:
                attachments = message.attachments
        else:
            attachments = ctx.message.attachments
            
        vc = ctx.voice_client
        if not vc:
            await ctx.invoke(self.connect_)

        def file_check(filename, i):
            if os.path.isfile(f'{filename}{i}.mp3'):
                return file_check(filename, i + 1)
            else:
                return f'{filename}{i}.mp3'
            
        async def mp3_file_save(attachment: discord.Attachment):
            i = 0
            path = file_check(attachment.filename, i)
            await attachment.save(path)
            return path
                
        for attachment in attachments:
            await ctx.trigger_typing()
            player = self.get_player(ctx)
            path = await mp3_file_save(attachment)
            source = Mp3Source(discord.FFmpegPCMAudio(path), title=attachment.filename, requester=ctx.author, path=path)
            await ctx.send(f'```ini\n[{source.title} をQueueに追加したの]\n```')
            await player.queue.put(source)

    @commands.command()
    async def loop(self, ctx):
        if not self.get_player(ctx).loop.is_set():
            self.get_player(ctx).loop.set()
            await ctx.send("キューをループするようにしたの")
        else:
            self.get_player(ctx).loop.clear()
            await ctx.send("キューをループしないようにしたの")

    @commands.command(name='pause')
    async def pause_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('何も再生してないの！')
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: 曲を一回止めるの～')

    @commands.command(name='resume')
    async def resume_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('何も再生してないの！')
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: 再開するの～')

    @commands.command(name='skip')
    async def skip_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('何も再生してないの！')

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: スキップしたの～')

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('ボイスチャンネルに接続してないの！')

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('キューには何もないの！')

        upcoming = list(player.queue._queue)

        fmt = '\n'.join(f'**`{_.title}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)

    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('ボイスチャンネルに接続してないの！')

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('何も再生してないの！')

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'今流している曲なの: `{vc.source.title}` '
                                   f'`{vc.source.requester}` からのリクエストなの')

    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float = None):
        vc = ctx.voice_client
        player = self.get_player(ctx)
        if not vc or not vc.is_connected():
            return await ctx.send('ボイスチャンネルに接続してないの！')
        if vol is None:
            return await ctx.send('今のvolumeは ' + str(player.volume) + ' なの')
        if not 0 <= vol <= 100:
            return await ctx.send('0～100までの値を入力してなの')

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: volumeを **{vol}%** に設定したの')

    @commands.command(name='stop')
    async def stop_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('何も再生してないの！')

        await self.cleanup(ctx.guild)
        await ctx.send("ボイスチャンネルから切断したの")

    @commands.command(aliases=["disconnect","bye"])
    async def leave(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send("ミヤコはこのサーバーのボイスチャンネルに参加してないの！")
            return

        self.del_player(ctx)
            
        ffmpeg_audio_source = discord.FFmpegPCMAudio('./mp3/disconnect.mp3')
        next_ = asyncio.Event()
        next_.clear()
        vc.play(ffmpeg_audio_source, after=lambda _: self.bot.loop.call_soon_threadsafe(next_.set))
        await next_.wait()
        await vc.disconnect()
        await ctx.send("ボイスチャンネルから切断したの")


def setup(bot):
    bot.add_cog(Music(bot))