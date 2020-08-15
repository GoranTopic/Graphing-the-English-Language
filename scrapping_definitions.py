#!/usr/bin/python

#   a program to scrap an store the whole wikipedia vertex and edges,
#   so that an ofline program can find the shortes path on this data
#   istahd of having to do online html requests, which take time
#   by Goran Topic

from word import Word
from urllib.request import urlopen 
from bs4 import BeautifulSoup
from multiprocessing import Queue
import networkx as nx
import pickle
import datetime
import random
import collections
import re
import os
import json
import dictionarydotcom

# word list file
word_list_filename = 'The_Economist_GRE_word_list.txt'
# destination file 
destination_json_file = "dictionary.json"



def start_crawling():
    
    dest_file = open(destination_json_file, 'w')
    word_list_file = open(word_list_filename, 'r')

    for word in word_list_file:
        # get definition
        definition = dictionarydotcom.query_word(word)
        #check if word got a definition
        if definition is not None:
            # save to json file
            print("got word " + word)
            json.dump(definition, dest_file, ensure_ascii=False, indent=4)
        else:
            exit()

    word_file.close()

start_crawling()
