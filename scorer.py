## PA5: Tag You're It! CS5242 program by Kimberly Mandery

## This is the second program for PA5
## This program will implement a comparison between the POS tags of the two text files and store the results in a dictionary similar to a confusion matrix
## The user will input a test set tagged by the first program tagger.py and a gold standard tagged test set
## The program will output the entries and values of the confusion dictionary as well as an accuaracy score

## INSTALLATION
## The user will call the program as the following:
## scorer.py output.txt pos-key.txt
## where scorer.py is the name of the program
## output.txt is the predicted tagging by the tagger program for the test data
## pos-key.txt is the actual tagging of the test data

##PRE-PROCESSING
## This program follows a few pre-processing steps for text inputs:
## Assume all words are newline separated strings
## Split each line on POS tag

## OPERATION
## The program will do the following:
## Read in output and tagged test files
## For each word compare the POS tag in each file
## Append a dictionary where the keys consist of the two tags, one from each file.
## For example: if the word is cat and the two results from the files are cat/NN and cat/JJ,
## then the program will add 1 to value of the NN, JJ key in the dictionary
## This "confusion" dictionary has around 170 tag pairs. The POS tags can be found here: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html


import re
import sys
import collections
from collections import *
import tagger #import the tagger program (Part 1 of the PA5 program) to reuse functions

    
def main():
    print ("Command line: " + sys.argv[0] +" " + sys.argv[1] +" "+ sys.argv[2])
    print ("____________________________")
    #Read in tagger output and test key
    pred = tagger.text_in(sys.argv[1])
    actual = tagger.text_in(sys.argv[2])

    L =Counter() # Make a dictionary of tag pairs where the key is the two tags /NN /NN and the value is the count of times they matched
    A = 0 # Count the number of times the program got the correct tag. Use this to find accuaracy later on
    for word in range(len(pred)):
        tag1 = tagger.strip_POS(pred[word])[1] #predited POS tag
        tag2 = tagger.strip_POS(actual[word])[1] #actual POS tag
        if tag1 == tag2: 
            A+=1 #Add one to accuracy counter
        L[str(tag1) + " " + str(tag2)]+=1 # Add one to the count of the tag1 tag2 key

    print ("Confusion Matrix has the form:")
    print ("Predicted | Actual | Count")
    print ("____________________________")
    for tagpair in sorted(L.items()): #order by tag 1 to make comparisons easier
        print (list(tagpair)[0] +": " +str(list(tagpair)[1]))
    print ("____________________________")
    print ("Accuracy is :" + str(A/len(pred))) # Print accuracy
    print ("____________________________")
if __name__=="__main__":
    main()
