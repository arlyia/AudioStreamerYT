#Script requires appropriate version of VLC to be installed based on Python implemention either 32 bit or 64 bit
#IF IT DOES NOT MATCH YOU WILL GET AN ERROR

import pafy
import vlc
import asyncio

global player
#set vlc and vlc player instance
vlcInstance = vlc.Instance("--input-repeat=-1", "--fullscreen")
player = vlcInstance.media_player_new()

#core of the script - get a YouTube URL and get the downlink link for VLC to play
def core():
    #get url from user
    url = input("Insert a youtube url:\t")
    #try to create url, if incorrect alert the user and quit, otherwise print video information
    try:
        video = pafy.new(url)
    except ValueError:
        print (ValueError)
    else:
        print ("Getting video %s, which is %s long\n" % (video.title, video.duration))

    #get the best audio bitrate and format available then print it to the console
    bestaudio = video.getbestaudio()
    print ("Best available audio format is %sbps %s \n" % (bestaudio.bitrate, bestaudio.extension))
    #default audio volume is 40% as 100% can be very loud
    player.audio_set_volume(40)
    #set media to the previous audio url
    media = vlcInstance.media_new(bestaudio.url)
    player.set_media(media)

#run the core of the script and play the audio, setting playing to True allows the loop below
core()
player.play()
playing = True

#provides menu functions so requires looping
while playing == True:
    #if the player stops playing and can't continue, stop and alert the user
    if player.will_play == 0:
        player.stop()
        print ("Audio has ended, please add more links")
    #menu string to print to user
    choice = input("Pause/resume the audio with p, stop with s\nvolume is %s : change with v(0-100) eg v40\nN for a new video\nC to stop running\nt to change time t(time in s) or t0 to get current time eg t20\n\n" % (player.audio_get_volume()))
    #deals with a pause/resume request, pauses or resumes audio playback
    if choice == "p":
        player.pause()
        choice = ""
    #deals with stop request, stops playback entirely
    elif choice == 's':
        player.stop()
    #deals with volume request, v(int between 0-100) sets the volume level for audio playback
    elif choice[0] == 'v':
        val = choice[1:]
        vol = int(val)
        player.audio_set_volume(vol)
    #deals with new link request, if audio is playing stops it and asks for the new link
    elif choice == 'n':
        if player.is_playing == 1:
            player.stop()
        core()
        player.play()
    #deals with time request, t0 gets the current time and t(int) sets the new time
    elif choice[0] == 't':
        if len(choice) == 2 and choice[1] == "0":
            currentTime = player.get_time() / 1000
            print("Current time: %d s\n" % (currentTime))
        else:
            val = choice[1:]
            val = int(val)
            newTime = val * 1000
            player.set_time(newTime)
    #deals with cancel request, stops playback and sets playing to False which ends the loop and program
    elif choice == 'c':
        player.stop()
        playing = False
    #user has input an option not given to them, admirable but not useful
    else:
        "Invalid choice"