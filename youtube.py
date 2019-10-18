#!/usr/bin/env python3
import urllib
import os
import xmlmanager
from auto_captions import get_exact_time
from video_editor import cut_videos


def main():
    search_keyword()

def run_exact_match():
    with open("final_res","r") as fr:
        for line in fr:
            print(line)
            lines = line.split("$$")
            sub_time = float(lines[1]) * 1000
            kwrd  = lines[2]          
            print(get_exact_time(int(sub_time),kwrd))


def find_best_urls(keyphrase):
        list_of_items = []
        list_of_keywords = []
        list_ids = []
        phrase = keyphrase
        with open("outputs","r") as opt:
            for line in opt:
                items = str(line).split("|")
                if len(items) > 2:
                    list_of_items.append(items)
            for items in list_of_items:
                keyword = items[1].replace('Keyword : ','')
                keyword = keyword[1:]
                while(keyword[-1] == " "):
                    keyword = keyword[:-1]
                list_of_keywords.append(keyword)
            
            list_of_keywords.sort(key=len)
            list_of_keywords.reverse()
            done = False
            while list_of_keywords and not done:
                big_phrase = list_of_keywords[0]
                
                if big_phrase in phrase:
                    phrase = phrase.replace(big_phrase, "")
                    list_ids.append(big_phrase)
                val = big_phrase
                list_of_keywords = [value for value in list_of_keywords if value != val]
                if(phrase == "" or phrase == " "):
                    done = True
        list_done_items = list_ids.copy()
        list_sorter = []
        for word in list_done_items:
            list_sorter.append(keyphrase.find(word))
        new_list = list_done_items.copy()
        list_sorter.sort()
        for index, nb in enumerate(list_sorter):
            for word in list_done_items:
                if keyphrase.find(word) == nb:
                    new_list[index] = word
        #print(new_list)
        for word in new_list:
            for item in list_of_items:
                keyword = item[1].replace("Keyword : ","")
                while keyword[-1] == " ":
                    keyword = keyword[:-1]
                while keyword[0] == " ":
                    keyword = keyword[1:]                
                if keyword == word:
                    with open("final_res", "a+") as res:
                        #print(item[2])
                        res.write("{} $$ {}\n".format(item[2][:-1], keyword))
                        res.close
                        break
        run_exact_match()
        #cut_videos()



            
            
def clear_files():
    with open("ouputs","w") as f:
        f.close()
    with open("final_res","w") as f2:
        f2.close()
    with open('timestamps.txt','w') as f3:
        f3.close()
        
def search_keyword():
    clear_files()
    print("Enter a keyphrase you want to look for.")
    keyword = input('Choose a keyword ')
    keyword = keyword.lower()
    num = 1
    num = sum(1 for line in open('output.txt'))
    caption_files = []
    for i in range(num):
        caption_xml = "captions/caption_%s.xml"%(str(i))

        caption_files.append(caption_xml)

    xmlmanager.search_keyphrase(caption_files,keyword)
    """ for item in caption_files:
        print(item) 
        isEmpty = os.path.getsize(item) == 0
        exits = os.path.isfile(item)
        if exits and not isEmpty:
            xmlmanager.search_keyphrase(item,keyword) """
    

    find_best_urls(keyword)
    keep_going = input('Do you wanna look for another word? Y/N ')
    if keep_going == 'Y' or keep_going == 'y':
        search_keyword()
    else:
        return 0



if __name__ == '__main__':
    main()
