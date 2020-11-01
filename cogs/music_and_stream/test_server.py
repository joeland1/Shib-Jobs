import os

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath)
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']

import config
import mpv
import time
import zmq

from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqServerTransport
from tinyrpc.server import RPCServer
from tinyrpc.dispatch import RPCDispatcher

import pywinauto.mouse as mouse
from pywinauto import Application

import youtube_dlc as youtube_dl2
import youtube_dl as youtube_dc

video_player = mpv.MPV(ytdl=False)
app = Application(backend="uia").start(r'C:\Users\joe_land1\AppData\Local\Discord\app-0.0.308\Discord.exe')
#app = Application(backend="uia").connect(path=r'C:\Users\joe_land1\AppData\Local\Discord\app-0.0.308\Discord.exe')

ctx = zmq.Context()
dispatcher = RPCDispatcher()
transport = ZmqServerTransport.create(ctx, 'tcp://127.0.0.1:5001')
rpc_server = RPCServer(transport, JSONRPCProtocol(), dispatcher)

time.sleep(6)

try:
    email = app['Discord'].window(title='Email', control_type='Edit', found_index=0)
    email.type_keys(config.EMAIL)

    email = app['Discord'].window(title='Password', control_type='Edit', found_index=0)
    email.type_keys(config.PW)

    email = app['Discord'].window(title='Login', control_type='Button', found_index=0)
    email.click()

    time.sleep(3)

    try:
        button = app['Discord'].window(title='Quick Question!', found_index=0).window(title='No. Keep this off.', control_type='Button', found_index=0).click()
    except ElementNotFoundError:
        print('cancelled prompt for first popup')

    try:
        button = app['Discord'].window(title='Quick Question!', found_index=0).window(title='No. Keep this off.', control_type='Button', found_index=0).click()
    except ElementNotFoundError:
        print('cancelled prompt for secomd popup')
except:
    print('Could not find login menu -> Means we are logged in')


@dispatcher.public
def play(path_or_link, guild_name):
    while get_youtube_file_download(path_or_link) is False:
        get_youtube_file_download(path_or_link)

    video_player.playlist_append('filler.stream')
    video_player.playlist_pos = 0
    video_player.wait_until_playing()
    video_player.pause=True
    join()
    video_player.pause=False

    if len(video_player.playlist)+1 == len(video_player.playlist):
        video_player.playlist_pos = 0
        video_player.wait_until_playing()
        video_player.pause=True
        video_player.wait_for_property('core-idle')
        join()
        video_player.pause=False

    print('play')

@dispatcher.public
def pause():
    video_player.pause=True

@dispatcher.public
def resume():
    video_player.pause=False

@dispatcher.public
def next_vid():
    video_player.playlist_pos+=1


def join():
    print('joining')
    app['Discord'].set_focus()
    win = app['Discord'].window(title='Servers sidebar', control_type='Group', found_index=0)

    target = win.window(title='Servers', found_index=0).window(title=' self', found_index=0)
    app['Discord'].set_focus()
    mouse.click(coords=(target.rectangle().mid_point()))

    vc = app['Discord'].window(title='self (server)', control_type='Group', found_index=0).window(title_re="General (voice channel)*.", control_type="Button")
    vc.click()

    time.sleep(3)

    app['Discord'].window(title='User area', control_type='Pane', found_index=0).window(title='Share Your Screen', control_type='Button').click()
    screenshare_tab = app['Discord'].window(title='Screen Share', found_index=0)
    screenshare_tab.window(title_re=u'.*- mpv', control_type='Button', found_index=0).click()
    screenshare_tab.window(title='Go Live', control_type='Button', found_index=0).click()

@dispatcher.public
def dc():
    app['Discord'].window(title='User area', control_type='Pane', found_index=0).window(title='Disconnect', found_index=0).click()
    video_player.playlist_clear()
    print('disconnecting')

@video_player.event_callback('end-file')
def check_playlist(event):
    if video_player.playlist_pos==-1:
        print("end of line")
        dc()
    else:
        print("playlistpos= "+str(video_player.playlist_pos))
        print('videos left'+str(len(video_player.playlist)))

def get_youtube_file_download(name):
    for file in os.listdir():
        if file.endswith('.stream'):
            os.remove(file)
    ydl_opts = {
        'format': 'best',
        #'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        #'continuedl': True,
        'outtmpl': 'filler.stream',
        '--verbose': True}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(name, download=True)
        print('download worked with youtube-dl')
    except:
        print('error on try 1, trying again')
        try:
            with youtube_dl2.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(name, download=True)
            print('download worked with youtube-dlc')
        except:
            print('both tries failed, booking it')
            return False
    return True

rpc_server.serve_forever()
