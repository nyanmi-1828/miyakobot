import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

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

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'```ini\n[{data["title"]} をQueueに追加したの]\n```')

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


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
            source = await self.queue.get()
            # if self.loop.is_set():
            #     await self.queue.put(source)
            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'送った曲の処理が出来ないの！\n'
                                             f'```css\n[{e}]\n```')
                    continue
            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'今流している曲なの: `{source.title}`'
                                               f' `{source.requester}` のリクエストなの')
            await self.next.wait()

            self.current = None

    def destroy(self, guild):
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

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
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
                    raise VoiceConnectionError(f'<{channel}> に移動しようとしたけどタイムアウトしたの')
                    return
        else:
            if not channel == None:
                try:
                    await channel.connect()
                    await ctx.send(f'**{channel}** に入ったの～')
                    return
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f'<{channel}> に接続しようとしたけどタイムアウトしたの')
                    return

    @commands.command(name='play', aliases=['sing','p'])
    async def play_(self, ctx, *, search: str):
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        try:
            async with timeout(5):
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=True)
        except:
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command()
    async def loop(self, ctx):
        if not self.get_player(ctx).loop.is_set():
            self.get_player(ctx).loop.set()
            await ctx.send("Queueをループするようにしたの")
        else:
            self.get_player(ctx).loop.clear()
            await ctx.send("Queueをループしないようにしたの")

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

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
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
        vo_client = ctx.message.guild.voice_client
        player = self.get_player(ctx)

        if not vc or not vc.is_connected():
            await ctx.send("ミヤコはこのサーバーのボイスチャンネルに参加してないの！")
            return

        while not player.queue.empty():
            vc.stop()
            break

        if vc.is_playing() and player.queue.empty():
            vc.stop()
            ffmpeg_audio_source = discord.FFmpegPCMAudio('./mp3/disconnect.mp3')
            vo_client.play(ffmpeg_audio_source)
            try:
                wait = await ctx.bot.wait_for('reaction_add' , timeout = 3.5)
            except asyncio.TimeoutError:
                await vo_client.disconnect()
                await ctx.send("ボイスチャンネルから切断したの")
            return  
            
        ffmpeg_audio_source = discord.FFmpegPCMAudio('./mp3/disconnect.mp3')
        vo_client.play(ffmpeg_audio_source)
        
        try:
            wait = await ctx.bot.wait_for('reaction_add' , timeout = 3.5)
        except asyncio.TimeoutError:
            await vo_client.disconnect()
            await ctx.send("ボイスチャンネルから切断したの")


        

def setup(bot):
    bot.add_cog(Music(bot))