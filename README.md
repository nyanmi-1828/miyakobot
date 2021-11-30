# miyakobot
プリコネRに登場する「ミヤコ（出雲宮子）」の非公式未公認botです　ネタ系botを作りたかったので作りました
bot招待リンク→（ https://discord.com/api/oauth2/authorize?client_id=711371885300023356&permissions=3205184&scope=bot ）
## 目次
* [Botに与えている権限](#Botに与えている権限)
* [出来ること](#出来ること)
* [使い方（コマンド一覧）](#使い方コマンド一覧)
* [m!playの詳しい使い方](#mplayの詳しい使い方)
* [m!arenaの詳しい使い方](#marenaの詳しい使い方)
* [FAQ、よくある質問](#FAQよくある質問)
* [協力いただいた方](#協力いただいた方)
* [緊急連絡先](#緊急連絡先)
## Botに与えている権限
- メッセージを送る権限（最低限）
- メッセージを編集する権限（m!helpのため、また今後botの機能追加のため）
- Embed Links（スケジュール機能のため）
- Attach Files（m!miyakoのため）
- Add Reactions（m!talkのため）
- VC接続（m!playのため）
- VC発言（同上）
## 出来ること
- おみくじやスロットのネタ要素
- 音楽再生機能（VC）
- アリーナ対抗編成検索（仮）
## 使い方（コマンド一覧）
**m!help**コマンドで大体の使い方説明が出ます
#### m!help
コマンドに関するヘルプが出ます。"m!help コマンド名"でさらに詳しい説明が出ます。
#### m!miyako
登録されているミヤコ（など）の画像を貼ってくれます。
#### m!miyakor18
貼りません。
#### m!talk
喋りません。プリンをあげると喋ってくれるかもしれません。
#### m!pudding
登録されているプリンのレシピを貼ってくれます。
#### m!omikuji
おみくじを引いてくれます。何回でも引き直せます。
#### m!slot
スロットを引いてくれます。当選確率は1/49です。多分。
#### m!joubutsu
~~やめてなの～！~~
#### m!join
ボイスチャンネルに接続します。この状態で"m!joubutsu"コマンドを打つと喋ります。かなり音量がでかいので注意。
#### m!play url
urlのところをyoutubeまたはsoundcloudのリンクにすると、自分のVCに来て音楽を流してくれます。簡易的な再生リストなどにどうぞ。詳しい使い方は後述。
#### m!speak（未実装）
喋るようになる予定です。PC壊れてデータ吹っ飛んだのでモチベがない。
#### m!leave
ボイスチャンネルから切断します。喋るので音量に注意。
#### m!setschedule
このコマンドを打ったチャンネルに今日のイベントスケジュールを貼ってくれるようになります。
#### m!setscheduledelete
上のコマンドの設定したチャンネルに送らなくなります。
#### m!arena
~~画像を貼ると対抗編成を出してくれます。使い方は後述。~~ 一時的に機能を停止しています。
## m!playの詳しい使い方
このbotは「コマンドを入力」→「キューに追加」、そして「キューに入っている曲を順次再生」という方式をとっています。<br>
#### m!play url
url先の音楽を再生（既に再生されている場合はキューに追加）します。<br>
`m!play https://youtube.com/***`のように入力します。
SoundCloudとYoutubeとNiconicoに対応しています。
#### m!playmp3
m!mp3でも反応します。
このコマンドを入力して「mp3を送れ」と言われた後にmp3ファイルを送ると再生（既に再生されている場合はキューに追加）します。
mp3でなくとも、「opusでエンコードされている」または「16ビットの48KHzステレオPCM」であるファイルは再生できます。
#### m!loop
今のキューに入っている曲をループします。再度入力することで解除されます。
#### m!pause
一時停止します。
#### m!resume
再開します。
#### m!skip
今の流れている曲を停止し、キューに登録されている次の曲を再生します。
#### m!queue
今のキューに追加されている曲を表示します。
#### m!np
今流れている曲の情報を出します。
#### m!volume 音量
ミヤコの音量を調整します。音量のところを0~100の値で指定してください。<br>
`m!volume 75`のように入力します。
#### m!stop
ミヤコの再生機能を強制終了します。
## m!arenaの詳しい使い方
- 一時的に機能を停止しています。
## よくある質問
- エラーが出まくります<br>コマンドが間違っていないか確認してみてください。あるいは僕がテスト中の可能性があります。
## 協力いただいた方
- maguro869様 - プログラム協力
- ポンズ様 - m!arena実装協力
## 緊急連絡先
開発者のにゃんみーまでDMなどでご連絡ください。<br>
Discord: nyanmi-1828#7675<br>
Twitter: @nyanmi_23<br>
<br>
他ゲームのDMでも反応できます。<br>
osu!: nyanmi-1828
## 権利表記
このbotに使用されている画像、ロゴなどは全て©️Cygames inc.に帰属します。
