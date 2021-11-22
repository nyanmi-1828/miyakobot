from discord.ext import commands,tasks
import discord
import traceback
import os

cogs = [
    'cogs.help',
    'cogs.miyako',
    'cogs.slot',
    'cogs.music',
    'cogs.event',
    'cogs.arena'
    ]
# cogs.help = helpコマンド
# cogs.miyako = miyako,talk,joubutsuなど細かいコマンド
# cogs.slot = slotコマンド
# cogs.music = music系コマンド　俺には分からん（コピペなので）
# cogs.event = event処理
# cogs.arena = m!arenaの画像処理系はこっち

class MyBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self, command_prefix,help_command):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix,help_command)

        # cogsに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

if __name__ == '__main__':
    BOT_TOKEN = os.environ['TOKEN']
    bot = MyBot(command_prefix='m!', help_command=None)
    bot.run(BOT_TOKEN) # Botのトークン
