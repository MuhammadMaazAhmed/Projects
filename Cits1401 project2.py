def main(textfile1,textfile2,feature):
    (words1,counts1) = parse_txt(textfile1)
    (words2,counts2) = parse_txt(textfile2)
    if feature=='conjunctions':
        profile_1=conjunctions(words1)
        profile_2=conjunctions(words2)
    if feature=='unigrams':
        profile_1=unigrams(words1)
        profile_2=unigrams(words2)
    if feature=='punctuations':
        profile_1=punctuations(words1,counts1)
        profile_2=punctuations(words2,counts2)
    if feature=='composite':
        profile_1=composite(words1,counts1)
        profile_2=composite(words2,counts2)
        
    dict1=dict(profile_1)
    dict2=dict(profile_2)
    dist=distance(profile_1,profile_2)
    return(dist,dict1,dict2)

def nonblank_lines(f): #skips \n\n lines and counts paragraphs 
    for l in f:
        line= l.replace('\n','"') # adds '"' to end of each line to be removed later
        if line:
            yield line
            
def count_para(w):
    para=1
    while not w[-1]: #deletes blank spaces from the end of the text file
        del w[-1]
    for line in w:
        if not line: #check for empty string
            para+=1
    return (para)

def parse_txt(filename):#tokenises words and counts numb of sentences,';' and ',' from a given txt file   
    words = []
    semicolan_count, comma_count, sentence_count,para_count = 0,0,0,0
    newline_terminators = ['.^^', '!^^', '?^^', ':^^', ';^^',',^^'] #characters that define an end of a line
    sentence_terminators = [".'", '. ', '? ', '! ', '."', '?"', "?'", '!"', "!'"] #characters that define a end of a sentence
    punctuations = [',--','--', ':' , ';' , '"' , " '" , "' " , ", " , " ," ] 
    removes = newline_terminators + sentence_terminators + punctuations       #all the characters than need to be replaced with a space
    removes.append('\n')
    removes.append('^^')
    
    with open(filename) as f:
        iterate=nonblank_lines(f)
        for line in iterate:
            temp_semi_count = line.count(';')
            semicolan_count += temp_semi_count
            
            temp_comma_count = line.count(',')
            comma_count += temp_comma_count
            
            for terminator in sentence_terminators:# counts the occurances characters than define an end of a sentence
                temp_sent_count = line.count(terminator)
                sentence_count += temp_sent_count
                
            if line.startswith("'") : #removes the quotation mark at the start and end of a line
                line = line[1:]
            elif line.endswith("'"):
                line=line[:-1]
                    
            line = line.strip()   
            for remove in removes:
                line = line.replace(remove, ' ').lower()  
            line = line.split()
            words.append(line)
    para_count=count_para(words)
    count=[semicolan_count,comma_count,sentence_count,para_count]
    return (words,count)
   
def conjunctions(w):
    conjunction = {'also': 0, 'although': 0, 'and': 0, 'as': 0, 'because': 0, 'before': 0, 'but': 0, 'for': 0,
                   'if': 0, 'nor': 0, 'of': 0, 'or': 0, 'since': 0, 'that': 0, 'though': 0, 'until': 0, 'when': 0,
                   'whenever': 0, 'whereas': 0, 'which': 0, 'while': 0, 'yet': 0}
    for line in w:
        for word in line:
            if word in conjunction:
                conjunction[word] += 1
    return (conjunction)

def unigrams(w):
    unigram = dict()
    for line in w:
        for word in line:
            if word in unigram:
                unigram[word] += 1
            else:
                unigram[word] = 1 #creates new key 
    return (unigram)

def punctuations(w,c): # c=[number of ';' , number of ',', number of sentences, number of paragraphs]
    punctuation = {';':0, "'":0, '-':0, ',':0}
    punctuation[';']=c[0] 
    punctuation[',']=c[1]
    for line in w:
        for word in line:
            for character in word:
                if character in punctuation:
                    punctuation[character]+=1                                
    return (punctuation)

def word_count(w):
    words=0
    for line in w:
        for word in line:
            words+=1
    return (words)
       
def composite(w,c):
    words=word_count(w)
    profile1=conjunctions(w)
    profile2=punctuations(w,c)
    profile1.update(profile2)
    numb_of_sentences=c[2]
    numb_of_para=c[3]
    profile1['words_per_sentence']= round(words/numb_of_sentences, 4)
    profile1['sentences_per_par']= round(numb_of_sentences/numb_of_para, 4)
    return (profile1)
    
def distance(p1,p2):    
    dist=0
    for key in list(p1):
        if key in p2:
            
            d=p1.pop(key)-p2.pop(key)
            dist+=(d**2)
        else:
            d=p1.pop(key)
            dist+=(d**2)
    if len(p2) != 0:        #counts remaining keys in p2 which werent in p1
        for key in list(p2):
            d=p2.pop(key)
            dist+=(d**2)
    dist=round(dist**(0.5),4)
    return dist
    
