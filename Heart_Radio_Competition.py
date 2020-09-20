# Must be updated here, I believe the new API doesn't allow this to work
from bs4 import BeautifulSoup
import time
import requests
from pushbullet import Pushbullet
from pushbullet import Listener


# Your Pushbullet API Key
pb = Pushbullet("*******")


# Target Device Name
device = pb.get_device('*******')




def get_artist_name():
    page = requests.get("https://www.heart.co.uk/berkshire/")
    soup = BeautifulSoup(page.content, 'html.parser')
    artist_info=soup.find('span', itemprop="byArtist").find_all(text=True, recursive=False)
    current_artist_name=(artist_info[0].strip())
    return current_artist_name

def pushMessage(device,msg):
    pushTitle = "Heart Radio Notification"
    push = device.push_note(pushTitle, msg)
    print("Message was sent!")

def contest_artist_name():
    page = requests.get("https://www.heart.co.uk/radio/win-with-hearts-30k-triple-play/")
    soup = BeautifulSoup(page.content, 'html.parser')
    contest_artist_info=soup.title.string
    artist_name_split= contest_artist_info.split(' is now Heart')
    contest_artist_name=artist_name_split[0]
    return contest_artist_name

#******************   MAIN  *********************************

starttime=time.time()
while True:
    current_artist=get_artist_name()
    contest_artist=contest_artist_name()
    if current_artist == contest_artist:
        message_text='Contest artist= ' + contest_artist + ", Current artist= "+current_artist
        pushMessage(device, message_text)
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
