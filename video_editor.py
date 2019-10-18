from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips

def cut_videos():
    clip = VideoFileClip("vids/ZVv-5xXmhd8.mp4")
    clip.audio.write_audiofile("theaudio.mp3")

    """  with open('timestamps.txt','r') as f:
        nb = 0
        for line in f:
            print(line)
            times = line.split(">")
            start_time = int(times[0]) / 1000
            end_time = int(times[1]) / 1000
            ffmpeg_extract_subclip("vids/ZVv-5xXmhd8.mp4", start_time, end_time, targetname="{}.mp4".format(nb))
            nb = nb + 1 """

#cut_videos()

# clip1 = VideoFileClip("0.mp4")
# clip2 = VideoFileClip("1.mp4")
# clip3 = VideoFileClip("2.mp4")
# clip4 = VideoFileClip("3.mp4")
# final_clip = concatenate_videoclips([clip1,clip2,clip3,clip4])
# final_clip.write_videofile("video.mp4")