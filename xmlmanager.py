import xml.etree.ElementTree as ET
import webbrowser
import string
import os
from html.parser import HTMLParser
import re
from search_str import words_list

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{0} day{1}, ".format(days, "s" if days!=1 else "") if days else "") + \
    ("{0} hour{1}, ".format(hours, "s" if hours!=1 else "") if hours else "") + \
    ("{0} minute{1}, ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
    ("{0} second{1}, ".format(seconds, "s" if seconds!=1 else "") if seconds else "")
    return result
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
def getVidID(xml_file):
    linenb = xml_file.split("_",1)[1]
    linenb = linenb.split(".")[0]
    with open("output.txt") as f:
        for i, line in enumerate(f):
            if i == int(linenb):
                return line.rstrip()
    return "empty"

def to_parseable(tree):
    t = ET.tostring(tree)
    t = t.lower()
    return ET.fromstring(t)

def checkBetween(sentence,keyword):
     #print(sentence)
     fstring = str(sentence)
     lstring = str(sentence)
     try:
      fstring = sentence.split(keyword)[0]
      lstring = sentence.split(keyword,1)[1]
     except IndexError:
      pass

     ssymbols = ['(','"','*','[','{']
     esymbols =[')','"','*',']','}']
     if ':' in fstring:
         #print("false :")
         return False
     for index,s in enumerate(ssymbols):
         if s in fstring:
             #print("true ssym")
             if esymbols[index] in lstring:
                 #print("true esym")
                 return False
     return True

def getCaptionInfo(xml_file,keyword):
    #check if file is empty
    #okeyword=keyword
     try:
        e = ET.parse(xml_file)
     except Exception as e:
        return "empty"
     root = e.getroot()
     e = to_parseable(root)

     translator=str.maketrans('','',string.punctuation)
     keyword = keyword.translate(translator) #add this
     #keyword = " {} ".format(keyword)
     filename = "empty.txt"
     for text in e.findall('text'):
        start_element = text.get('start') # equivalent to .attrib() in this case
        dur_element = text.get('dur')
        flavor = text.text
        info_list = []
        if isinstance(flavor, str):
            flavor = HTMLParser().unescape(flavor)
            translator=str.maketrans('','',string.punctuation)
            pun_flavor = flavor
            flavor=flavor.translate(translator)
            flavor = HTMLParser().unescape(flavor)
        if flavor and keyword in flavor:
          pun_flavor = HTMLParser().unescape(pun_flavor)
          #if "[" not in pun_flavor and "*" not in pun_flavor and u'"' not in pun_flavor and "(" not in pun_flavor and ":" not in pun_flavor:
          if checkBetween(pun_flavor,keyword):
          #if True:
            info_list.append(start_element)
            info_list.append(dur_element)
            info_list.append(flavor)
            pos = flavor.find(keyword)
            pos = pos + 1
            #pos_keyword = pos
            #if(len(flavor) > 0 and pos > 0):
                #pos_keyword = 1 / (len(flavor) / pos)
            #pos_keyword = 1
            #print("position is :",pos_keyword,"///",len(flavor.split()) ,"///",pos)
            time_float = float(start_element)
            #time_float = float(start_element) + (float(dur_element)*pos_keyword)
            url = "{video}&t={time}".format(video=getVidID(xml_file),time=int(time_float))
            #webbrowser.open(url.rstrip())
            #line_url = "{}\n".format(url)
            with open("outputs", "a+") as op:
                opt = "Full Part : {} | Keyword : {} | Url : {} $$ {}\n".format(pun_flavor,keyword,url,start_element)
                #opt = "Start time: {}",start_element, "\nDuration: ",dur_element, "\nFull Part: ", pun_flavor, "\nURL: ",url
                op.write(opt)    
            
            #break
            #return info_list
     return filename

def search_keyphrase(caption_files,keyphrase):
        full_keywords = []
        for xml_file in caption_files: 
            isEmpty = os.path.getsize(xml_file) == 0
            exits = os.path.isfile(xml_file)
            if exits and not isEmpty:
                #xmlmanager.search_keyphrase(item,keyword)
                keywords_to_search = words_list(xml_file,keyphrase)
                #print(xml_file)
                #print(keywords_to_search)
                #print(full_keywords)
                if full_keywords is not None:
                    keywords_to_search = list(set(keywords_to_search) - set(full_keywords))
                    if keywords_to_search:
                        full_keywords.extend(keywords_to_search)
                        result_file = open("res.txt", "a+")
                        result_file.write("{}\r\n".format(keywords_to_search))
                        result_file.close
                        for keyword in keywords_to_search:
                            getCaptionInfo(xml_file,keyword)
