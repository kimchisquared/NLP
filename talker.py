## CS5242: PA 2 The Random Talker by Kimberly Mandery created October 4th 2019
## This program will perform an n-gram language model on a collection of texts
## that the user inputs and outputs a collection of random sentences.
## Ngram language models predict the nth word given (n-1) prior words.
## This means for a trigram model (n=3) we predict the 3rd word given 2 prior words.

## to use this program, you can use the following format in your terminal:
## talker n m text1.txt text2.txt
## where n is the ngram you wish to use (1=unigram, 2=bigram, 3=trigram)
## m is the number of example sentences you wish to output
## you can input as many text.txt you wish, here we only do two.

## We will be implementing the following algorithm
## Read in books to create corpus
## Create unigram counts (unigram) and unigram probabilities (unigramprob)
## Create bigram/trigram counts and probabilities if needed
## Output m sentences using the appropriate make_sentence function

## The unigram probability is c(w)/N.
## The bigram probability is c(w0,w1)/c(w0)
## where c(w0,w1) is in the bigram counter, c(w0) is in the unigram counter.
## The trigram probability is c(w0,w1, w2)/c(w0, w1)
## where c(w0,w1, w2) is in the trigram counter, c(w0,w1) is in the bigram counter.

## modules to import. re is for regular expressions, Counter is for the
## counter of our tokens, sys is for accessing command line arguments (the inputed
## values for n, m and files from the user)
import re
from collections import Counter
import sys
from numpy.random import choice
import itertools
import random


## the book_in function will read in a text and ouput the text string split on whitespace,
## contractions, and EOS
def book_in(text):
    book = open(text, "r") #opens book in read mode
    if book.mode == "r":
        contents = book.read().lower() #lowers text, #capture EOS, split on other punctuations
        contents = re.sub(r"\.|\?|\!", " EOS", contents) #capture ?.! as EOS character
        contents = re.sub(r"\W(?<!['\s])", " ", contents) #get rid of all punctuation except words with contractions
    return filter(None, re.split(r"\s", contents))

## get_(n)prob function will take the (n)count dictionary and return it as a (n)probabilities dictionary
def get_unigramprob(u):
    total = sum(u.values()) 
    for key in u:
        u[key] /=total      #count of each unigram / count of all unigrams
    return u

def get_bigramprob(b,u):
    for key in list(b):
        b[key] /= u[key[0]]        #prob of two words / prob of first word

def get_trigramprob(t, b):
    for key in t:
        t[key] /= b[key[:1]]        #prob of three words / prob of first two words

## get_random will randomly choose one key from the ngram probability dictionary proportional
## to the probability of that ngram key
def get_random(pdict):
    i =random.random()
    total=0
    for k,v in pdict.items():
        total+=v                #cumulative total
        if i <= total:          #random value threshold
            return k

#unigram_sentence will create a sentence from a unigram model
def unigram_sentence(probdict):
    unigram=""
    sentence=[]
    while unigram != "EOS":
        sentence.append(unigram)
        unigram=get_random(probdict)
    print(" ".join(sentence)[1:].capitalize()+".")


#bigram_sentence will create a sentence from a bigram model
def bigram_sentence(b):
    sentence=[]
    big=get_random(b)
    while r".|?|!" not in big:
        if big[1] != ".":
            sentence.append(big)
            big1=dict(filter(str(big[1]) in b.items()))
            big=get_random(b)
    print(" ".join(sentence))


def main():
    print("< This program generates random sentences based off an n-gram language model.")
    print("< Command line settings: " + sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2])
    books = [sys.argv[i] for i in range(3,len(sys.argv))] #finds input text files for the books
    corpus = [word for book in books for word in book_in(book)] #adds all words in all books into corpus
    n=int(sys.argv[1])
    m=int(sys.argv[2])
    
    #get counts and probabilities for each model
    unigram=Counter(corpus)
    unigramprob=get_unigramprob(unigram)
    if n > 1:
        bigram=Counter(list(zip(corpus, corpus[1:])))
        bigramprob=get_bigramprob(bigram, unigram)
        if n > 2:
            trigram = Counter(list(zip(corpus, corpus[1:], corpus[2:])))
            trigramprob=get_trigramprob(trigram,bigram)
            
    #generate sentences based off models
    for i in range(m):
        if n==1:
            print("\nSentence " + str(i+1))
            sentence=unigram_sentence(unigramprob)
        elif n==2:
            sentence=bigram_sentence(bigramprob)
        elif n==3:
            sentence=trigram_sentence(trigramprob)
        print(sentence)

    #sanity check
##    for x in list(unigram)[0:3]:
##        print (x, unigram[x])
##    for x in list(bigram)[0:3]:
##        print (x, bigram[x],x[0],x[1])
##    for x in list(unigramprob)[0:3]:
##        print (x, unigramprob[x])    
##    for x in list(bigramprob)[0:3]:
##        print (x, bigramprob[x],x[0])
    

if __name__ == "__main__":
    main()

            
