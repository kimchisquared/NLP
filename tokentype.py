import re
import sys

word_boundary=r"\b\w+\b"

def tokens(text):
    return len(text)

def types(text):
    return len(set(text))

def book_in(text):
    book = open(text, "r")
    if book.mode == "r":
        contents = book.read().lower().split()
        print(str(text))
        print ("Tokens : " + str(tokens(contents)))
        print ("Types : " + str(types(contents)))
        print ("Token/Type ratio : " +str(tokens(contents)/types(contents)))

def main():
    print("< This program will tell you how many tokens and types are in your text.")
    print("< Command line settings: " + str([sys.argv[i] for i in range(0,len(sys.argv))]))
    texts = [sys.argv[i] for i in range(1,len(sys.argv))]
    out = [book_in(txt) for txt in texts]
          

if __name__ == "__main__":
    main()
              
