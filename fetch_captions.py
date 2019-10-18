import os
import urllib

def main():
    #os.system('python youtubeChannelVideosFinder.py -k AIzaSyAzIFOCSWqh_0SLH9it1AL8Z4k5septnq8 -c pewdiepie -x 2019-01-10 -y 2018-12-01 -l logf.log -o output.txt')
    get_caption_files()

def getVideoIDs():
    ids_list = []
    with open("output.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
    for line in content:
        ids_list.append(line.split("=",1)[1])
    return ids_list

def fetch_file(lang,videoID,num):
    caption_file = "captions/caption_%s.xml"%(str(num))
    captionURL="http://video.google.com/timedtext?lang=%s&v=%s"%(lang,videoID)
    captionfile = urllib.URLopener()
    captionfile.retrieve(captionURL, caption_file)
    if os.path.getsize(caption_file) == 0:
        if lang=="en":
            lang = "en-US"
        elif lang =="en-US":
            lang = "en-GB"
            fetch_file(lang,videoID,num)



def get_caption_files():
    ids_list = getVideoIDs()
    num = 0
    for id in ids_list:
        lang = "en"
        videoID=id
        fetch_file(lang,videoID,num)
        num = num + 1
    return num

if __name__ == '__main__':
    main()
