## PA5: Tag You're It! CS5242 program by Kimberly Mandery

## This is the first program for PA5
## This program will implement the "most likely tag" POS tagger.
## The user will input a tagged training file and an untagged test file.
## The program will output a tagged test file.
## The user can then use the output file and a gold standard file as inputs to a
## scorer program that creates a confusion matrix of counts of each classification.


## Additional code has been commented out in order to run a basic model.
## Follow the instructions on commenting out lines 97/98 and 114/115 to run either the basic or extended model
## The basic version has an accuracy of 0.9211777 
## The extended version has an accuracy of 0.9318070


## INSTALLATION
## The user will call the program as the following:
## tagger.py pos-train.txt pos-test.txt
## where tagger.py is the name of the program
## pos-train.txt is the training file with tagged data
## pos-test.txt is the test file with untagged data

## PRE-PROCESSING
## This program follows a few pre-processing steps for text inputs:
## Assume all words are newline separated strings
## Split each line on POS tag
## Testing set has postpended POS tags to each word.
## An example snippet would be: the/DT results/NNS were/VBD trivial/JJ
## where / denotes the beginning of the tag. Each tag abbreviation can be found here:
## https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
## Backward slashes escape forward slashes in the case of: 3\/4/CD

## OPERATION
## The program will do the following:
## Read in training and test sets (text_in function)
## Count each word occurance in the training set (using Counter)
## Sort by most_common (labels function)
## Use regular expression to separate the POS tag from the word (strip_POS function)
## If the word has not been seen yet, append it and its tag to POS_tags list (labels function)
## Label the test set using POS_tags (tagged function)
## Additionally, extended rules are within the extend_rules function. To access, follow the
## details in the tagged function description (location: lines 97/98 and 114/115)

import re
import sys
import collections
from collections import *

## The text_in function will open a text file and return the file split on whitespace
def text_in(file):
    text = open(file, "r") #opens book in read mode
    if text.mode == "r":
        contents = text.read() #lowers text
    text.close()
    return contents.split()

## The strip_POS function will split the word on the last forward slash within the word
def strip_POS(text):
    return text.rsplit("/",1)

## The labels fucntion will create a dictionary to store most likely occurances of all words within the corpus. Computing time is saved by only grabbing the first instances of each word
def labels(text):
    tags=dict() # Use a dictionary to store words as keys (since keys must be unique) and the respective value as the POS tag
    for word, count in text.most_common():
        if strip_POS(word)[0] not in tags.keys(): # The [0] indicates the part stripped before the last forward slash. For example, if I had the text cat/NN, the [0] element would be the string cat and the [1] element would be the string /NN
            tags[strip_POS(word)[0]]=strip_POS(word)[1] # Append tags dictionary with the word as the key and the POS tag as the value
    return tags

## The extend_rules function will deal with unseen test text by implementing the following rules:
def extend_rules(word):
    if re.match(r".*ly$", word): ## If a word ends in "ly" it will be classified as an adverb /RB
        word = word + "/RB"
    elif (re.match(r"^un.*", word)): ## If a word begins with a common prefix like "un" it will be classified as an adjective
        word = word + "/JJ"
    elif (re.match(r".*'s", word)): ## If a word ends with 's it will be classified as a possessive ending /POS
        word = word + "/POS"
    elif (re.match(r"[A-Z].*",word)): ## If a word starts with a capital letter it will be classified as a proper noun NNP
        word = word + "/NNP"
    elif (re.match(r"\d+(-\w+)+", word)): ## If a word has a certain shape like 35-year it will be classified as an adjective JJ. This approach was mentioned in Chapter 8 of the Jurafsky textbook
        word = word + "/JJ"
    elif (re.match(r"\d", word)): ## If a word contains a number it will be classified as a cardinal number /CD
        word = word + "/CD"
    elif (re.match(r".*ier$", word)): ## If a word ends with -ier it will be classified as an adjective
        word = word + "/JJ"
    elif (re.match(r".*ed$", word)):
        word = word + "/JJ" ## If a words ends with -ed it will be  classified as an adjective
    else: 
        word = word +"/NN"
    return word
        

## The tagged function will append words in the test set with the most likely POS tag. If a word was unseen in the training set, the default is to append /NN. To use the extended version of this program, uncomment out tagged.append(extend_rules(word)) and comment out tagged.append(word + "/NN").
def tagged(text, tagsdict):
    tagged=[]
    for word in text:
        if word in tagsdict.keys(): # if the word was in the training corpus
            tagged.append(word + "/"+tagsdict[word]) # use the most likely tag for that word
        # If the word is not in the training corpus
        #elif word.lower() in tagsdict.keys(): # Lower the word and check the training corpus
                #tagged.append(word + "/"+tagsdict[word.lower()])
        else: # Use either basic or extended rules to classify the unseen word
            tagged.append(extend_rules(word)) # Use extended rules to try to accurately tag the word
            ##tagged.append(word + "/NN") # Use default rule to tag unseen words as /NN
    return tagged

def file_out(text, rule):
    with open("pos-test-with-tags-" + str(rule) +".txt",mode='a+') as file:
        file.write(text)
        
def main():
    print ("Command line: " + sys.argv[0] +" " + sys.argv[1] +" " + sys.argv[2])
    print ("____________________________")
    train = text_in(sys.argv[1]) #Read in training and test text
    test = text_in(sys.argv[2])
    word_set=collections.Counter(train) # Gather all instances into a counting dictionary word_set. This will allow us to only keep the most likely classifications
    POS_tags= labels(word_set) # Iterate through word_set and keep the most common POS tag. POS_tags has the form (word : POS_tag)
    test_tagged = tagged(test, POS_tags) # Tag all words in test set with POS tags from the POS_tags dictionary. If a word in the test text is not in the training text, classify it as /NN.
    test_tagged=("\n").join(test_tagged)
    
    file_out(test_tagged, "extend") #Uncomment this line and comment out line 115 (below) to run extended version
##    file_out(test_tagged, "basic")
    print ("Success")
    
if __name__=="__main__":
    main()
