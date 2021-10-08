import argparse
import discord
from discord import player
from discord.errors import ClientException
import youtube_dl
from youtube_dl import YoutubeDL
import os
import asyncio

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import _Response, Request

from collections import defaultdict, deque

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
TOKEN = "" #TOKENを入力

client = discord.Client()
count_music = 1
elect = 0
tit = []
youtube_url = ""
voice = None
playerr = None
url = 0
qloo = 0
loop = 0
ended = 0
queue_dict = deque()
t = 0
videde = []
titl = [] 
sss = ""
meme = None
print_title = 0
queue_title = 0
loopskip = 0


#キューの設定
def enqueue(voice_client, youtube_ur):

    queue = queue_dict
    queue.append(youtube_ur)
    print(queue)
    
    if not voice_client.is_playing():
        ytl(queue)
    else:
      return


#googleのapiを使ってyoutubeの動画を検索する
def youtube_search(options):
  global videde,tit
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = [] #リストを作成
  playlists = []
  
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videde.append(search_result["id"]["videoId"])
      tit.append(search_result["snippet"]["title"])
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["videoId"]))

  print("Videos:\n", "\n".join(videos), "\n")
  print("Channels:\n", "\n".join(channels), "\n")
  print("Playlists:\n", "\n".join(playlists), "\n")
  print(search_result)
 
  
  #vcで流すためにvideoIDを取得
  print (videde)

#youtubeで検索するための設定。.scで来たワードを入れる
def youtudeop():
  global videde
  # 検索ワード
  argparser = argparse.ArgumentParser()
  argparser.add_argument("--q")
  # 検索上限
  argparser.add_argument("--max-results", help="Max results", default=5)
  args = argparser.parse_args()
  args.q = sss
  
  try:
    youtube_search(args)
    print(videde)

    
  
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))



#URLでyoutubeに飛んで、ダウンロード&再生。
def ytl(que):
  ai = que[0]
  global voice,t,ended,titl,meme,loop,loopskip
  if ai[24:40] == "playlist":
    return
  else:   
    
    if ended != loopskip: 
      youtube_dl.utils.bug_reports_message = lambda: ''
      print(que)
      ydl_opts = {
        'options': "-vn -socket-timeout 5 --keep-video",
        'format': 'bestaudio/webm/m4a',
        'outtmpl':  f"vc_music_{ended}" + '.%(ext)s'
      }
      ydl = youtube_dl.YoutubeDL(ydl_opts)
      count = 0
      try:
        info_dict = ydl.extract_info(que[0], download=True) 
        for a in range(-1):
          print(count)
          if info_dict != None:
            break
          count = count +1

      except Exception as e: 
        print(e.__class__.__name__, e)
        raise
      titl.append(info_dict.get("title" ,None))
      
    if voice != None:
        if loop == 0:
          if ended >= 1:
            j = ended -1
            if os.path.isfile(f"vc_music_{j}.m4a") == True:
              os.remove(f"vc_music_{j}.m4a")
            elif os.path.isfile(f"vc_music_{j}.webm") == True:
              os.remove(f"vc_music_{j}.webm")
        if os.path.isfile(f"vc_music_{ended}.m4a") == True:
            try:
              voice.play(discord.FFmpegPCMAudio(f"vc_music_{ended}"+".m4a"), after=lambda e : ende(que))
            except ClientException:
              voice = None
              voice = meme.author.voice.channel.connect(reconnect = True)
              ytl(que)

        elif os.path.isfile(f"vc_music_{ended}.webm") == True:
            try:
              voice.play(discord.FFmpegPCMAudio(f"vc_music_{ended}"+".webm"), after=lambda e : ende(que))
            except ClientException:
              voice = None
              voice = meme.author.voice.channel.connect(reconnect = True)
              ytl(que)
        else:
            return
        
#終了後にqueueの先頭を削除
def ende(queu):
  print("done")
  print(queu)
  global ended,qloo,loop
  if loop == 0:
    ended = ended + 1
  if qloo == 0 and loop == 0:
    if len(queu) >= 2:  
      queu.popleft()
      ytl(queu)
    elif len(queu) == 1:
      queu.popleft()
      print(queu)
      return
    else:
      return

  elif qloo == 1 and loop == 0:
    queu.append(queu[0])
    queu.popleft()
    if len(queu) >= 1 :
        ytl(queu)
  elif loop == 1:
    ytl(queu)
  else:
    return


