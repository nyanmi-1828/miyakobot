from discord.ext import commands,tasks
import discord
import traceback
import os
import io
import asyncio
import pytz
import csv
import math
import dropbox
import string
import cv2
from docopt import docopt
import glob
import logging
import sys
from PIL import Image
import numpy as np
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

dbxtoken = os.environ['dbxtoken']
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
dbx.files_download_to_file('./src/miyakobot-spreadsheet.json', '/miyakobot/miyakobot-spreadsheet-f0f4058290d2.json', rev=None)
credentials = ServiceAccountCredentials.from_json_keyfile_name('./src/miyakobot-spreadsheet.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = os.environ['SpreadSheet2']
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

class Imagehashmanager(object):
    """
    imageハッシュ同士の比較や辞書のキーに使える
    """
    
    def __init__(self, binary_array: np.ndarray):
        self.hash = binary_array
    
    def __str__(self):
        return _binary_array_to_hex(self.hash.flatten())
    
    def __repr__(self):
        return repr(self.hash)
    
    def __sub__(self, other):
        if other is None:
            raise TypeError('Other hash must not be None.')
        if isinstance(other, Imagehashmanager):
            if self.hash.size != other.hash.size:
                raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.hash.shape)
            return np.count_nonzero(self.hash.flatten() != other.hash.flatten())
        elif isinstance(other, np.ndarray):
            if self.hash.size != other.size:
                raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.shape)
            return np.count_nonzero(self.hash.flatten() != other.flatten())
        else:
            raise TypeError(f'Other Invalid type:{type(other)}')
    
    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Imagehashmanager):
            return np.array_equal(self.hash.flatten(), other.hash.flatten())
        elif isinstance(other, np.ndarray):
            return np.array_equal(self.hash.flatten(), other.flatten())
        else:
            raise TypeError(f'Other Invalid type:{type(other)}')
    
    def __ne__(self, other):
        if other is None:
            return False
        if not isinstance(other, Imagehashmanager):
            return not np.array_equal(self.hash.flatten(), other)
        else:
            return not np.array_equal(self.hash.flatten(), other.hash.flatten())
    
    def __hash__(self):
        # this returns a 8 bit integer, intentionally shortening the information
        return sum([2 ** (i % 8) for i, v in enumerate(self.hash.flatten()) if v])
        # long ver
        # return sum([2 ** i for (i, v) in enumerate(self.hash.flatten()) if v])
        
def dhash(image: np.ndarray, hashsize: int = 8):
    """
    8x8 = 64[bit]
    Difference Hash computation.
    following http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

    computes differences horizontally
    """
    assert image.shape[-1] in (1, 3)  # グレイスケールまたはRGBではない場合エラー、下のコードでもよい
    #     raise RuntimeError(f"Unknown format: shape={image.shape}")
    if hashsize < 2:
        raise ValueError("Hash size must be greater than or equal to 2")
    img = cv2.resize(image, (hashsize + 1, hashsize), interpolation=cv2.INTER_AREA)  # リサイズ
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if image.shape[2] == 3 else img  # 上の行と順番逆でもいいかも
    
    resized = np.asarray(img)
    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]
    
    # 念の為
    diff = np.asarray(diff, dtype=bool)
    return Imagehashmanager(diff)

