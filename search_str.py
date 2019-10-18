from re import search
def words_list(caption_file,keyphrase):
    caption = open(caption_file,"r")
    fullstring = caption.read()
    fullstring = fullstring.lower()
    substring = keyphrase
    substring = substring.lower()
    test_substring = substring
    last_found_str = substring
    phrases_list = []
    #while string is not empty keep looping
    while test_substring:
        #if substring in fullstring
        #print(test_substring)
        if search(r'\b{}\b'.format(test_substring), fullstring):
            #add to list
            added = test_substring
            if added.startswith(" "):
                added = added[1:]
            if len(added) > 1:   
                phrases_list.append(added)
            #remove the found substring
            substring = substring.replace(test_substring,'',1)
            if len(test_substring.replace(" ","")) < 3:
                break
            test_substring = substring
            #this is the substring from the last found results
            last_found_str = substring
        else:
            #if only one word is left
            if len(test_substring.split()) == 1:
                if len(last_found_str.split()) > 1:
                    #if substring from last found results is more than 1 word, remove the first word and loop through the rest
                    substring = substring.replace(r'\b{}\b'.format(test_substring),'')
                    test_substring = last_found_str.partition(' ')[2]
                    last_found_str = test_substring
                else:
                    #if its a word or less then stop looping
                    break
            else:
                #if there is more than one word remove the last word and keep looping
                test_substring = test_substring.rsplit(' ', 1)[0] 
                if len(test_substring.replace(" ","")) < 3:
                    if len(last_found_str.split()) > 1:
                        #if substring from last found results is more than 1 word, remove the first word and loop through the rest
                        substring = substring.replace(r'\b{}\b'.format(test_substring),'')
                        test_substring = last_found_str.partition(' ')[2]
                        last_found_str = test_substring   

    return phrases_list

#print(words_list("captions/caption_0.xml", "Goddammit i unironically love my gay bros"))