#ここからdiscord
@client.event #起動が完了するとコンソールにhiと送り、プレイ中の表示をさせる
async def on_ready():
    print("hi")
    await client.change_presence(activity=discord.Game(name="hi", type=1))
    await client.change_presence(activity=discord.Game(name="i'm listening to music now!", type=1))
@client.event
async def on_voice_state_update(member, before, after):
  global voice,ended,qloo,loop,meme
  if voice != None:
    cout = 0
    tes = []
    for i in voice.channel.members:
      tes.append(i)
      cout = cout + 1
      print (cout)
    print(tes)
    if cout == 1:
      qloo = 0
      loop = 0
      queue_dict.clear()
      if voice.is_playing():
        voice.stop()
      await voice.disconnect()
      voice = None
      
      j = 0
      async with meme.channel.typing():
        await asyncio.sleep(0.7)
        for j in range(ended +1):
          if os.path.isfile(f"vc_music_{j}.m4a") == True:
            os.remove(f"vc_music_{j}.m4a")
          elif os.path.isfile(f"vc_music_{j}.webm") == True:
            os.remove(f"vc_music_{j}.webm")
        await meme.channel.send("good bye!")
        ended = 0

  elif voice == None:
    return
@client.event
async def on_message(message): #メッセージの確認
    
    global voice,player,youtube_url,url,sss,argparser,videde,queue_dict,ended,qloo,loop,tit,elect,meme,print_title,queue_title,count_music,loopskip
    meme = message
    msg = message.content
  
    
    if message.author.bot: #botの場合反応しない
        return

    if elect == 1:
      if msg.isdecimal() == False:
        return
      inmsg = int(msg) #検索した候補を選ぶ
      if inmsg <= count_music:
        q = f"https://www.youtube.com/watch?v={videde[inmsg-1]}"
        enqueue(voice ,q)
        async with message.channel.typing():
          await asyncio.sleep(2)
          if print_title == 0:
            await message.channel.send("キューに追加: "+tit[inmsg-1])
          elif print_title == 1:
            await message.channel.send("キューに追加: "+q)
      videde = []
      tit = []
      elect = 0

    if msg == ".move": #vcを移動する
      await voice.move_to(message.author.voice.channel)
    
    if msg == ".clear": #キューをクリア
      async with message.channel.typing():
        await asyncio.sleep(1)
        await message.channel.send("キューをリセットしました.")
      queue_dict.clear()
    
    if msg == ".pr_title": #検索時にタイトルのみにする
      if print_title == 0:
        print_title = 1
        await message.channel.send("検索時にタイトルのみ表示します。")
      elif print_title == 1:
        print_title = 0
        await message.channel.send("検索時にURLも表示します。")

    if msg == "!debug":
      name = [m.name for m in message.author.voice.channel.members]
      await message.channel.send(name)

    if msg == ".info": #botの情報
      await message.channel.send("This bot made by kakigoori(2021) \n\n You can listen to music to use this bot. \n\n This bot is happened to occur an error or to slow down download.")

    if msg == ".help": #botのコマンド
      await message.channel.send("```.help :このメッセージを表示します。\n.play <URL>,<word> :URLでその曲、wordで検索して、流します。\n.sc <word> :wordをyoutube検索して、5個の候補を表示します。\n.q :キューの中身を表示します(ログが流れます)。\n.skip :流れている曲をスキップします。\n.clear :キューをリセットします。\n.dc :botをvcから切断させます。\n.move :vcを移動させます。\n.queueloop :キューをループさせます。\n.loop :一曲のみをループします。(queueloopよりも早いです)\n.pr_title :検索時にタイトルのみを表示します。\n.info :botの情報を表示します\n```")
    
    if msg == ".dc": #切断
      qloo = 0
      loop = 0
      queue_dict.clear()
      if voice.is_playing():
        voice.stop()

      #guild = message.guild.voice_client
      await voice.disconnect()
      voice = None
      
      j = 0
      async with message.channel.typing():
        await asyncio.sleep(0.7)
        for j in range(ended +1):
          if os.path.isfile(f"vc_music_{j}.m4a") == True:
            os.remove(f"vc_music_{j}.m4a")
          elif os.path.isfile(f"vc_music_{j}.webm") == True:
            os.remove(f"vc_music_{j}.webm")
        await message.channel.send("good bye!")
        ended = 0

   # if msg == ".q_title":
      #if queue_title == 0:
      #  queue_title = 1
      #  await message.channel.send("キューの表示時にタイトルのみ表示します。")
     # elif queue_title == 1:
      #  queue_title  = 0
      #  await message.channel.send("キューの表示時にURLも表示します。")


    if msg == ".q": #キューの中身を表示させる。デザインを変えたいね.
     # if queue_title == 0:
      count_music = 1
      for spt in queue_dict:
        await message.channel.send(str(count_music)+":"+spt)
        count_music = count_music + 1
      if qloo == 1:
        await message.channel.send("queueloop: \N{Heavy Large Circle}")
      elif qloo == 0:
        await message.channel.send("queueloop: \N{Cross Mark}")
      if loop == 1:
        await message.channel.send("loop: \N{Heavy Large Circle}")
      if loop == 0:
        await message.channel.send("loop : \N{Cross Mark}")

    if msg == ".skip": #流れている曲をスキップ。stopするだけで、曲が終了したときの処理が起こる
      if loop == 1:
        loopskip = ended
        ended = ended + 1
      voice.stop()
      if loop == 1:
        j = ended -1
        if os.path.isfile(f"vc_music_{j}.m4a") == True:
          os.remove(f"vc_music_{j}.m4a")
        elif os.path.isfile(f"vc_music_{j}.webm") == True:
          os.remove(f"vc_music_{j}.webm")

    if msg== ".loop": #一曲のみのloopをon,offする
      if loop == 0:
        loop = 1
        await message.channel.send("loopがonになりました")
      elif loop == 1:
        loop = 0
        await message.channel.send("loopがoffになりました")


    if msg == ".queueloop": #queueloopをon,offする。
      if qloo == 0:
        qloo = 1
        await message.channel.send("queueloopがonになりました")
      elif qloo == 1:
        qloo = 0
        await message.channel.send("queueloopがoffになりました")

    if msg[:3] == ".sc": #検索する。動画idを取得して、youtubeのURLの後にくっつけてるだけ
      tit = []
      videde = []
      if message.author.voice is None:
        await message.channel.send("ボイスチャットに参加してください.")
        return
      sss = msg[4:]
      youtudeop()
      #youtube_url = f"https://www.youtube.com/watch?v={videde}"
      if voice == None:
        voice = await message.author.voice.channel.connect(recconect = True)
      elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別

          await voice.move_to(message.author.voice.channel)

      count_music = 1
      if print_title == 0:
            for spt in videde:
              await message.channel.send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
      elif print_title == 1:
            for spt in tit:
              await message.channel.send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(tit) + 1:
                break
      await message.channel.send("流したい曲の番号を送信してください(.無し)")
      elect = 1
      #enqueue(voice,youtube_url)
      
      
    if msg[:5] == ".play": #指定されたURLの曲を流す。
        if msg[6:14] == "https://": #youtubeのURLかを判別。
            youtube_url = msg[6:]
        
        
            if message.author.voice is None:
                await message.channel.send("ボイスチャットに参加してください.")
                return

            if voice == None:
             voice = await message.author.voice.channel.connect(reconnect = True)
            

            elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id:
             
                await voice.move_to(message.author.voice.channel)

            enqueue(voice,youtube_url)
            async with message.channel.typing():
              await asyncio.sleep(2)
              await message.channel.send("正常に追加されました")


        else:
          videde =[]
          tit = []
          if message.author.voice is None:
            await message.channel.send("ボイスチャットに参加してください.")
            return
          sss = msg[4:]
          youtudeop()
         #youtube_url = f"https://www.youtube.com/watch?v={videde}"
          if voice == None:
            voice = await message.author.voice.channel.connect(reconnect = True)
          elif message.author.voice is not None and message.guild.me not in message.author.voice.channel.members and message.guild.id == voice.guild.id: #サーバーと、ボイスチャンネルを判別

            await voice.move_to(message.author.voice.channel)

          count_music = 1
          if print_title == 0:
            for spt in videde:
              await message.channel.send(str(count_music)+": https://www.youtube.com/watch?v="+spt)
              count_music = count_music + 1
              if count_music == len(videde) + 1:
                break
          elif print_title == 1:
            for spt in tit:
              await message.channel.send(str(count_music)+": "+spt)
              count_music = count_music + 1
              if count_music == len(tit) + 1:
                break
          await message.channel.send("流したい曲の番号を送信してください(.無し)")  
          elect = 1
          #enqueue(voice,youtube_url)
      
if __name__ == '__main__':
  client.run(TOKEN)

#やりたいことリスト
#
#プレイリスト(現在無効) →頭の中ではだいたい構想が作れてるけど、どう作るか考え中
#
#
#
#
#
#
#
