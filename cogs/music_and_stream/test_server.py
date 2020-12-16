import os

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath)
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']

import sqlite3

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

#try force window
import youtube_dlc as youtube_dl2
import youtube_dl as youtube_dl
import ffmpeg


video_player = mpv.MPV(ytdl=False)
video_player.force_window='yes'
#video_player.idle='yes'
app = Application(backend="uia").start(r'C:\Users\joe_land1\AppData\Local\Discord\app-0.0.308\Discord.exe')
#app = Application(backend="uia").connect(path=r'C:\Users\joe_land1\AppData\Local\Discord\app-0.0.308\Discord.exe')

ctx = zmq.Context()
dispatcher = RPCDispatcher()
transport = ZmqServerTransport.create(ctx, 'tcp://127.0.0.1:5001')
rpc_server = RPCServer(transport, JSONRPCProtocol(), dispatcher)

playlist=[]
current_resolution=None
time.sleep(2)

try:
    conn=sqlite3.connect('stream_server.db')
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM LOGIN_STUFF")
    login_creds = cursor.fetchone()

    email = app['Discord'].window(title='Email', control_type='Edit', found_index=0)
    email.type_keys(login_creds[0])

    email = app['Discord'].window(title='Password', control_type='Edit', found_index=0)
    email.type_keys(login_creds[1])

    cursor.close()
    conn.close()

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
def play(path_or_link, guild_name, voice_name):

    if len(playlist) == 0:
        playlist.append((path_or_link, 1))
        if get_youtube_file_download((path_or_link, 1)) is False:
            print('it aint worked')
        print(playlist)

        video_player.playlist_append('1.stream')
        print(video_player.playlist)
        video_player.pause=True
        video_player.playlist_pos=0
        video_data=ffmpeg.probe('1.stream')
        current_resolution=(video_data['streams'][0]["height"], video_data['streams'][0]["width"])
        join(guild_name, voice_name)
        video_player.pause=False
        print('join play ran')


    else:
        name = playlist[len(playlist)-1][1]+1
        playlist.append((path_or_link, name   ))
        print('add play ran')

@dispatcher.public
def pause():
    video_player.pause=True

@dispatcher.public
def resume():
    video_player.pause=False

@dispatcher.public
def next_vid():
    #check_playlist function runs when this happens
    video_player.seek('+'+str(video_player.time_remaining))

def join(guild_name, voice_name):
    print('joining')
    app['Discord'].set_focus()
    win = app['Discord'].window(title='Servers sidebar', control_type='Group', found_index=0)
    app['Discord'].set_focus()
    #target = win.window(title='Servers', found_index=0).child_window(title=' self',control_type='TreeItem', found_index=0).parent()
    mouse.click(coords=(win.window(title='Servers', found_index=0).descendants(control_type='Image')[0].rectangle().mid_point()))
    app['Discord'].window(title=guild_name+' (server)', control_type='Group', found_index=0).window(title_re=voice_name+" (voice channel)*.", control_type="Button").click()

    time.sleep(3)

    app['Discord'].window(title='User area', control_type='Pane', found_index=0).window(title='Share Your Screen', control_type='Button').click()
    screenshare_tab = app['Discord'].window(title='Screen Share', found_index=0)
    got_mpv_button = False

    #this should work but i havent been able to test it, implemented for redundancy anyway
    while got_mpv_button is False:
        try:
            mpv_application_selector_button = screenshare_tab.window(title_re='.*- mpv', control_type='Button', found_index=0).click()
            got_mpv_button = True
            print('set true')
        except:
            app['Discord'].set_focus()
            mouse.scroll(coords=app['Discord'].rectangle().mid_point(), wheel_dist = 1)

    screenshare_tab.window(title='Go Live', control_type='Button', found_index=0).click()

@dispatcher.public
def dc():
    app['Discord'].window(title='User area', control_type='Pane', found_index=0).window(title='Disconnect', found_index=0).click()
    video_player.playlist_clear()
    print('disconnecting')

@video_player.event_callback('end-file')
def check_playlist(event):
    print('check_plyalist')
    del playlist[0]
    print(playlist)
    print('del')

    if len(playlist)==0:
        print("end of line")
        app['Discord'].window(title='User area', control_type='Pane', found_index=0).window(title='Disconnect', found_index=0).click()
        video_player.playlist_clear()
        print('disconnecting')
    else:
        while get_youtube_file_download(playlist[0]) is False:
            del playlist[0]
            print('could not get this one, getting next video')

            if len(playlist) == 0:
                print('deleted last item, quitting now')
                dc()
                return

        #cant use .play -> doesnt keep window
        video_player.playlist_pos=-1
        #get_youtube_file_download(playlist[0])
        video_player.playlist_append(str(playlist[0][1])+'.stream')
        print(video_player.playlist)
        video_player.playlist_remove(0)
        video_player.pause=True
        video_player.playlist_pos=0
        video_player.pause=False


def get_youtube_file_download(url):
    for file in os.listdir():
        if file == str(url[1])+'.stream':
            os.remove(file)
    print(url[0])
    ydl_opts = {
        'format': 'best',
        #'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        #'continuedl': True,
        'outtmpl': str(url[1])+'.stream',
        '--verbose': True}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url[0], download=True)
        print('download worked with youtube-dl')
    except:
        print('error on youtube-dl, trying again')
        try:
            with youtube_dl2.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url[0], download=True)
            print('download worked with youtube-dlc')
        except:
            print('both tries failed, booking it')
            return False
    return True

rpc_server.serve_forever()
