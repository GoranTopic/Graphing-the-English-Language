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
import merriam_webster

# word list file
word_list_filename = 'The_Economist_GRE_word_list.txt'
# destination file 
destination_json_file = "dictionary.json"
# line number file
current_line_filename = "current_line_number.txt"

def get_line_number():
    try:
        line_number_file = open(current_line_filename, 'r')
        number = line_number_file.readline().rstrip()
        return int(number)
    except IOError:
        print("number file not found, starting at 0")
        return  0 

def save_line_number(number):
    try:
        line_number_file = open(current_line_filename, 'w')
        line_number_file.write(str(number))
    except IOError:
        print("Could not save line number:" + str(number))

def get_definition(word):
    '''tries to get a definition from diffrent web dictionaries including merriam webster and dictionary.com'''
    # try to get definition from merriam webster
    definition = merriam_webster.query_word(word)
    if definition is not None: 
        return definition
    # try to get definition from merriam webster
    definition = dictionarydotcom.query_word(word)
    if definition is not None:
        return definition
    if definition is None :
        print("could not get definition")
        return None
    


def start_crawling():
    dest_file = open(destination_json_file, 'a')
    word_list_file = open(word_list_filename, 'r')
    cur_line = get_line_number()
    
    for num, word in enumerate(word_list_file):
        if cur_line < num:
            #check if word got a definition    
            print("Getting word " + str(cur_line) +  ": " + word.rstrip())
            definition = get_definition(word)
            if definition is not None:
                # save to json file
                print(definition)
                print("")
                json.dump(definition, dest_file, ensure_ascii=False, indent=4)
                cur_line = num
            else:
                save_line_number(cur_line)
                exit()
    word_list_file.close()
    dest_file.close()
    
def crawl_once():
    dest_file = open(destination_json_file, 'w')
    word_list_file = open(word_list_filename, 'r')
    word = word_list_file.readline()
    definition = merriam_webster.query_word(word)
    word_list_file.close()
    dest_file.close()

start_crawling()
