## PA 4: Similar to What? CS5242 program by Kimberly Mandery. Wednesday November 6, 2019.

## This program will measure the similiarity between words in various documents using tf-idf and cosine metrics.
## The user will input two words they wish to measure the similarity for.
## The program will output a similarity measure between 0 and 1. The closer to 1, the closer the similarity.
## For example, if the user inputs "fish" and "fish", the output will be 1.
## The user will enter "exit" twice to exit the program.

## NOTE: this program does not rely on efficiency.
## Some functions are available in numpy/pandas that would decrease resource consumption.
## Make sure to run this program in a capable environment.

## The user will call the program as the following:
## similar.py /home/cs/mande143/Pang-Lee-PA4/*
## where similar.py is the name of the program
## home/cs/mande143/Pang-Lee-PA4/* is the directory where the folder lives
## and the * at the end will grab all files in the folder

## This program uses the following for pre-processing the corpus: 
## Remove all non-alphanumeric characters
## Assume all words are space separated strings
## Lower all text


## Cosine and tf-idf measures are taken from Chapter 6 of Speech and Language Processing by Jurafsky and Martin 2019.
## You can find the text here: https://web.stanford.edu/~jurafsky/slp3/6.pdf


#libraries
import math #for sqrt and log in tf_idf and cosine functions
import sys #for reading in command line arguments
import os #for searching for files in a directory
import re #for replacing nonalphanumeric characters in files_in function
import time # to test efficiency of the program

## The files_in function will read in a file and ouput the text string split on word boundaries.
## The pre-processing outlined earlier is used in this function.
def files_in(file):
    text = open(file, "r") #opens book in read mode
    if text.mode == "r":
        contents = text.read().lower() #lowers text
        contents = re.sub(r"[^A-Za-z\s]", "", contents).split() #replace all non-alphanumeric with blanks
    return contents

## The dot_prod function will return the dot product of two equal sized vectors.
# This function does not error check the length of the vectors.
def dot_prod(vec1, vec2):
    return sum(vec1[i]*vec2[i] for i in range(len(vec1)))

#the tf_idf function will return the term frequency * document frequency as outlined in the textbook linked earlier
def tf_idf(vec1, dic):
    tf = [vec1[i]/len(dic[i]) for i in range(len(vec1))]
    df = sum(vec1[i]>0 for i in range(len(vec1)))
    idf = [math.log(len(vec1)/df)]*len(vec1)
    return [tf[i]*idf[i] for i in range(len(tf))]

#the cosine function will return a single value as outlines in the aforementioned text
def cosine(vec1, vec2):
    n = math.sqrt(dot_prod(vec1,vec1)*dot_prod(vec2,vec2))
    if n == 0.0:
        return 0
    else:
        return dot_prod(vec1, vec2)/n

def main ():
    print ("Command line: " + sys.argv[0] +" " + sys.argv[1])
    print ("--------------------------------")
    # Read in files from directory the user inputs
    filepath=str(sys.argv[1])
    filenames = os.listdir(filepath)
    
    # Create list of texts and a corpus
    texts=[files_in(str(filepath)+"/"+str(file)) for file in filenames]
    corpus=sorted(list(set([word for text in texts for word in text])))

    # Prompt the user for two words and lower to reduce inconsistencies
    print ("Enter two words, press Enter after the first word:")
    word1 = str(input().lower())
    word2 = str(input().lower())

    # Allow user to exit program
    while (word1 != "exit" or word2 != "exit"):

        # If the words are both in the set corpus
        if word1 and word2 in corpus:
            
            # Count the number of times each word occurs in each text
            wordvec1=[text.count(word1) for text in texts]
            wordvec2 = [text.count(word2) for text in texts]
            
            # Remove all low-frequency words (words occuring only one time in the entire corpus)
            # This will cut down problem space and reduce noise.
            if sum(wordvec1) <2 or sum(wordvec2)<2:
                print ("One of your words does not occur often enough")
                print ("--------------------------------")
            else:
                wordvec1 = tf_idf(wordvec1,texts)
                wordvec2 = tf_idf(wordvec2, texts)
                print(cosine(wordvec1, wordvec2))
                print ("--------------------------------")
            # Prompt user to input new words to test
            print ("Enter two new words:")
            word1 = str(input().lower())
            word2 = str(input().lower())
            
        else:
            # Prompt the user to input new words that have a likelier chance of being in the texts

            print ("One of your words is not in the corpus")
            print ("--------------------------------")
            print ("Enter two new words:")
            word1 = str(input().lower())
            word2 = str(input().lower())
    


if __name__=="__main__":
    main()

