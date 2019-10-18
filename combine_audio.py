from pydub import AudioSegment
import os
from mp3_tagger import MP3File
import moviepy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as mp
from moviepy.editor import VideoFileClip
import time
from convert_time import sec2time

def audio_combiner(added):
    if os.path.isfile('combined_mp3/combined.mp3'):
        sound1 = AudioSegment.from_file('combined_mp3/combined.mp3')
    else:
        sound1 = AudioSegment.empty()
    sound2 = AudioSegment.from_file(added)
    combined = sound1 + sound2
    combined.export("combined_mp3/combined.mp3", format='mp3')

def search_phrase():
    input_ = input("Type your phrase : ")
    print('Your input is {}'.format(input_))
    for word in input_.split():
        path = "mp3_results/{}.mp3".format(word)
        audio_combiner(path)
    video_combiner(input_)

def video_combiner(phrase):
    i = 0
    open('vid_results/list.txt','w').close()
    for word in phrase.split():
        path = "mp3_results/{}.mp3".format(word)
        mp3 = MP3File(path)
        alb = mp3.album[0].value
        times = alb.split(':')
        start = float(times[0]) - 0.06
        dur = float(times[1]) + 0.01
        print("word : {} START : {} // Dur : {}".format(word,start,dur))
        video_path = 'vids/ZVv-5xXmhd8.mp4'
        end = start + dur
        #ffmpeg_extract_subclip(video_path, start, end, targetname="vid_results/{}.mp4".format(i))
        start_time = sec2time(start)
        end_time = sec2time(end) 
        cmd = 'ffmpeg -i {} -ss {} -to {} -async 1 vid_results/{}.mp4'.format(video_path,start_time,end_time,i)
        list_file = open('vid_results/list.txt','a+')
        list_file.write("file '{}.mp4'\n".format(i))
        os.system(cmd)
        i = i + 1
    list_file.close()
    combine_videos()
""" 
    clips = []
    
    for file in os.listdir('vid_results/'):
        print(file)
        if file.endswith('.mp4'):
            clips.append(VideoFileClip('vid_results/{}'.format(file)))

    concat_clip = mp.concatenate_videoclips(clips, method="compose")
    background_music = mp.AudioFileClip("combined_mp3/combined.mp3")
    new_clip = concat_clip.set_audio(background_music)
    new_clip.write_videofile("final_cut.mp4") """
    #concat_clip.write_videofile("combined_vid.mp4")

def combine_videos():
    print(open('vid_results/list.txt','r').read)
    cmd = 'ffmpeg -f concat -safe 0 -i vid_results/list.txt -c copy output.mp4'
    os.system(cmd)


search_phrase()
#combine_videos()
#concat_clip.write_videofile("combined_vid.mp4")