import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import html
import string
import re
import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

def write_tags(path_to_mp3,s,d):
    # Create MP3File instance.
    mp3 = MP3File(path_to_mp3)
    # Get/set/del tags value.
    mp3.album = '{}:{}'.format(s,d)
    mp3.save()
    

def to_parseable(tree):
    t = ET.tostring(tree)
    t = t.lower()
    return ET.fromstring(t)

def check_word(output,start,dur):
    caption_file = open("new_captions/new_caption_0.xml")
    try:
        e = ET.parse(caption_file)
    except Exception as e:
        print("Error")
    root = e.getroot()
    e = to_parseable(root)
    start = start / 1000
    dur = dur / 1000
    output = output.replace(" ","")
    for text in e.findall('text'):
        start_element = float(text.get('start')) # equivalent to .attrib() in this case
        dur_element = float(text.get('dur'))
        flavor_text = text.text
        end_element = start_element + dur_element
        if (end_element + 2) > start > (start_element - 2):
            if output in flavor_text:
                return True
            else: 
                return False
    return False

def xml_to_auido():
    caption_file = open("auto_captions/auto_caption_0.xml","r")
    try:
        e = ET.parse(caption_file)
    except Exception as e:
        print("Error")
    root = e.getroot()
    e = to_parseable(root)
    
    for p in e.findall('.//p'):
        if p.get('a') != 1:
            time = p.get('t')
            time = int(time)
            start_time = time
            end_time = start_time
            word = ''
            for elem in p.getiterator():
                if elem.tag == 's':
                    end_time = int(start_time) + int(elem.attrib.get('ac'))
                    dur = end_time - start_time
                    if elem.attrib.get('t'):
                        end_time = int(elem.attrib.get('t')) + time
                        dur = end_time - start_time 
                        #print("{} = {} - {}".format(dur,start_time,end_time))
                        output = 'mp3_results/{}.mp3'.format(word)
                        time_sec = (start_time + 100) / 1000
                        dur_sec = (dur+80) / 1000
                        cmd = ('sox theaudio.mp3 {} trim {} {}'.format(output,time_sec,dur_sec))
                        if(check_word(word,start_time,dur)):
                            os.system(cmd)
                            write_tags(output,time_sec,dur_sec)
                            #here add metadata
                            print('Word : {} \\ Start: {} \\ Dur: {}\n.'.format(word,start_time,dur))
                        else:
                            print('Passed on {}'.format(output))
                        #do shit here
                        word = elem.text
                        word = word.replace(" ","")
                        start_time = int(time) + int(elem.attrib.get('t'))
                    else:
                        word = elem.text
                        start_time = time

                    

            
       

def strip_captions(caption_name):
    caption_file = open(caption_name,'r')
    try:
        e = ET.parse(caption_file)
    except Exception as e:
        print("Error")
    root = e.getroot()
    e = to_parseable(root)
    new_caption_file = open("new_captions/new_caption_0.xml",'a+')
    new_caption_file.write('<?xml version="1.0" encoding="utf-8" ?>\n <transcript>\n')
    for text in e.findall('text'):
        start_element = text.get('start') # equivalent to .attrib() in this case
        dur_element = text.get('dur')
        flavor = text.text
        #info_list = []
        if isinstance(flavor, str):
            flavor = html.unescape(flavor)
            translator=str.maketrans('','',string.punctuation)
            pun_flavor = flavor
            pun_flavor = re.sub(r'\*.*?\*','',pun_flavor)
            pun_flavor = re.sub(r'\([^)]*\)', '', pun_flavor)
            pun_flavor = re.sub(r'\{.*?\}','',pun_flavor)
            pun_flavor = re.sub(r'\[.*?\]','',pun_flavor)
            pun_flavor = re.sub(r'\-.*?\-','',pun_flavor)
            pun_flavor = pun_flavor.replace('"',"'")
            pun_flavor = pun_flavor.replace("  "," ")
            flavor = pun_flavor
            #
            #print(pun_flavor)
            #print(re.sub(r'\([^)]*\)', '', flavor))
            
            flavor=flavor.translate(translator)
            flavor = html.unescape(flavor)
            if flavor.startswith(" "):
                flavor = flavor[1:]
            if flavor.endswith(" "):
                flavor = flavor[:-1]
            if flavor and flavor != " " and flavor !="\n" and flavor != " \n":
                line_str = '<text start="{}" dur="{}">{}</text>'.format(start_element,dur_element,flavor)
                new_caption_file.write(line_str)
    new_caption_file.write("</transcript>")
    new_caption_file.close()        


def get_exact_time(sub_time,word_to_look):
    caption_file = open("auto_captions/auto_caption_0.xml","r")
    print("SUB: ",sub_time)
    try:
        e = ET.parse(caption_file)
    except Exception as e:
        print("Error")
    root = e.getroot()
    e = to_parseable(root)
    #sub_time = 71150
    #word_to_look = "Goddamnit"
    #translator=str.maketrans('','',string.punctuation)
    #filename = "empty.txt"
    closest_nb = 0
    start_time = 0
    end_time = 0
    for text in e.findall('.//p'):
        time = text.get('t')
        if text.get('a') != "1":
            if (sub_time - 1500) <= int(time) <= (sub_time + 1500):
                nb = sub_time - int(time)
                dif = sub_time - closest_nb
                if abs(nb) < abs(dif):
                    closest_nb = int(time)

    for t in e.findall('.//p'):
        time = t.get('t')
        if int(time) == closest_nb:
            start_time = closest_nb
            end_time = closest_nb
            first_time = False
            st_ending = 0
            last_used = False
            for elem in t.getiterator():
                if elem.tag == "s": 
                    if elem.attrib.get('t'):
                        word = elem.text
                        if elem.text.startswith(" "):
                            word = elem.text[1:]
                        if word_to_look.find(word) != -1:
                            last_used = True
                            if not first_time:
                                start_time = int(elem.attrib.get('t')) + closest_nb
                                st_ending = int(elem.attrib.get('ac'))
                                first_time = True
                            end_time = int(elem.attrib.get('t')) + int(elem.attrib.get('ac')) + closest_nb
                        if last_used:
                            end_time = end_time + int(elem.attrib.get('t'))
                            last_used = False
                    else:
                        if end_time == closest_nb:
                            end_time = closest_nb + int(elem.attrib.get('ac'))
                            
            if first_time == False and end_time == closest_nb:
                end_time = closest_nb + st_ending
                #print("{}, {}, {}".format(start_time, end_time, elem.text))
    list_start_end = [start_time,end_time]
    with open('timestamps.txt','a+') as f:
        f.write("{} > {}\n".format(list_start_end[0],list_start_end[1]))
    return list_start_end

#strip_captions("captions/caption_0.xml")
#xml_to_auido()