class Arena_recognation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.arena_chara_list = []
        self.im = None
    
    # 値から辞書型リストのキーを取得
    def get_keys_from_value(self,d, val):
        return [k for k, v in d.items() if v == val]

    # 各キャラ画像切り抜き
    def cropping(self,x1,y1,x2,y2,name):
        img_size = (66, 64)
        im_crop = self.im.crop((x1, y1, x2, y2))
        img_path = 'data/crop/arena_pillow_crop_' + name + '.jpg'
        im_crop.save(img_path, quality=95)

        img = cv2.imread(img_path)
        img = cv2.resize(img,img_size)
        cv2.imwrite(img_path,img)

    # 画像認識
    def image_check(self,file_path):

        hash_list = []
        pattern = '%s/*.jpg'
        comparing_dir_path = './data/save/'
        comparing_files = glob.glob(pattern % (comparing_dir_path))
        for comparing_file in comparing_files:
            img = cv2.imread(comparing_file)
            hash = dhash(img)
            hash_list.append(hash)
        printname = ''
        # get parameters
        target_file_path = './data/crop/arena_pillow_crop_' + file_path + '.jpg'

        # setting
        img_size = (66, 64)

        # read target image
        target_img = cv2.imread(target_file_path)
        target_img = cv2.resize(target_img, img_size)

        hash = dhash(target_img)
        min_hash_list = [hash_list[i] - hash for i in range(len(hash_list))]
        for i in range(len(hash_list)):
            if min_hash_list[i] == min(min_hash_list):
                printname = comparing_files[i].replace('./data/save\\', '').replace('.jpg', '')

        self.arena_chara_list += printname

    # 複数の要素番号を取得
    def my_index_multi(self,l, x):
        return [i for i, _x in enumerate(l) if _x == x]

    # botのコマンド部分
    @commands.command()
    async def arena(self,ctx):
        # -------------------各種データ-------------------
        size_list = {
                'iPhoneXr':{'y1':238, 'y2':302, 'x':[[1168,1234],[1238,1304],[1308,1374],[1379,1445],[1448,1517]]}, \
                'xperia':{'y1':436, 'y2':556, 'x':[[1939,2060],[2067,2190],[2197,2318],[2327,2448],[2456,2576]]},\
                'Widescreen':{'y1':327, 'y2':416, 'x':[[1335,1424],[1431,1522],[1528,1618],[1625,1715],[1722,1811]]},\
                'iPad':{'y1':541, 'y2':636, 'x':[[1424,1519],[1527,1623],[1631,1726],[1733,1828],[1837,1932]]}
            }
        
        # 画像比率分析用
        Xr = round(1792/828, 2)
        iPhone11 = round(2436/1125, 2)
        Widescreen = round(1920/1080, 2)
        iPad = round(2048/1536, 2)
        img_shape_list = {'iPhoneXr': Xr, 'iPhoneXr': iPhone11, 'xperia': 2, 'Widescreen': Widescreen, 'iPad': iPad}
        width_list = {'iPhoneXr': 1792, 'xperia': 2880, 'Widescreen': 1920, 'iPad': 2048}
        # -------------------各種データ-------------------
        
        img_path = "data/image/arena_test.jpg"
        channel = ctx.message.channel
        await ctx.send("画像を送ってなの～")
        
        # 画像が送られてくるまで待つ
        def check(msg):
            return msg.author == ctx.message.author and msg.attachments

        receive_msg = await ctx.bot.wait_for('message',check=check)
        await receive_msg.attachments[0].save(img_path)

        img = cv2.imread(img_path)
        img_height,img_width,_ = img.shape

        # 読み込んだ画像の比率
        img_shape = round(img_width/img_height, 2)

        # 比率から機種を判別
        keys_list = self.get_keys_from_value(img_shape_list, img_shape)

        try:
            keys = keys_list[0]
        except IndexError:
            await ctx.send("画像が対応してない比率なの…")
            return

        # 多解像度対応用に変換
        try:
            resize_width = width_list[keys]
        except UnboundLocalError:
            await ctx.send("画像が対応してない比率なの…")
            return
        resize_height = resize_width / img_width * img_height
        img = cv2.resize(img,(int(resize_width),int(resize_height)))
        cv2.imwrite(img_path,img)

        self.im = Image.open('data/image/arena_test.jpg')
        y1 = size_list[keys]['y1']
        y2 = size_list[keys]['y2']
        x = size_list[keys]['x']
        
        self.cropping(x[0][0],y1,x[0][1],y2,"p1")
        self.cropping(x[1][0],y1,x[1][1],y2,"p2")
        self.cropping(x[2][0],y1,x[2][1],y2,"p3")
        self.cropping(x[3][0],y1,x[3][1],y2,"p4")
        self.cropping(x[4][0],y1,x[4][1],y2,"p5")

        for i in ["p1","p2","p3","p4","p5"]:
            self.image_check(i)

        chara_list = {
                'aoi':'アオイ','hiyori':'ヒヨリ','io':'イオ','kaori_summer':'水着カオリ','kasumi_magical':'カスミ（マジカル）',\
                'kokkoro':'コッコロ','kurumi':'クルミ','kuuka':'クウカ','kyaru':'キャル','maho':'マホ',\
                'nozomi_christmas':'ノゾミ（クリスマス）','pecorine':'ペコリーヌ','pecorine_summer':'水着ペコリーヌ',\
                'rei_newyear':'正月レイ','rima':'リマ','rino':'リノ','saren_summer':'水着サレン',\
                'shinobu_halloween':'シノブ（ハロウィン）','tsumugi':'ツムギ','yukari':'ユカリ','yuki':'ユキ',\
                'tamaki':'タマキ','rin_deremas':'リン（デレマス）','pecorine_princess':'ペコリーヌ（プリンセス）','yui':'ユイ',\
                'runa':'ルナ','hatsune':'ハツネ','kokkoro_princess':'コッコロ（プリンセス）','mifuyu':'ミフユ','yuni':'ユニ',\
                'kuuka_ooedo':'クウカ（オーエド）','ruka':'ルカ','rin':'リン','ayumi':'アユミ'
            }
        # 出力、判定用にまとめ
        chara_l = [chara_list[n] for n in self.arena_chara_list]
        chara_output = '、'.join(chara_l)

        # シートから編成を取得
        attackers = worksheet.col_values(1)
        defenders = worksheet.col_values(2)
        attack_index = self.my_index_multi(defenders, chara_output)

        # 取得した編成を一つにまとめる
        chara_counter = [attackers[attack_index[l]] for l in range(len(attack_index))]
        chara_counter_output = '\n'.join(chara_counter)

        if len(attack_index) == 0:
            await ctx.send(f"```{chara_output}``` に勝てる編成が見つからなかったの…")
        else:
            await ctx.send(f'```{chara_output}``` に勝てそうな編成が{len(attack_index)} つ見つかったの！```{chara_counter_output}``` で勝てると思うの！')

        self.arena_chara_list.clear()
        chara_output = None
        
def setup(bot):
    bot.add_cog(Arena_recognation(bot))